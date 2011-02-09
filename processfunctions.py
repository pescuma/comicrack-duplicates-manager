#########
#
#    Import section


import constants

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

from constants import *

#from process_dupes import *

'''TODO: BookWrapper by XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'''

# from utils import convert_bytes

#
#
##########



#################################################################################################

# ================ PAGECOUNT FUNCTIONS ==========================================================


def keep_pagecount_noads(dgroup, logfile):
    ''' Keeps from the 'group' the ones that seem to be 'noads' (less pages)
            dgroup -> list of duplicate comics
            logfile -> file object    '''
    
    logfile.write('_________________KEEP_PAGECOUNT_NOADS______________\n')

    to_keep = []
    to_remove =[]

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=False) # sorts by filesize of covers
           
    i=0                                                                             #keeps the first one
    to_keep.append(by_size[i])
    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
           
    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) < (int(by_size[i][PAGECOUNT]) + C2C_NOADS_GAP)):
            to_keep.append(by_size[i+1])
            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n')
            i = i+1
    for j in range (i+1,len(by_size)):
        to_remove.append(by_size[j])
        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
            
    delcomics(to_remove)    
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_c2c(dgroup, logfile):
    ''' Keeps from the 'group' the ones that seem to be 'noads' (less pages)
            dgroup -> list of duplicate comics
            logfile -> file object    '''
    
    logfile.write('_________________KEEP_PAGECOUNT_C2C______________\n')

    to_keep = []
    to_remove = []

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=True) # sorts by filesize of covers
           
    i=0                               #keeps the first one
    to_keep.append(by_size[i])
    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
         
 
    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) > (int(by_size[i][PAGECOUNT]) - int(C2C_NOADS_GAP))):
            to_keep.append(by_size[i+1])
            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n') 
            i = i+1
    for j in range (i+1,len(by_size)):
        to_remove.append(by_size[j])
        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
            
    delcomics(to_remove)
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_largest(dgroup, logfile):
    ''' Keeps from the 'dgroup' the ones with most pages
            dgroup -> list of duplicate comics
            logfile -> file object    '''
    
    logfile.write('_________________KEEP_PAGECOUNT_MOST______________\n')

    to_keep = []
    to_remove = []     

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=True) # sorts by number of pages

    i=0                               #keeps the first one
    to_keep.append(by_size[i])
    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
    
    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) == (int(by_size[i][PAGECOUNT]))):
            to_keep.append(by_size[i+1])
            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n') 
            i = i+1
    for j in range (i+1,len(by_size)):
        to_remove.append(by_size[j])
        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
                      
    
    delcomics(to_remove)
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_smallest(dgroup, logfile):
    ''' Keeps from the 'group' the one with less pages
            dgroup -> list of duplicate comics
            logfile -> file object    '''
    
    logfile.write('_________________KEEP_PAGECOUNT_LESS______________\n')
    
    to_keep =[]
    to_remove = []  
    
    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=False) # sorts by number of pages
                         
    i=0                               #keeps the first one
    to_keep.append(by_size[i])
    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
    
    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) == (int(by_size[i][PAGECOUNT]))):
            to_keep.append(by_size[i+1])
            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n') 
            i = i+1
    for j in range (i+1,len(by_size)):
        to_remove.append(by_size[j])
        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
                      
    
    delcomics(to_remove)
    dgroup = to_keep[:]
    return dgroup


###################################################################################################


def delcomics(comicslist):
    return


####################################################

class NoRulesFileException(Exception):
	pass
