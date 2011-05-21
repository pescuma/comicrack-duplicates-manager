#####################################################################################################
##
##      constants.py - part of duplicatemanager, a script for comicrack
##
##      Author: perezmu
##
##      Copyleft perezmu 2011. 
##
######################################################################################################



##########
#
#   DEFINITIONS


import re
import clr
import System
import System.IO
from System.IO import Path, Directory, File, FileInfo

#
#############   **** USER CONFIGURABLE VARIABLES ***    ###########################################
#
#          see http://code.google.com/p/comicrack-duplicates-manager/wiki/UserConfiguration for details
#
#          These may also be set in the "dmrules.dat" rules file using this syntax:  "@ OPTION VALUE". Values
#           found in the "dmrules.dat" file override the defaults set in this file.


MOVEFILES = False
REMOVEFROMLIB = False
UPDATEINFO = False

DUPESDIRECTORY = Path.Combine("C:\\","__dupes__")

C2C_NOADS_GAP = 5          # Difference of pages between c2c and noads
SIZEMARGIN = 0             # Preserve comics within sizemargin % size
COVERPAGES = 4             # Minimal number of pages to be considered "covers only"
 
VERBOSE = False            # Logging level (true/false)
DEBUG = False              # Logging level (true/false)


#
############   DON'T MODIFY BELOW THIS LINE ######
#

VERSION= "0.8"

SCRIPTDIRECTORY = __file__[0:-len("constants.py")]
RULESFILE = Path.Combine(SCRIPTDIRECTORY, "dmrules.dat")
LOGFILE = Path.Combine(DUPESDIRECTORY, "logfile.log")
(SERIES,NUMBER,VOLUME,FILENAME,PAGECOUNT,FILESIZE,ID,CVDB_ID,FILEPATH,TAGS,NOTES,FILETYPE,SCAN,BOOK) = range(14)
FIELD_NAMES = ['series','number','volume','filename','pages','size','id','cvdb_id','path','tags','notes','type','scan','book']
FIELDS_TO_UPDATE_INFO = [
        [ 'AlternateCount', lambda x: int(x) ],
        [ 'AlternateNumber', lambda x: x ],
        [ 'AlternateSeries', lambda x: x ],
        [ 'Count', lambda x: int(x) ],
        [ 'Title', lambda x: x ],
]

#
#
###########