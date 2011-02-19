#####################################################################################################
##
##      duplicatesmanager.py - a script for comicrack
##
##      Author: perezmu
##
##      Copyleft perezmu 2011. 
##
##        Detailed credits: "http://code.google.com/p/comicrack-duplicates-manager/wiki/FellowCredits"
##
######################################################################################################



#########
#
#    Import section

import sys, traceback
import re
import clr
import System
import System.IO
from System.IO import Path, Directory, File, FileInfo

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import DialogResult, MessageBox, MessageBoxButtons, MessageBoxIcon


from itertools import groupby
from dmBookWrapper import *
from utilsbycory import cleanupseries
from processfunctions import *
from dmParser import *
from utilsbycory import *

from constants import *


#
#
##########

  
##'''---------------------------------------------------------'''


############
#
#   MAIN FUNCTION


#@Name DuplicatesManager
#@Hook Books
#@Image duplicatesmanager.png

def DuplicatesManager(books):

    ########################################
    #
    # Starting log file
    #
    
    if not Directory.Exists(DUPESDIRECTORY):
        try:
            Directory.CreateDirectory(DUPESDIRECTORY)
        except Exception, ex:
            MessageBox.Show('ERROR: '+ str(ex), "ERROR creating dump directory" + DUPESDIRECTORY, MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
            return
    
    logfile = open(LOGFILE,'w')
    logfile.write('COMICRACK DUPLICATES MANAGER V '+VERSION+'\n\n')
    ''' Logfile initialized '''
    
    #
    #
    #########################################
    
    try:
        ProcessDuplicates(books, logfile)
    
    except Exception, ex:
        logfile.write('\n\nSTOPPED PROCESSING BECAUSE OF EXCEPTION:\n')
        traceback.print_exc(None, logfile, False)
        raise ex
        
    finally:
        logfile.close()



def ProcessDuplicates(books, logfile):
    
    #########################################
    #
    # Getting comics info
        
    comiclist = []
    for book in books:
        
        b = dmBookWrapper(book)
        # re.sub(r'^0+','',b.Number) -> removes leading 0's
        series = b.Series
        if b.Volume:
            series += ' Vol.' + b.Volume
        comiclist.append((cleanupseries(series),re.sub(r'^0+','',b.Number),b.Volume,b.FileName,b.PageCount,b.FileSize/1048576.0,b.ID,b.CVDB_ID,b.FilePath,book.Tags,book.Notes,b.FileFormat,book))

    logfile.write('Parsing '+str(len(comiclist))+ ' ecomics\n')

   
    #
    #
    ########################################

    #########################################
    #
    # Setting intial options values

    options = {"movefiles":MOVEFILES,
               "removefromlib":REMOVEFROMLIB,
               "updateinfo":UPDATEINFO,
               "verbose":VERBOSE,
               "debug":DEBUG,
               "sizemargin":SIZEMARGIN,
               "coverpages":COVERPAGES,
               "c2c_noads_gap":C2C_NOADS_GAP}
                   
    ########################################
    #
    # Main Loop
    #

    try:
     
        ###########################################
        #
        # Load rules file
                
        rules = LoadRules(logfile, options)

        #
        ############################################

        
        
        ############################################
        #
        # Massage comics to get a list of dupes groups
        
        ''' Now we group books looking for dupes! '''
        comiclist.sort()
        ''' begin sorting and sort the list '''

                # TODO: I need to cleanup the series names and issues 1/2, 0.5, etc...
                # TODO: Also, check for CVDB items first!

        cl = {}
        ''' temp dictionary'''
        for key, group in groupby(comiclist, lambda x: x[SERIES]):
                cl[key] = list(group)
                '''groups by series'''
                ''' cl is a dictionary that now has 'series' as keys'''
                ''' we remove series with only one ecomic '''
        
        logfile.write('============= Begining dupes identification ==================================\n\n')             
        
        logfile.write('Parsing '+str(len(comiclist))+ ' ecomics\n')
        logfile.write('Found '+str(len(cl))+ ' different series\n')
                
        if options["verbose"]:
            for series in sorted(cl.keys()):
                            logfile.write('\t'+series+'\n')
        
        remove = []
        for series in cl.keys():
                if len(cl[series])==1:
                                remove.append(series)   
        for series in remove:
                del cl[series]
        logfile.write('Found '+str(len(cl))+ ' different series with more than one issue\n')
                
        if options["verbose"]:
            for series in sorted(cl.keys()):
                            logfile.write('\t'+series+'\n')
                
        ''' we now regroup each series looking for dupe issues '''
        for series in cl.keys():
                cl[series].sort()
                        
                temp_dict = {} 
                for key, group in groupby(cl[series], lambda x: x[NUMBER]):
                        temp_dict[key] = list(group)
                        cl[series] = temp_dict
                                
        
                
        ''' cleaning issues without dupes '''
        remove = []
        for series in cl.keys():
                for number in cl[series]:
                        if len(cl[series][number])==1:
                                        remove.append([series,number])
                
        for a in remove:
                del cl[a[0]][a[1]]
        
        
        ''' now a second go for series without issues after non-dupe removal '''
        remove = []
        for i in cl:
                if len(cl[i])==0:
                                remove.append(i)
        for i in remove:
                del cl[i]

        logfile.write('Found '+str(len(cl))+ ' different series with dupes\n')
        if options["verbose"]:
            for series in sorted(cl.keys()):
                            logfile.write('\t'+series+'\t('+str(cl[series].keys())+')\n')
                
        ''' Now I have them sorted, I convert them to a simple list of lists (groups)...
        each item in this list is a list of dupes '''
        
        dupe_groups = []
        for i in cl:
                for j in cl[i]:
                        dupe_groups.append(cl[i][j])
        
        logfile.write('Found '+str(len(dupe_groups)) +' groups of dupes, with a total of '+ str(len(reduce(list.__add__, dupe_groups, [])))+ ' ecomics.\n')
        if options["verbose"]:
                for group in sorted(dupe_groups):
                        logfile.write('\t'+group[0][SERIES]+' #'+group[0][NUMBER]+'\n')
                        for comic in group:
                                logfile.write('\t\t'+comic[FILENAME]+'\n')

        dupe_groups.sort()

        logfile.write('\n============= End of dupes identification=====================================\n\n\n\n')
        logfile.write('============= Beginning dupes processing =====================================\n\n')
        
        del cl
        
        #
        ##########################################################
        
        #
        #      Exception handling
        #

    except NoRulesFileException, ex:
        MessageBox.Show('ERROR: '+ str(ex), "ERROR in Rules File", MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
        logfile.write('\n\nERROR in Rules File:\n')
        traceback.print_exc(None, logfile, False)
        return
        
        
    ###################### processing ########################################
    
    movedcomics = 0
    
    new_groups = []
    
    # fix for issue 4 - if there are no dupes, end gracefully
    if len(dupe_groups) == 0:
        MessageBox.Show('Script execution completed: No duplicates found in the comics selected', 'Success', MessageBoxButtons.OK, MessageBoxIcon.Information)
        logfile.write('\n\n\n\ ########################################################### \n\n\n')
        logfile.write('Scritp execution completed: No duplicates found in the comics selected')
        
        del dupe_groups
        del new_groups
        return
    
    for group in dupe_groups:
        
        t_group = group[:]

        logfile.write('\n= PROCESSING GROUP_____\n')
        logfile.write('= '+ t_group[0][SERIES] + ' #'+str(t_group[0][NUMBER])+'\n')
        
        i_rules = 0
        
        while (len(t_group)> 1) and (i_rules < len(rules)):
            t_rule = rules[i_rules][:]
            
            line = t_rule[0]
            t_rule = t_rule[1:]
            
            logfile.write('\n_________________  ')
            logfile.write(line)
            logfile.write('  _________________\n')
            logfile.flush()
            
            if options["debug"]:
                logfile.write('  ' + str(t_rule) + '\n')
            
            t_rule.append(t_group[:])
            t_rule.append(logfile)
            t_rule.insert(1,ComicRack)
            t_rule.insert(1,options)
            
            t_group = globals()[t_rule[0]](*t_rule[1:])     ### this is the trick to call a function using a string with its name
            
            i_rules = i_rules+1
        
        new_groups.append(t_group)

    
    dupe_groups = new_groups[:]
    
    remain_comics = len(reduce(list.__add__, new_groups))
    
    for group in dupe_groups:
        if len(group) == 1: new_groups.remove(group)
    
    # new_groups holds now the remaining groups for logging purposes
    
    #if len(dupe_groups)>=1:
    #    print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'

    #
    #   End of Main Loop
    #
    ###########################################################

#### End report

    MessageBox.Show('Scritp execution completed correctly on: '+ str(len(books))+ ' books.\n - '+str(len(dupe_groups))+' duplicated groups processed.\n - '+str(len(new_groups))+' duplicated groups remain.\n - '+str(remain_comics)+' comics remain', 'Sucess', MessageBoxButtons.OK, MessageBoxIcon.Information)
    logfile.write('\n\n\n\ ########################################################### \n\n\n')
    logfile.write('Scritp execution completed correctly on: '+ str(len(books))+ ' books.\n'+str(len(dupe_groups))+' duplicated groups processed.\n'+str(len(new_groups))+' duplicated groups remain..\n'+str(remain_comics)+' comics remain')

#### Garbage collecting

    del dupe_groups
    del new_groups

    return


#### ============================================================================================================================
    
###############################
#
#    Read and parse rules files dmrules.dat
#    
    
def LoadRules(logfile, options):
    
    # Check if file exists
    if not File.Exists(RULESFILE):
        raise NoRulesFileException('Rules File (dmrules.dat) could not be found in the script directory ('+ SCRIPTDIRECTORY +')')
    
    # Read file
    f = open(RULESFILE, 'r')
    all_lines = f.readlines()
    f.close()

    # Parse rules and filter out options
    options_list = []
    rules = []
    for line in Parse(all_lines):
        if line[2] == '@':
            options_list.append(line)
        elif line[2][0] == '@':
            options_list.append(line[:2] + ['@', line[2][1:]] + line[3:])
        else:
            rules.append(line)
    
    logfile.write('\n\n============= Beginning options reading ==================================\n\n')               
    logfile.write('Successfully read the following options: \n\n')
    for option in options_list:
        logfile.write('\tLine ' + str(option[0]) + ': ' + str(option[3:]) + '\n')
    logfile.write('\n')
            
    logfile.write('\n\n============= Beginning rules reading ==================================\n\n')               
    logfile.write('Successfully read the following rules: \n\n')
    for rule in rules:
        logfile.write('\tLine ' + str(rule[0]) + ': ' + str(rule[2:]) + '\n')
    logfile.write('\n')
      
    bool_options = ("movefiles", "removefromlib", "updateinfo", "verbose", "debug")
    int_options = ("sizemargin", "coverspages", "c2c_noads_gap")

    
#
#   Parse options
#
#               Checks if options need to have (and in fact do have) boolean or integer values

    bDict = {"false":False, "true":True}
     
    for option in options_list:
        opLineNum = option[0]
        opLine = option[1]
        
        if len(option) != 5:
            raise NoRulesFileException('Line ' + str(opLineNum) + ': Option "' + opLine + '" has wrong format')
            
        opName = option[3].lower()
        opVal = option[4].lower()

                                            # boolean option
        if opName in bool_options:
            opVal = opVal
            if opVal in bDict.keys():
                options[opName] = bDict[opVal]
            else:
                raise NoRulesFileException('Line ' + str(opLineNum) + ': Option "'+ opLine +'" value is invalid ("True" or "False" required)')
                
                                            # integer option
        elif opName in int_options:
            try:
                options[opName] = int(opVal)
            except:
                raise NoRulesFileException('Line ' + str(opLineNum) + ': Option "'+ opLine +'" value is invalid (integer required)')             
                                            # failure
        else:
            raise NoRulesFileException('Line ' + str(opLineNum) + ': Option "'+ opLine +'" not recognized (' + str(opName) + ')')
   

    logfile.write('\n\n============= Beginning options parsing ==================================\n\n')               
    logfile.write('Using the following options: \n\n')
    for option in options:
        logfile.write('\t'+option.upper() + " = " + str(options[option]).upper()+'\n')
        
#
#   Parse rules
#

    logfile.write('\n\n============= Beginning rules parsing ==================================\n\n')               
    
    parsed_rules = []
        
    for rule in rules:
        parsed_rules.append(ParseRule(rule))            
			
    if VERBOSE:
        logfile.write('\nParsed rules:\n\n')
        for rule in parsed_rules:
            logfile.write('\t\t'+str(rule)+'\n')
    logfile.write('\n============= End of rules parsing ======================================\n\n\n\n')  

    return parsed_rules

    

def AsPercentage(args, index, defVal):
    if index < len(args):
        text = args[index]
    else:
        text = defVal
    
    if text[-1] == '%':
        num = text[:-1]
    else:
        num = text 
    
    try:
        return int(num)
    except:
        raise Exception('Invalid percentage value: ' + text)
    


known_rules = [
    [ ["pagecount", "keep", "fileless"],  lambda args: ["keep_pagecount_fileless"] ],
    [ ["pagecount", "remove", "fileless"],lambda args: ["remove_pagecount_fileless"] ],
    [ ["pagecount", "keep", "largest"],   lambda args: ["keep_pagecount_largest", AsPercentage(args, 0, "0%")] ],
    [ ["pagecount", "remove", "largest"], lambda args: ["remove_pagecount_largest", AsPercentage(args, 0, "0%")] ],
    [ ["pagecount", "keep", "smallest"],  lambda args: ["keep_pagecount_smallest", AsPercentage(args, 0, "0%")] ],
    [ ["pagecount", "remove", "smallest"],lambda args: ["remove_pagecount_smallest", AsPercentage(args, 0, "0%")] ],
    [ ["pagecount", "keep", "noads"],     lambda args: ["keep_pagecount_noads"] ],
    [ ["pagecount", "keep", "c2c"],       lambda args: ["keep_pagecount_c2c"] ],
    [ ["filesize", "keep", "largest"],    lambda args: ["keep_filesize_largest", AsPercentage(args, 0, "0%")] ],
    [ ["filesize", "remove", "largest"],  lambda args: ["remove_filesize_largest", AsPercentage(args, 0, "0%")] ],
    [ ["filesize", "keep", "smallest"],   lambda args: ["keep_filesize_smallest", AsPercentage(args, 0, "0%")] ],
    [ ["filesize", "remove", "smallest"], lambda args: ["remove_filesize_smallest", AsPercentage(args, 0, "0%")] ],
    [ ["covers", "keep", "some"],         lambda args: ["keep_covers_all", False] ],
    [ ["covers", "keep", "all"],          lambda args: ["keep_covers_all", True] ],
    [ ["filename", "keep"],               lambda args: ["keep_with_words", args, [FILENAME]] ],
    [ ["filename", "remove"],             lambda args: ["remove_with_words", args, [FILENAME]] ],
    [ ["filepath", "keep"],               lambda args: ["keep_with_words", args, [FILEPATH]] ],
    [ ["filepath", "remove"],             lambda args: ["remove_with_words", args, [FILEPATH]] ],
    [ ["tags", "keep"],                   lambda args: ["keep_with_words", args, [TAGS]] ],
    [ ["tags", "remove"],                 lambda args: ["remove_with_words", args, [TAGS]] ],
    [ ["notes", "keep"],                  lambda args: ["keep_with_words", args, [NOTES]] ],
    [ ["notes", "remove"],                lambda args: ["remove_with_words", args, [NOTES]] ],
    [ ["text", "keep"],                   lambda args: ["keep_with_words", args, [FILENAME, FILEPATH, TAGS, NOTES]] ],
    [ ["text", "remove"],                 lambda args: ["remove_with_words", args, [FILENAME, FILEPATH, TAGS, NOTES]] ],
    [ ["filetype", "keep"],               lambda args: ["keep_with_words", args, [FILETYPE]] ],
    [ ["filetype", "remove"],             lambda args: ["remove_with_words", args, [FILETYPE]] ],
    [ ["keep", "first"],                  lambda args: ["keep_first"] ],
]


def ParseRule(rule):
    line_num = rule[0]
    line = rule[1]
    rule_tokens = rule[2:]
    
    # Try to match to a known command
    for cmd in known_rules:
        tokens = cmd[0]
        action = cmd[1]
        
        if len(rule_tokens) < len(tokens):
            continue
        
        # Check it the rule matches the command
        matches = True
        for i in range(len(tokens)):
            if tokens[i] != rule_tokens[i]:
                matches = False
                break;
        
        if not matches:
            continue
        
        args = rule_tokens[len(tokens):]
        
        try:
            result = [line]
            result.extend(action(args))
            return result
        except Exception, ex:
            raise NoRulesFileException('Line ' + str(line_num) + ': ' + str(ex) + '\n' + line)
    
    # If got here not command was matched
    raise NoRulesFileException('Line ' + str(line_num) + ': Rule could not be parsed:\n' + line) 



class NoRulesFileException(Exception):
    pass
    
