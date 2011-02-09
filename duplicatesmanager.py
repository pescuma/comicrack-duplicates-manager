#####################################################################################################
##
##	duplicatesmanager.py
##
##	Author: perezmu
##
##	Copyleft perezmu 2011. 
##
##	Icon -> created from http://findicons.com/icon/25565/cancel & http://findicons.com/icon/16770/copy#
##
######################################################################################################

#### TODO: Add references to so many people


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
from BookWrapper import *
from utilsbycory import cleanupseries
from processfunctions import *

from constants import *

#from process_dupes import *

'''TODO: BookWrapper by XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''

# from utils import convert_bytes

#
#
##########

##'''----------------------------------------------------------'''
##
############
###
###   DEFINITIONS
##
##
##VERSION= "0.1"
##
##SCRIPTDIRECTORY = __file__[0:-len("duplicatesmanager.py")]
##RULESFILE = Path.Combine(SCRIPTDIRECTORY, "dmrules.dat")
##LOGFILE = Path.Combine(SCRIPTDIRECTORY, "logfile.log")
##(SERIES,NUMBER,VOLUME,FILENAME,PAGECOUNT,FILESIZE,ID,CVDB_ID,FILEPATH,TAGS,BOOK) = range(11)
##C2C_NOADS_GAP = 5
##
##VERBOSE = False
##
###
###
#############
##
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
        
        b = BookWrapper(book)
        comiclist.append((cleanupseries(b.Series),b.Number,b.Volume,b.FileName,b.PageCount,b.FileSize/1048576.0,b.ID,b.CVDB_ID,b.FilePath,book.Tags,book))

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
        MessageBox.Show('ERROR: '+ str(ex), "Missing Rules File", MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
        logfile.write('ERROR: Rules file not found (dmrules.dat) in script directory\n')
        print NoRulesFileException
	
    except Exception, ex:
        logfile.write('ERROR: '+ str(Exception) +' -> '+str(ex)+'\n')
        print "The following error occured"
        print Exception
        print str(ex)
        
        
    ###################### TEST ########################################
        
    for i in range(len(dupe_groups)):

        t_group = dupe_groups[i][:]

        if len(t_group)>1:   # process group only if there is more than one comic
           t_group = keep_pagecount_smallest(t_group, logfile)          
        dupe_groups[i] = t_group[:]

    #temp_groups = dupe_groups[:]
    #for group in temp_groups:
    #    if len(group) == 1: dupe_groups.remove(group)
    #del temp_groups
    #
    #if len(dupe_groups)>=1:
    #    print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'

    #
    #   End of Main Loop
    #
    ###########################################################

#### Garbage collecting

    del  dupe_groups
    logfile.close()
    
    return


#### ============================================================================================================================
    
def LoadRules(logfile):

    rules = ""
    
    if File.Exists(RULESFILE):
        f = open(RULESFILE, 'r')
        rules = f.readlines()
        f.close()
        
        logfile.write('\n\n============= Beginning rules parsing ==================================\n\n')        	
        logfile.write('Successfully loaded the following rules: \n\n')
        for rule in rules:
            logfile.write('\t'+rule)
        logfile.write('\n')
        logfile.write('\n============= End of rules parsing ======================================\n\n\n\n')        	
        
    else:
        raise NoRulesFileException('Rules File (dmrules.dat) could not be found in the script directory ('+ SCRIPTDIRECTORY +')')
    return rules


	
def __cleanup_series(series_name):
    # All of the symbols below cause inconsistency in title searches
    series_name = series_name.lower()
    series_name = series_name.replace('.', '')
    series_name = series_name.replace('_', ' ')
    series_name = series_name.replace('-', ' ')
    series_name = series_name.replace("'", ' ')
    series_name = re.sub(r'\b(vs\.?|versus|and|or|the|an|of|a|is)\b','', series_name)
    series_name = re.sub(r'giantsize', r'giant size', series_name)
    series_name = re.sub(r'giant[- ]*sized', r'giant size', series_name)
    series_name = re.sub(r'kingsize', r'king size', series_name)
    series_name = re.sub(r'king[- ]*sized', r'king size', series_name)
    series_name = re.sub(r"directors", r"director's", series_name)
    series_name = re.sub(r"\bvolume\b", r"\bvol\b", series_name)
    series_name = re.sub(r"\bvol\.\b", r"\bvol\b", series_name)

   #series_name = re.sub(r'gijoe', r'gi joe', series_name)
   
    series_name = re.sub(r' *', r'', series_name)

   # try to expand single number
   # words, and if that fails, try to contract them.
   # orig_series_name = series_name
   # if alt_b:
      # series_name = utils.convert_number_words(series_name, True)
   # if alt_b and series_name == orig_series_name:
      # series_name = utils.convert_number_words(series_name, False)
      
   # # strip out punctuation
   # word = re.compile(r'[\w]{1,}')
   # series_name = ' '.join(word.findall(series_name))
   
    return series_name
   



###################################################################################################
##
### ================ PAGECOUNT FUNCTIONS ==========================================================
##
##
##def keep_pagecount_noads(dgroup, logfile):
##    ''' Keeps from the 'group' the ones that seem to be 'noads' (less pages)'''
##    
##    logfile.write('_________________KEEP_PAGECOUNT_NOADS______________\n')
##
##    to_keep = []
##    to_remove =[]
##
##    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=False) # sorts by filesize of covers
##           
##    i=0                               #keeps the first one
##    to_keep.append(by_size[i])
##    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
##           
##    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) < (int(by_size[i][PAGECOUNT]) + C2C_NOADS_GAP)):
##            to_keep.append(by_size[i+1])
##            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n')
##            i = i+1
##    for j in range (i+1,len(by_size)):
##        to_remove.append(by_size[j])
##        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
##            
##    delcomics(to_remove)    
##    dgroup = to_keep[:]
##    
##    return dgroup
##
##
##def keep_pagecount_c2c(dgroup, logfile):
##    ''' Keeps from the 'group' the ones that seem to be 'noads' (less pages)'''
##    
##    logfile.write('_________________KEEP_PAGECOUNT_C2C______________\n')
##
##    to_keep = []
##    to_remove = []
##
##    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=True) # sorts by filesize of covers
##           
##    i=0                               #keeps the first one
##    to_keep.append(by_size[i])
##    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
##         
## 
##    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) > (int(by_size[i][PAGECOUNT]) - int(C2C_NOADS_GAP))):
##            to_keep.append(by_size[i+1])
##            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n') 
##            i = i+1
##    for j in range (i+1,len(by_size)):
##        to_remove.append(by_size[j])
##        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
##            
##    delcomics(to_remove)
##    dgroup = to_keep[:]
##    
##    return dgroup
##
##
##def keep_pagecount_largest(dgroup, logfile):
##    ''' Keeps from the 'group' the one with most pages'''
##    
##    logfile.write('_________________KEEP_PAGECOUNT_MOST______________\n')
##
##    to_keep = []
##    to_remove = []     
##
##    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=True) # sorts by number of pages
##
##    i=0                               #keeps the first one
##    to_keep.append(by_size[i])
##    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
##    
##    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) == (int(by_size[i][PAGECOUNT]))):
##            to_keep.append(by_size[i+1])
##            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n') 
##            i = i+1
##    for j in range (i+1,len(by_size)):
##        to_remove.append(by_size[j])
##        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
##                      
##    
##    delcomics(to_remove)
##    dgroup = to_keep[:]
##    
##    return dgroup
##
##
##def keep_pagecount_smallest(dgroup, logfile):
##    ''' Keeps from the 'group' the one with less pages'''
##    
##    logfile.write('_________________KEEP_PAGECOUNT_LESS______________\n')
##    
##    to_keep =[]
##    to_remove = []  
##    
##    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=False) # sorts by number of pages
##                         
##    i=0                               #keeps the first one
##    to_keep.append(by_size[i])
##    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
##    
##    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) == (int(by_size[i][PAGECOUNT]))):
##            to_keep.append(by_size[i+1])
##            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n') 
##            i = i+1
##    for j in range (i+1,len(by_size)):
##        to_remove.append(by_size[j])
##        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
##                      
##    
##    delcomics(to_remove)
##    dgroup = to_keep[:]
##    return dgroup
##
##
#####################################################################################################


def delcomics(comicslist):
    return


####################################################

class NoRulesFileException(Exception):
	pass
