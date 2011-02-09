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
from utilsbycory import cleanupseries, convertnumberwords

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
            
    if to_remove != []: deletecomics(to_remove, logfile)    
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
            
    if to_remove != []: deletecomics(to_remove, logfile)
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
                      
    
    if to_remove != []: deletecomics(to_remove, logfile)
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
                      
    
    if to_remove != []: deletecomics(to_remove, logfile)
    dgroup = to_keep[:]
    return dgroup

	
def keep_pagecount_fileless(dgroup, logfile):
    ''' Keeps only fileless comics          
		dgroup -> list of duplicate comics
        logfile -> file object    '''
    
    logfile.write('_________________REMOVE_FILELESS_ECOMICS_______________\n')

    to_keep = dgroup[:]
	to_remove = []

    for comic in dgroup:
        if comic[FILENAME] !== "Fileless":
			to_remove.append(comic)
			to_keep.remove(comic)
        
    if len(to_keep) > 0:
            dgroup = to_keep[:]
			if to_remove != []: deletecomics(to_remove, logfile)
    
	del to_keep
	del to_remove
	
    return dgroup

	
def remove_pagecount_fileless(dgroup, logfile):
    ''' Removes fileless comics          
		dgroup -> list of duplicate comics
        logfile -> file object    '''
    
    logfile.write('_________________REMOVE_FILELESS_ECOMICS_______________\n')

    to_keep = dgroup[:]
	to_remove = []

    for comic in dgroup:
        if comic[FILENAME] == "Fileless":
            to_keep.remove(comic)
			to_remove.append(comic)
        
    if len(to_keep) > 0:
            dgroup = to_keep[:]
			if to_remove != []: deletecomics(to_remove, logfile)
    
    return dgroup


	
# =================== FILESIZE FUNCTIONS ========================================================

def keep_filesize_largest(dgroup, logfile):
    ''' Keeps from the 'group' the largest comic
			dgroup -> list of duplicate comics
			logfile -> file object    '''    
			
    logfile.write('_________________KEEP_FILESIZE_MOST______________\n')


    to_remove = []

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[item], reverse=True) # sorts by filesize of covers
                         
    for comic in by_size[1:]:
        dgroup.remove(comic)
		to_remove.append(comic)
        logfile.write('removed... '+ comic[FILENAME]+'(size '+ str(comic[FILESIZE]) +')\n')

    logfile.write('keeping... '+ by_size[0][3]+'(size '+ str(by_size[0][FILESIZE])+')\n')
	
	if to_remove != []: deletecomics(to_remove, logfile)
    del by_size
	
    return dgroup


def keep_filesize_smallest(dgroup, logfile):
    ''' Keeps from the 'group' the smallest comic
			dgroup -> list of duplicate comics
			logfile -> file object    '''  
    
    logfile.write('_________________KEEP_FILESIZE_MOST______________\n')


    to_remove = []     

    by_size = sorted(dgroup, key=lambda dgroup: dgroup[item], reverse=False) # sorts by filesize of covers
                         
    for comic in by_size[1:]:
        dgroup.remove(comic)
		to_remove.append(comic)
        logfile.write('removed... '+ comic[FILENAME]+'(size '+str(comic[FILESIZE])+')\n')

    logfile.write('keeping... '+ by_size[0][3]+'(size '+str(by_size[0][FILESIZE])+')\n') 
    
	if to_remove != []: deletecomics(to_remove, logfile)
    del by_size
	
    return dgroup	

	
	
# =================== COVERS FUNCTIONS ============================================================	

def keep_covers_most(option, dgroup, logfile):
    ''' Keeps from the 'group' the comics with largest number of '(n covers)' in the file name
			dgroup -> list of duplicate comics
			logfile -> file object
			option -> boolean: True means all comics with or without 'covers' are considered, meaning that
				if there is a single comic with 'covers' the rest will be deleted. False means
				that only those comics with the 'covers' word will be considered in the process        '''
    
    logfile.write('_________________KEEP_COVERS_MOST______________\n')

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
				to_remove.append(comics)
				logfile.write('removed... '+ comic[FILENAME]+'\n')
            else:
				# logfile.write('keeping... '+ comic[FILENAME]+'\n')
				to_keep.append(comic)

        for comic in to_keep:
            dgroup.append(comic)
            logfile.write('keeping... '+ comic[FILENAME]+'\n')
	
	if to_remove != []: deletecomics(to_remove, logfile)
	
	del with_covers
	del to_keep
	del to_remove

    return dgroup



# =================== WORD SEARCH FUNCTIONS ========================================================	
		
def keep_with_word(word, items, dgroup, logfile):
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
                to_keep.append(comic)
			else:
				to_remove.append(comic)
                
    if len(to_keep)>=1:     # Make sure at least 1 book remains!!!!
        for comic in dgroup:
            if comic in to_keep:
                logfile.write('keeping...'+str(comic[FILENAME])+'\n')
            else:
                logfile.write('removed...'+str(comic[FILENAME])+'\n')
        
		if to_remove != []: deletecomics(to_remove, logfile)
				
        dgroup = to_keep[:]
		

    else:
        for comic in dgroup:
            logfile.write('keeping...'+str(comic[item])+'\n')
    
	del to_keep
	del to_remove
	
    return dgroup


def remove_with_word(word, items, dgroup, logfile):
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
                to_remove.append(comic)
			else:
				to_keep.append(comic)
                           
    if len(to_keep)>=1:     # Make sure at least 1 book remains!!!!
   
        for comic in dgroup:
            if comic in to_keep:
                logfile.write('keeping...'+str(comic[item])+'\n')
            else:
                logfile.write('removed...'+str(comic[item])+'\n')
  
		if to_remove != []: deletecomics(to_remove, logfile)
		
        dgroup = to_keep[:]

    else:					# Else no comic is removed!!!!!
        for comic in dgroup:
            logfile.write('keeping...'+str(comic[item])+'\n')
    
	del to_remove
    del to_keep
       
    return dgroup
	

	
###################################################################################################

# ================ DELETE COMICS FUNCTION ==========================================================

def deletecomics(deletelist, logfile):
	''' Moves or deletes the specified comics and removes them from the library'''
	
	for comic in deletelist:
		logfile.write('DELETED... '+ comic[FILENAME]\n')
	
	return 