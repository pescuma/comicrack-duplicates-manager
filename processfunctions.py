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

def keep_pagecount_noads(options, cr, dgroup, logfile):
    ''' Keeps from the 'group' the ones that seem to be 'noads' (less pages)
            dgroup -> list of duplicate comics
            logfile -> file object    '''
    
    logfile.write('_________________KEEP_PAGECOUNT_NOADS______________\n')

    to_keep = []
    to_remove =[]

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[PAGECOUNT], reverse=False) # sorts by filesize of covers
   
    for comic in dgroup:
        if comic[PAGECOUNT] <= options["coverpages"]:
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
            
    deletecomics(options, cr,to_remove, logfile)    
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_c2c(options, cr, dgroup, logfile):
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
         
 
    while (i<len(by_size)-1) and (int(by_size[i+1][PAGECOUNT]) > (int(by_size[i][PAGECOUNT]) - int(options["c2c_noads_gap"]))):
            to_keep.append(by_size[i+1])
            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][PAGECOUNT])+')\n') 
            i = i+1
    for j in range (i+1,len(by_size)):
        to_remove.append(by_size[j])
        logfile.write('removing... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][PAGECOUNT])+')\n')
            
    if to_remove != []: deletecomics(options, cr,to_remove, logfile)
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_largest(options, cr, dgroup, logfile):
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
                      
    
    if to_remove != []: deletecomics(options, cr,to_remove, logfile)
    dgroup = to_keep[:]
    
    return dgroup


def keep_pagecount_smallest(options, cr, dgroup, logfile):
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
                      
    
    if to_remove != []: deletecomics(options, cr,to_remove, logfile)
    dgroup = to_keep[:]
    return dgroup

    
def keep_pagecount_fileless(options, cr, dgroup, logfile):
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
        if to_remove != []: deletecomics(options, cr,to_remove, logfile)
    else:
        for comic in to_remove:
            logfile.write('keeping... '+ comic[FILENAME]+' (pages '+str(comic[PAGECOUNT])+')\n')
            
            
    del to_keep
    del to_remove
    
    return dgroup

    
def remove_pagecount_fileless(options, cr, dgroup, logfile):
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
    
    if to_remove != []: deletecomics(options, cr,to_remove, logfile)
        
    dgroup = to_keep[:]  
    
    return dgroup

    
# =================== FILESIZE FUNCTIONS ========================================================

def keep_filesize_largest(options, cr, percentage, dgroup, logfile):
    ''' Keeps from the 'group' the largest comic
            dgroup -> list of duplicate comics
            logfile -> file object    '''    
            
    logfile.write('_________________KEEP_FILESIZE_LARGEST___' + percentage + '%___________\n')


    by_size = sorted(dgroup, key=lambda dgroup: dgroup[FILESIZE], reverse=True) # sorts by filesize of covers
    largest = by_size[0]
    
    if percentage == 0:
        def IsToKeep(comic):
            return comic == largest
        
    else:
        min_size = largest[FILESIZE] * (1 - percentage/100.0)
        
        def IsToKeep(comic):
            return comic[FILESIZE] >= min_size
            
    process_dups(options, cr, IsToKeep, [FILESIZE], dgroup, logfile)

    return dgroup


def keep_filesize_smallest(options, cr, percentage, dgroup, logfile):
    ''' Keeps from the 'group' the smallest comic
            dgroup -> list of duplicate comics
            logfile -> file object    '''  
    
    logfile.write('_________________KEEP_FILESIZE_SMALLEST__' + percentage + '%____________\n')


    by_size = sorted(dgroup, key=lambda dgroup: dgroup[FILESIZE], reverse=False) # sorts by filesize of covers
                         
    # keep fileless
    for comic in by_size:
        if comic[PAGECOUNT] == 0:
            by_size.remove(comic)

    
    if len(by_size) < 1:
        # Keep all because they are all fileless
        def IsToKeep(comic):
            return True 
    
    elif percentage == 0:
        smallest = by_size[0]
        
        def IsToKeep(comic):
            return comic == smallest or comic[PAGECOUNT] == 0 
        
    else:
        smallest = by_size[0]
        max_size = smallest[FILESIZE] * (1 + percentage/100.0)
        
        def IsToKeep(comic):
            return comic[FILESIZE] <= max_size
            
    return process_dups(options, cr, IsToKeep, [FILESIZE, PAGECOUNT], dgroup, logfile)

    
    
# =================== COVERS FUNCTIONS ============================================================    

def keep_covers_all(options, cr, option, dgroup, logfile):
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
    
    if to_remove != []: deletecomics(options, cr,to_remove, logfile)
    
    del with_covers
    del to_keep
    del to_remove

    return dgroup



# =================== WORD SEARCH FUNCTIONS ========================================================    

def fix_words_for_testing(words):
    wordlist = []
    
    for word in words:
        word = word.lower()
    
        ''' some common substitutions .... more can be added '''
        if word in ('c2c', 'ctc', 'fiche'): 
            wordlist.append(['c2c', 'ctc', 'fiche'])
        elif word in ('noads'): 
            wordlist.append(['noads', 'no ads'])
        elif word in ('(f)', 'fixed'): 
            wordlist.append(['(f)', 'fixed'])
        elif word in ('(f)', 'fiche'): 
            wordlist.append(['(f)', 'fiche'])
        elif word in ('zip','cbz'): 
            wordlist.append(['zip','cbz'])
        elif word in ('rar','cbr'): 
            wordlist.append(['rar','cbr'])
        else:
            wordlist.append(cleanupseries(word))
    
    return wordlist


def keep_with_words(options, cr, words, items, dgroup, logfile):
    ''' Removes from the 'group' all comics that do not include any of the 'words'
        in the fields 'item'
            dgroup -> list of duplicate comics
            logfile -> file object
            words -> text strings to be searched
            items -> LIST of fields to search in'''

    logfile.write('_________________KEEP_WITH_WORDS______' + str(words) + '________\n')

    wordlist = fix_words_for_testing(words)

    def IsToKeep(comic):
        searchstring = ""
        for item in items:
            searchstring = searchstring + " " + cleanupseries(comic[item])
            ''' adds all search strings together '''
        
        for word in wordlist:
            if searchstring.find(word) != -1:    #word found
                return True
        
        return False
        
    return process_dups(options, cr, IsToKeep, (FILENAME), dgroup, logfile)


def remove_with_words(options, cr, words, items, dgroup, logfile):
    ''' Removes from the 'group' all comics that do not include any of the 'words'
        in the fields 'item'
            dgroup -> list of duplicate comics
            logfile -> file object
            words -> text strings to be searched
            items -> LIST of fields to search in'''
            

    logfile.write('_________________REMOVE_WITH_WORDS______' + str(words) + '________\n')

    wordlist = fix_words_for_testing(words)

    def IsToKeep(book):
        searchstring = ""
        for item in items:
            searchstring = searchstring + " " + cleanupseries(comic[item])
            ''' adds all search strings together '''
        
        for word in wordlist:
            if searchstring.find(word) != -1:    #word found
                return False
        
        return True
        
    return process_dups(options, cr, IsToKeep, [], dgroup, logfile)
    

    
###################################################################################################

# ================ BASE FUNCTION TO HANDLE THE DUPS ================================================

def process_dups(options, cr, test_to_keep, fields, dgroup, logfile):
    ''' Removes from the 'group' all comics that test_to_keep('comic') returns false
            dgroup -> list of duplicate comics
            logfile -> file object
            test_to_keep -> function to do the tesing'''

    to_keep = []
    to_remove = []
    
    for comic in dgroup:
        if test_to_keep(comic):
            if comic not in to_keep: 
                to_keep.append(comic)
            break
        
        if comic not in to_keep: 
            to_remove.append(comic)

    # Make sure at least 1 book remains!!!!
    if len(to_keep) < 0:
        logfile.write('Filter would remove all items, so it will be ignored\n')
        to_keep = dgroup[:]
        to_remove = []

    # Log comic actions    
    for comic in dgroup:
        if comic in to_keep:
            logfile.write('keeping... ')
        else:
            logfile.write('removing... ')
        
        logfile.write(str(comic[FILENAME]))
        
        if len(fields) > 0:
            logfile.write(' (')
            for i in range(len(fields)):
                if i > 0:
                    logfile.write(' ')
                f = fields[i]
                logfile.write(names[f] + '=' + str(comic(f)))
            logfile.write(')')
                
        logfile.write('\n')
    
    # Delete boolks
    if to_remove != []: 
        deletecomics(options, cr, to_remove, logfile)

    del to_remove
    
    return to_keep


# ================ DELETE COMICS FUNCTION ==========================================================

def deletecomics(options, cr, deletelist, logfile):
    ''' Moves or deletes the specified comics and removes them from the library'''
    
    ''' Mostly ripped form StonePawn's Libary Organizer script'''
    
    if not Directory.Exists(DUPESDIRECTORY):
        try:
            Directory.CreateDirectory(DUPESDIRECTORY)
        except Exception, ex:
                MessageBox.Show('ERROR: '+ str(ex), "ERROR creating dump directory" + DUPESDIRECTORY, MessageBoxButtons.OK, MessageBoxIcon.Exclamation)
                logfile.write('ERROR: '+str(ex)+'\n')
                print Exception
    
    for comic in deletelist:
        
        if options["movefiles"]: 
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
        
        if options["removefromlib"]:
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
        CleanDirectories(parent)
