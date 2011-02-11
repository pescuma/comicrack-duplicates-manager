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
                logfile.write('ERROR: '+str(ex)+'\n')
                print Exception
    
    logfile = open(LOGFILE,'w')
    logfile.write('COMICRACK DUPLICATES MANAGER V '+VERSION+'\n\n')
    ''' Logfile initialized '''
    
    #
    #
    #########################################
    
    
    
    #########################################
    #
    # Getting comics info
        
    comiclist = []
    for book in books:
        
        b = dmBookWrapper(book)
        # re.sub(r'^0+','',b.Number) -> removes leading 0's
        comiclist.append((cleanupseries(b.Series),re.sub(r'^0+','',b.Number),b.Volume,b.FileName,b.PageCount,b.FileSize/1048576.0,b.ID,b.CVDB_ID,b.FilePath,book.Tags,book.Notes,book))

    logfile.write('Parsing '+str(len(comiclist))+ ' ecomics\n')

  

    
    #
    #
    ########################################


    ########################################
    #
    # Main Loop
    #

    try:
     
        ###########################################
        #
        # Load rules file
                
        rules = LoadRules(logfile)

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
                
        if VERBOSE:
            for series in sorted(cl.keys()):
                            logfile.write('\t'+series+'\n')
                
        remove = []
        for series in cl.keys():
                if len(cl[series])==1:
                                remove.append(series)   
        for series in remove:
                del cl[series]
        logfile.write('Found '+str(len(cl))+ ' different series with more than one issue\n')
                
        if VERBOSE:
            for series in sorted(cl.keys()):
                            logfile.write('\t'+series+'\n')
                
        ''' we now regroup each series looking for dupe issues '''
        for series in cl.keys():
                cl[series].sort()
                        
                temp_dict = {} 
                for key, group in groupby(cl[series], lambda x: x[NUMBER]):
                        temp_dict[key] = list(group)
                        cl[series]= temp_dict
                                
        
                
        ''' cleaning issues without dupes '''
        remove = []
        for series in cl.keys():
                for number in cl[series]:
                        if len(cl[series][number])==1:
                                        remove.append((series,number))
                
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
        if VERBOSE:
            for series in sorted(cl.keys()):
                            logfile.write('\t'+series+'\t('+str(cl[series].keys())+')\n')

                
        ''' Now I have them sorted, I convert them to a simple list of lists (groups)...
        each item in this list is a list of dupes '''
        
        dupe_groups = []
        for i in cl:
                for j in cl[i]:
                        dupe_groups.append(cl[i][j])
        
        logfile.write('Found '+str(len(dupe_groups)) +' groups of dupes, with a total of '+ str(len(reduce(list.__add__, dupe_groups)))+ ' ecomics.\n')
        if VERBOSE:
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
        logfile.write('ERROR: '+str(ex)+'\n')
        print NoRulesFileException
        
    except Exception, ex:
        logfile.write('ERROR: '+ str(Exception) +' -> '+str(ex)+'\n')
        print "The following error occured"
        print Exception
        print str(ex)
        
        
    ###################### processing ########################################
    
    movedcomics = 0
    
    new_groups = []
    
    # fix for issue 4 - if there are no dupes, end gracefully
    if len(dupe_groups) == 0:
        MessageBox.Show('Scritp execution completed: No duplicates found in the comics selected', 'Sucess', MessageBoxButtons.OK, MessageBoxIcon.Information)
        logfile.write('\n\n\n\ ########################################################### \n\n\n')
        logfile.write('Scritp execution completed: No duplicates found in the comics selected')
        
        del  dupe_groups
        del new_groups
        logfile.close()
        
        return
    
    for group in dupe_groups:
        
        t_group = group[:]

        logfile.write('\n= PROCESSING GROUP_____\n')
        logfile.write('= '+ t_group[0][SERIES] + ' #'+str(t_group[0][NUMBER])+'\n')
        logfile.write('\n')
        
        i_rules = 0
        
        while (len(t_group)> 1) and (i_rules < len(rules)):
            t_rule = rules[i_rules][:]
            
            t_rule.append(t_group[:])
            t_rule.append(logfile)
            t_rule.insert(1,ComicRack)
            
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

    del  dupe_groups
    del new_groups
    logfile.close()

    
    
    return


#### ============================================================================================================================
    
###############################
#
#    Read and parse rules files dmrules.dat
#    
    
def LoadRules(logfile):

    rules = ""
    
    # Read file
    
    if File.Exists(RULESFILE):
        f = open(RULESFILE, 'r')
        rules = f.readlines()
        f.close()
        
        # Delete empty lines
        clean_rules = rules[:]
        for line in rules:
            if (line == "\n") or (line[0]=="#"):
                clean_rules.remove(line)
        rules = clean_rules[:]
        
        logfile.write('\n\n============= Beginning rules parsing ==================================\n\n')               
        logfile.write('Successfully read the following rules: \n\n')
        for rule in rules:
            logfile.write('\t'+rule)
        logfile.write('\n')
                            
    else:
        raise NoRulesFileException('Rules File (dmrules.dat) could not be found in the script directory ('+ SCRIPTDIRECTORY +')')
    
#
#   Parse rules
#
    raw_rules = rules[:]
    strip_rules = []
    parsed_rules = []    
    
    index_dict = {"filename":FILENAME, "filepath":FILEPATH, "tags":TAGS, "notes":NOTES}
    
    for raw_rule in raw_rules:
        rule = raw_rule.split()
        strip_rules.append(rule)
                
    for strip_rule in strip_rules:
                
        if len(strip_rule) != 3:
             RaiseParseException(strip_rule)
        
        if strip_rule[0].lower() == "pagecount":
            if strip_rule[1].lower() == "keep":
                if strip_rule[2].lower() in ["fileless", "largest", "smallest", "noads", "c2c"]:
                    parsed_rules.append(["keep_pagecount_"+strip_rule[2]])
                    
                else: RaiseParseException(strip_rule)               
            elif strip_rule[1].lower() == "remove":
                if strip_rule[2].lower() == "fileless":
                    parsed_rules.append(["remove_pagecount_fileless"])
                    
                else: RaiseParseException(strip_rule)
            else: RaiseParseException(strip_rule)
            
        elif strip_rule[0].lower() == "filesize":
            if strip_rule[1].lower() == "keep":
                if strip_rule[2].lower() == "largest":
                    parsed_rules.append(["keep_filesize_largest"])
                    
                elif strip_rule[2].lower() == "smallest":
                    parsed_rules.append(["keep_filesize_smallest"])
                    
                else: RaiseParseException(strip_rule)               
            else: RaiseParseException(strip_rule)
            
            
        elif strip_rule[0].lower() == "covers":
            if strip_rule[1].lower() == "keep":
                if strip_rule[2].lower() == "some":
                    parsed_rules.append(["keep_covers_all","False"])
                    
                elif strip_rule[2].lower() == "all":
                    parsed_rules.append(["keep_covers_all","True"])
                    
                else: RaiseParseException(strip_rule)               
            else: RaiseParseException(strip_rule)
                
        elif strip_rule[0].lower() in ["filename", "filepath", "tags", "notes"]:
            if strip_rule[1].lower() == "keep":
                parsed_rules.append(["keep_with_word",strip_rule[2],(index_dict[strip_rule[0]],)])
                
            elif strip_rule[1].lower() == "remove":
                parsed_rules.append(["remove_with_word",strip_rule[2],(index_dict[strip_rule[0]],)])  # tricky ... must be a list and a list of integers as given by global variables FILENAME, FILEPATH...
                
            else: RaiseParseException(strip_rule)
        
        elif strip_rule[0].lower() == "text":
            if strip_rule[1].lower() == "keep":
                parsed_rules.append(["keep_with_word",strip_rule[2],(FILENAME, FILEPATH, TAGS, NOTES)])
                
            elif strip_rule[1].lower() == "remove":
                parsed_rules.append(["keep_with_word",strip_rule[2],(FILENAME, FILEPATH, TAGS, NOTES)])
                
            else: RaiseParseException(strip_rule)
            
        else:
            RaiseParseException(strip_rule)
            
			
    if VERBOSE:
        logfile.write('\nParsed rules:\n\n')
        for rule in parsed_rules:
            logfile.write('\t\t'+str(rule)+'\n')
    logfile.write('\n============= End of rules parsing ======================================\n\n\n\n')  
    
    return parsed_rules
    
def RaiseParseException(rule):
    wrong_rule = ""
    for i in rule:
        wrong_rule = wrong_rule + " " + i 
    raise NoRulesFileException('Rule "'+ wrong_rule.upper() +'" could not be parsed')
    return

class NoRulesFileException(Exception):
        pass
        
