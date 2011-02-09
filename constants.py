##########
#
#   DEFINITIONS


import re
import clr
import System
import System.IO
from System.IO import Path, Directory, File, FileInfo

#
############   DON'T MODIFY THESE
#

VERSION= "0.1"

SCRIPTDIRECTORY = __file__[0:-len("constants.py")]
RULESFILE = Path.Combine(SCRIPTDIRECTORY, "dmrules.dat")
LOGFILE = Path.Combine(SCRIPTDIRECTORY, "logfile.log")
(SERIES,NUMBER,VOLUME,FILENAME,PAGECOUNT,FILESIZE,ID,CVDB_ID,FILEPATH,TAGS,BOOK) = range(11)

#
#############   THESE VARIABLES CAN BE DEFINED BY USER
#

C2C_NOADS_GAP = 5           # Difference of pages between c2c and noads
VERBOSE = False             # Logging level (true/false)

DUPESDIRECTORY = Path.Combine("C:","__dupes__")

#
#
###########