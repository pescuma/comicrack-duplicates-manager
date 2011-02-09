##########
#
#   DEFINITIONS


import re
import clr
import System
import System.IO
from System.IO import Path, Directory, File, FileInfo



VERSION= "0.1"

print __file__
SCRIPTDIRECTORY = __file__[0:-len("constants.py")]
RULESFILE = Path.Combine(SCRIPTDIRECTORY, "dmrules.dat")
LOGFILE = Path.Combine(SCRIPTDIRECTORY, "logfile.log")
(SERIES,NUMBER,VOLUME,FILENAME,PAGECOUNT,FILESIZE,ID,CVDB_ID,FILEPATH,TAGS,BOOK) = range(11)
C2C_NOADS_GAP = 5

VERBOSE = False

#
#
###########
