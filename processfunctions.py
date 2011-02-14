#####################################################################################################
##
##      processfunctions.py - part of duplicatemanager, a script for comicrack
##
##      Author: perezmu
##
##      Copyleft perezmu 2011. 
##
######################################################################################################

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
from dmBookWrapper import *
from utilsbycory import cleanupseries, convertnumberwords

from constants import *

#
#
##########



#################################################################################################


# ================ PAGECOUNT FUNCTIONS ==========================================================

def keep_pagecount_noads(cr, dgroup, logfile):
    ''' Keeps from the 'group' the ones that seem to be 'noads' (less pages)
            dgroup -> list of duplicate comics
            logfile -> file object    '''
    
    logfile.write('_________________KEEP_PAGECOUNT_NOADS______________\n')

    to_keep = []
    to_remove =[]

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=False) # sorts by filesize of covers
   
    for comic in dgroup:
        if comic[PAGECOUNT] <= 5:
            by_size.remove(comic)
            to_keep.append(comic)
            if comic[PAGECOUNT] == 0: logfile.write('skipping... '+ comic[SERIES]+' #' + comic[NUMBER] + ' (fileless)\n')
            else: logfile.write('skipping... '+ comic[FILENAME]+' #' + comic[NUMBER] +' (pages '+str(comic[PAGECOUNT])+')\n')
            
    i=0                                                                             #keeps the first one
    to_keep.append(by_size[i])
    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
    
       
    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) < (int(by_size[i][PAGECOUNT]) + C2C_NOADS_GAP)):
            to_keep.append(by_size[i+1])
            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n')
            i = i+1
    for j in range (i+1,len(by_size)):
        to_remove.append(by_size[j])
        logfile.write('removing... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
            
    deletecomics(cr,to_remove, logfile)    
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_c2c(cr, dgroup, logfile):
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
        logfile.write('removing... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
            
    if to_remove != []: deletecomics(cr,to_remove, logfile)
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_largest(cr, dgroup, logfile):
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
        logfile.write('removing... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
                      
    
    if to_remove != []: deletecomics(cr,to_remove, logfile)
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_smallest(cr, dgroup, logfile):
    ''' Keeps from the 'group' the one with less pages
            dgroup -> list of duplicate comics
            logfile -> file object    '''
    
    logfile.write('_________________KEEP_PAGECOUNT_LESS______________\n')
    
    to_keep =[]
    to_remove = []  
    
    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=False) # sorts by number of pages
    
    # remove fileless:
    
    for comic in by_size:
        if comic[PAGECOUNT] == 0:
            by_size.remove(comic)
            logfile.write('keeping... '+ comic[SERIES]+' #' + comic[NUMBER] + ' (fileless)\n') 
                         
    i=0                               #keeps the first one
    to_keep.append(by_size[i])
    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][PAGECOUNT])+')\n')
        
    
    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) == (int(by_size[i][PAGECOUNT]))):
            to_keep.append(by_size[i+1])
            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n') 
            i = i+1
    for j in range (i+1,len(by_size)):
        to_remove.append(by_size[j])
        logfile.write('removing... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
                      
    
    if to_remove != []: deletecomics(cr,to_remove, logfile)
    dgroup = to_keep[:]
    return dgroup

    
def keep_pagecount_fileless(cr, dgroup, logfile):
    ''' Keeps only fileless comics          
        dgroup -> list of duplicate comics
        logfile -> file object    '''
    
    logfile.write('_________________KEEP_FILELESS_ECOMICS_______________\n')

    to_keep = dgroup[:]
    to_remove = []

    for comic in dgroup:
        if comic[FILENAME] != "Fileless":
            to_remove.append(comic)
            to_keep.remove(comic)
            
        
    if len(to_keep) > 0:
        dgroup = to_keep[:]
        for comic in to_keep:
            logfile.write('keeping... '+ comic[SERIES]+' #' + comic[NUMBER] + ' (fileless)\n') 
        for comic in to_remove:
            logfile.write('removing... '+ comic[FILENAME]+' (pages '+str(comic[PAGECOUNT])+')\n')
        if to_remove != []: deletecomics(cr,to_remove, logfile)
    else:
        for comic in to_remove:
            logfile.write('keeping... '+ comic[FILENAME]+' (pages '+str(comic[PAGECOUNT])+')\n')
            
            
    del to_keep
    del to_remove
    
    return dgroup

    
def remove_pagecount_fileless(cr, dgroup, logfile):
    ''' Removes fileless comics          
        dgroup -> list of duplicate comics
        logfile -> file object    '''
    
    logfile.write('_________________REMOVE_FILELESS_ECOMICS_______________\n')

    to_keep = dgroup[:]
    to_remove = []
    fileless_thumb = []
    fileless_nothumb = []
    
    # First separate all fileless
    for comic in dgroup:
          
        if comic[FILENAME] == "Fileless":
            to_keep.remove(comic)
            if comic[BOOK].CustomThumbnailKey == None:
                fileless_nothumb.append(comic)
            else:
                fileless_thumb.append(comic)
            
    if len(to_keep) == 0:                # all are fileless
        if len(fileless_nothumb) == len(dgroup):  # none has custom thumb
            to_keep.append(fileless_nothumb[0])  # keep the first one
            fileless_nothumb.pop(0)
            to_remove = fileless_nothumb[:]
        elif len(fileless_thumb) == 1:    # only one with custom thumb
            to_keep = fileless_thumb[:]
            to_remove = fileless_nothumb[:]
        else:                                # more than one with custom thumb
            to_keep.append(fileless_thumb[0])    #keep the first one
            fileless_thumb.pop(0)
            to_remove = fileless_thumb[:]
            to_remove.extend(fileless_nothumb)
    
    else:               # if there were non fileless, remove all fileless
        to_remove.extend(fileless_thumb)
        to_remove.extend(fileless_nothumb)
    
    
    for comic in fileless_nothumb:
        logfile.write('removing... '+ comic[SERIES]+' #' + comic[NUMBER] + ' (fileless + no cover)\n')  
    for comic in fileless_thumb:
        logfile.write('removing... '+ comic[SERIES]+' #' + comic[NUMBER] + ' (fileless + custom cover)\n')    
    for comic in to_keep:
        logfile.write('keeping... '+ comic[FILENAME]+' (pages '+str(comic[PAGECOUNT])+')\n')
    
    if to_remove != []: deletecomics(cr,to_remove, logfile)
        
    dgroup = to_keep[:]  
    
    return dgroup

    
# =================== FILESIZE FUNCTIONS ========================================================

def keep_filesize_largest(cr, dgroup, logfile):
    ''' Keeps from the 'group' the largest comic
            dgroup -> list of duplicate comics
            logfile -> file object    '''    
            
    logfile.write('_________________KEEP_FILESIZE_LARGEST______________\n')


    to_remove = []

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[FILESIZE], reverse=True) # sorts by filesize of covers
                         
    for comic in by_size[1:]:
        dgroup.remove(comic)
        to_remove.append(comic)
        logfile.write('removing... '+ comic[FILENAME]+'(size '+ str(comic[FILESIZE]) +')\n')

    logfile.write('keeping... '+ by_size[0][FILENAME]+'(size '+ str(by_size[0][FILESIZE])+')\n')
    
    if to_remove != []: deletecomics(cr,to_remove, logfile)
    del by_size
    
    return dgroup


def keep_filesize_smallest(cr, dgroup, logfile):
    ''' Keeps from the 'group' the smallest comic
            dgroup -> list of duplicate comics
            logfile -> file object    '''  
    
    logfile.write('_________________KEEP_FILESIZE_SMALLEST______________\n')


    to_remove = []     

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[FILESIZE], reverse=False) # sorts by filesize of covers
                         
    # keep fileless
    for comic in by_size:
        if comic[PAGECOUNT] == 0:
            by_size.remove(comic)
            logfile.write('keeping... '+ comic[SERIES]+' #' + comic[NUMBER] + ' (fileless)\n') 
                                                  
                         
    for comic in by_size[1:]:
        dgroup.remove(comic)
        to_remove.append(comic)
        logfile.write('removing... '+ comic[FILENAME]+'(size '+str(comic[FILESIZE])+')\n')

    logfile.write('keeping... '+ by_size[0][FILENAME]+'(size '+str(by_size[0][FILESIZE])+')\n') 
    
    if to_remove != []: deletecomics(cr,to_remove, logfile)
    del by_size
    
    return dgroup    

    
    
# =================== COVERS FUNCTIONS ============================================================    

def keep_covers_all(cr, option, dgroup, logfile):
    ''' Keeps from the 'group' the comics with largest number of '(n covers)' in the file name
            dgroup -> list of duplicate comics
            logfile -> file object
            option -> boolean: True means all comics with or without 'covers' are considered, meaning that
                if there is a single comic with 'covers' the rest will be deleted. False means
                that only those comics with the 'covers' word will be considered in the process        '''
    
    logfile.write('_________________KEEP_COVERS_MOST__' + str(option) + '___________\n')

    with_covers = []
    to_keep = [] 
    to_remove = []
                         
    for comic in dgroup:
        searchstring = convertnumberwords(comic[FILENAME],False)
        searchstring = searchstring.replace("(both","(2")
        searchstring = searchstring.lower()

        m = re.search('\((\d*) +covers\)', searchstring)
        if m:
            with_covers.append((comic, int(m.groups(0)[0])))
        else:
            if option == True:
                with_covers.append((comic,1))
            else:
                to_keep.append(comic)

    if with_covers != []:
        dgroup = []
        with_covers = sorted(with_covers, key=lambda to_keep: to_keep[1], reverse=True) # sorts by number of covers
        max = with_covers[0][1] # max number of covers found
            
        for (comic,covers) in with_covers:
            if covers < max:
                with_covers.remove((comic,covers))
                to_remove.append(comic)
                logfile.write('removing... '+ comic[FILENAME]+'\n')
            else:
                # logfile.write('keeping... '+ comic[FILENAME]+'\n')
                to_keep.append(comic)

        for comic in to_keep:
            dgroup.append(comic)
            logfile.write('keeping... '+ comic[FILENAME]+'\n')
    
    if to_remove != []: deletecomics(cr,to_remove, logfile)
    
    del with_covers
    del to_keep
    del to_remove

    return dgroup



# =================== WORD SEARCH FUNCTIONS ========================================================    
        
def keep_with_word(cr, word, items, dgroup, logfile):
    ''' Removes from the 'group' all comics that do not include 'word'
        in the fields 'item'
            dgroup -> list of duplicate comics
            logfile -> file object
            word -> text string to be searched
            items -> LIST of fields to search in'''

    logfile.write('_________________KEEP_WITH_WORD______'+word+'________\n')

    word = word.lower()
    wordlist = [word,]

    ''' some common substitutions .... more can be added '''
    if word in ('c2c', 'ctc', 'fiche'): wordlist = ('c2c', 'ctc', 'fiche')
    if word in ('noads') : wordlist = ('noads', 'no ads')
    if word in ('(f)', 'fixed'): wordlist = ('(f)', 'fixed')
    if word in ('(f)', 'fiche'): wordlist = ('(f)', 'fiche')

    to_keep = []
    to_remove = []
    
    for comic in dgroup:
        searchstring = ""
        for item in items:
            searchstring = searchstring + " " + cleanupseries(comic[item])
        ''' adds all search files together '''
        
        for word in wordlist:
            if searchstring.find(word) != -1:    #word found
                if comic not in to_keep: to_keep.append(comic)
                break
            else:
                if comic not in to_remove: to_remove.append(comic)
                
    if len(to_keep)>=1:     # Make sure at least 1 book remains!!!!
        for comic in dgroup:
            if comic in to_keep:
                logfile.write('keeping...'+str(comic[FILENAME])+'\n')
            else:
                logfile.write('removing...'+str(comic[FILENAME])+'\n')
        
        if to_remove != []: deletecomics(cr,to_remove, logfile)
                
        dgroup = to_keep[:]
        

    else:
        for comic in dgroup:
            logfile.write('keeping...'+str(comic[FILENAME])+'\n')
    
    del to_keep
    del to_remove
    
    return dgroup


def remove_with_word(cr, word, items, dgroup, logfile):
    ''' Removes from the 'group' all comics that do not include 'word'
        in the fields 'item'
            dgroup -> list of duplicate comics
            logfile -> file object
            word -> text string to be searched
            items -> LIST of fields to search in'''
            

    logfile.write('_________________REMOVE_WITH_WORD______'+word+'________\n')

    word = word.lower()
    wordlist = [word,]
    
    ''' some common substitutions .... more can be added '''
    if word in ('c2c', 'ctc', 'fiche'): wordlist = ('c2c', 'ctc', 'fiche')
    if word in ('noads') : wordlist = ('noads', 'no ads')
    if word in ('(f)', 'fixed'): wordlist = ('(f)', 'fixed')
    if word in ('(f)', 'fiche'): wordlist = ('(f)', 'fiche')

    to_keep = []    
    to_remove = []
                            
    for comic in dgroup:
        searchstring = ""
        for item in items:
            searchstring = searchstring + " " + cleanupseries(comic[item])
        ''' adds all search files together '''
        
        for word in wordlist:
            if searchstring.find(word) != -1: # word found
                if comic not in to_remove: to_remove.append(comic)
                break    
            else:
                if comic not in to_keep: to_keep.append(comic)
                    
                
    if len(to_keep)>=1:     # Make sure at least 1 book remains!!!!
   
        for comic in dgroup:
            if comic in to_keep:
                logfile.write('keeping...'+str(comic[item])+'\n')
            else:
                logfile.write('removing...'+str(comic[item])+'\n')
  
        if to_remove != []: deletecomics(cr,to_remove, logfile)
        
        dgroup = to_keep[:]

    else:                    # Else no comic is removing!!!!!
        for comic in dgroup:
            logfile.write('keeping...'+str(comic[item])+'\n')
    
    del to_remove
    del to_keep
       
    return dgroup
    

    
###################################################################################################

# ================ DELETE COMICS FUNCTION ==========================================================

def deletecomics(cr, deletelist, logfile):
    ''' Moves or deletes the specified comics and removes them from the library'''
    
    ''' Mostly ripped form Stonepaw's Libary Organizer script'''
    
    if not Directory.Exists(DUPESDIRECTORY):
        try:
            Directory.CreateDirectory(DUPESDIRECTORY)
        except Exception, ex:
                MessageBox.Show('ERROR: '+ str(ex), "ERROR creating dump directory" + DUPESDIRECTORY, MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
                logfile.write('ERROR: '+str(ex)+'\n')
                print Exception
    
    for comic in deletelist:
        
        if MOVEFILES: 
            fullpath = Path.Combine(DUPESDIRECTORY, comic[FILENAME])
        
           #Check if the file currently exists at all
           
            if comic[FILENAME]!='Fileless' and File.Exists(comic[FILEPATH]):
              #If the book is already in the location we don't have to do anything
              if fullpath == comic[FILEPATH]:
                 
                #print "books path is the same"
                logfile.write("\n\nSkipped moving book " + comic[FILEPATH] + " because it is already located at the calculated path")
                dmCleanDirectories(DirectoryInfo(path))
                
            if comic[FILENAME]!='Fileless' and not File.Exists(fullpath):
                try:
                    File.Move(comic[FILEPATH], fullpath)
                    comic[BOOK].FilePath = fullpath            #update new file path
                except Exception, ex:
                        MessageBox.Show('ERROR: '+ str(ex)+ "while trying to move " + comic[FILENAME], 'MOVE ERROR', MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
                        logfile.write('ERROR: '+str(ex)+'\n')
            else:
                logfile.write('WARNING: '+comic[FILENAME]+' could not be moved\n')
             
            logfile.write('---MOVED... '+ comic[FILENAME]+'\n')
        
        if REMOVEFROMLIB:
            try:
                cr.App.RemoveBook(comic[BOOK])
                logfile.write('---REMOVED FROM LIBRARY... '+ comic[FILENAME]+'\n')
            except:        
                logfile.write('---COULD NOT REMOVE FROM LIBRARY... '+ comic[FILENAME]+'\n')
            
            
    return
            
            
def dmCleanDirectories(directory):
    #Driectory should be a directoryinfo object
    if not directory.Exists:
        return
    if len(directory.GetFiles()) == 0 and len(directory.GetDirectories()) == 0:
        parent = directory.Parent
        directory.Delete()
        dmCleanDirectories(parent)
