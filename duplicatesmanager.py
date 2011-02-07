"""
duplicatesmanager.py

Author: Perezmu

Copyright Perezmu 2011. 

Icon -> created from http://findicons.com/icon/25565/cancel & http://findicons.com/icon/16770/copy#
"""

#### Add references to so many people


#########
#
#    Import section

import re
import clr
import System
import System.IO
from System.IO import Path, Directory, File, FileInfo

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import DialogResult, MessageBox

from BookWrapper import *
'''BookWrapper by XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''

# from utils import convert_bytes

#
#
##########

'''----------------------------------------------------------'''

##########
#
#   DEFINITIONS


SCRIPTDIRECTORY = __file__[0:-len("duplicatesmanager.py")]
RULESSFILE = Path.Combine(SCRIPTDIRECTORY, "dmrules.dat")
(SERIES,NUMBER,VOLUME,FILENAME,PAGECOUNT,FILESIZE,ID,CVDB_ID,FILEPATH) = range(9)

#
#
###########

'''---------------------------------------------------------'''


############
#
#   MAIN FUNCTION

#@Name DuplicatesManager
#@Hook Books
#@Image duplicatesmanager.png
def DuplicatesManager(books):
    
    ''' exporting temporary to a file '''
    
    csvfile = open(Path.Combine(SCRIPTDIRECTORY, 'comicslist.csv'),'w')
    
    csvfile.write("b.CVDB_ID, b.Series, b.Number, b.Volume, b.FileName, b.PageCount, b.FileSize, b.ID \n")
    
    for book in books:
        
        b = BookWrapper(book)
        csvfile.write(str(b.CVDB_ID) +", "+ b.Series +", " + b.Number + ", " + b.Volume +", " + b.FileName + ", " + str(b.PageCount) + ", " + str(b.FileSize/1048576.0) + ", " + str(b.ID) +"\n")
        
        #print "b.Series = " + b.Series + "\n"
        #print "b.Number = " + b.Number + "\n"
        #print "b.FileName = " + b.FileName + "\n"
        #print "b.FilePath = " + b.FilePath + "\n"
        #print "b.FileSize = " + str(b.FileSize/1048576.0) + "\n"
        #print "b.ID = " + str(b.ID) + "\n"
        #print "b.CVDB_ID = " + str(b.CVDB_ID) + "\n"
        #print "b.PageCount = " + str(b.PageCount) + "\n"
        #print "======================================================="
        #
                
    csvfile.close()
	#try:
 #           rules = LoadRules()
	#		
	#	# First we need to identify groups of duplicate files - 
	#	# dupes are identified if 
	#	#	  (i) belong to same series
	#	#	 (ii) same format
	#	#	(iii) same volume | same year (if one of them is empty in one of the comics)
	#	#	 (iv) same issue number
	#	#
	#	#	or same CVDB tag!!!!!
	#	
	#	
	#		
	#	# raised exception due to missing rules file	
	#except NoRulesFileException:
 #           MessageBox.Show(errors, "Missing Rules File", MessageBoxButtons.OK, MessageBoxIcon.Error)
 #           print NoRulesFileException
	#	
	#except Exception, ex:
 #           print "The following error occured"
 #           print Exception
 #           print str(ex)
    return
    
def LoadRules():
    rules = None
    if File.Exists(RULESFILE):
	f = open(RULESSFILE, 'r')
	rules = f.readlines()
	f.close()
    else:
	raise NoRulesFileException('Rules File (dmrules.dat) could not be found in the script directory ('+ SCRIPTDIRECTORY +')')
    return rules

#
#
###############
