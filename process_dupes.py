#from utils_noiron import __cleanup_series, convert_number_words

import re

(SERIES,NUMBER,VOLUME,FILENAME,PAGECOUNT,FILESIZE,ID,CVDB_ID,FILEPATH,BOOK) = range(10)
C2C_NOADS_GAP = 5


#def keep_with_word(word, item, dgroup, logfile):
#    ''' Removes from the 'group' all comics that do not include 'word'
#        in the field 'item' '''
#
#    logfile.write('_________________KEEP_WITH_WORD______'+word+'________\n')
#
#    word = word.lower()
#    wordlist = [word,]
#
#    if word in ('c2c', 'ctc', 'fiche'): wordlist = ('c2c', 'ctc', 'fiche')
#    if word in ('noads') : wordlist = ('noads', 'no ads')
#    if word in ('(f)', 'fixed'): wordlist = ('(f)', 'fixed')
#    if word in ('(f)', 'fiche'): wordlist = ('(f)', 'fiche')
#
#    to_keep = []            # This is to copy the contents of a list to another,
#                            # 'cause copyng a=b makes them the same list and
#                            # modifying on modifies the other.
#    #print dgroup
#    #print to_keep
#    
#    for comic in dgroup:
#        searchstring = __cleanup_series(comic[item],False)
#
#        
#        for word in wordlist:
#            if searchstring.find(word) != -1:
#                if comic not in to_keep:  to_keep.append(comic)
#
#
#                
#    if len(to_keep)>=1:     # Make sure at least 1 book remains!!!!
#        #logging
#        for comic in dgroup:
#            if comic in to_keep:
#                logfile.write('keeping...'+str(comic[item])+'\n')
#            else:
#                logfile.write('removed...'+str(comic[item])+'\n')
#        #end logging
#        dgroup = to_keep[:]
## logging
#    else:
#        for comic in dgroup:
#            logfile.write('keeping...'+str(comic[item])+'\n')
##end logging
#        
### TO DO: EFFECTIVELY REMOVE COMICS (MOVE TO NEW LOCATION) FROM HDD AND LIBRARY
#    
#    return dgroup
#
#
## ========================================================================
#
#def remove_with_word(word, item, dgroup, logfile):
#    ''' Removes from the 'group' all comics that do include 'word'
#        in the field 'item' '''
#
#    logfile.write('_________________REMOVE_WITH_WORD______'+word+'________\n')
#
#    word = word.lower()
#    wordlist = [word,]
#
#    if word in ('c2c', 'ctc', 'fiche'): wordlist = ('c2c', 'ctc', 'fiche')
#    if word in ('noads') : wordlist = ('noads', 'no ads')
#    if word in ('(f)', 'fixed'): wordlist = ('(f)', 'fixed')
#    if word in ('(f)', 'fiche'): wordlist = ('(f)', 'fiche')
#
#    to_keep = dgroup[:]     # This is to copy the contents of a list to another,
#                            # 'cause copyng a=b makes them the same list and
#                            # modifying on modifies the other.
#    to_remove = []
#                            
#    for comic in dgroup:
#        searchstring = __cleanup_series(comic[item],False)
#        
#        for word in wordlist:
#            if searchstring.find(word) != -1:
#                if comic not in to_remove:  to_remove.append(comic)
#                           
#    if (len(to_keep) - len(to_remove))>=1:     # Make sure at least 1 book remains!!!!
#        for comic in to_remove:
#            to_keep.remove(comic)
#          
#        #logging
#        for comic in dgroup:
#            if comic in to_keep:
#                logfile.write('keeping...'+str(comic[item])+'\n')
#            else:
#                logfile.write('removed...'+str(comic[item])+'\n')
#        #end logging    
#        dgroup = to_keep[:]
#
### TO DO: EFFECTIVELY REMOVE COMICS (MOVE TO NEW LOCATION) FROM HDD AND LIBRARY
#        
#    del to_remove
#    del to_keep
#       
#    return dgroup
#
#
##print 'remove from this group___________________________'
##        group=filter(lambda x:x not in remove,group)
#
#
## ========================================================================
#
#
#
#
#
#
#
#
#
#def keep_covers_most(option, item, dgroup, logfile):
#    ''' Keeps from the 'group' the comics with largest number of '(n covers)'
#        in the field 'item'
#
#        'word' is boolean: True means all comics with or without 'covers' are considered, meaning that
#        if there is a single comic with 'covers' the rest will be deleted. False means
#        that only those comics with the 'covers' word will be considered in the process        '''
#    
#    logfile.write('_________________KEEP_COVERS_MOST______________\n')
#
#    with_covers = []
#    to_keep = []     
#                         
#    for comic in dgroup:
#        searchstring = convert_number_words(comic[item],False)
#        searchstring = searchstring.replace("(both","(2")
#        searchstring = searchstring.lower()
#
#        m = re.search('\((\d*) +covers\)', searchstring)
#        if m:
#            with_covers.append((comic, int(m.groups(0)[0])))
#        else:
#            if option == True:
#                with_covers.append((comic,1))
#            else:
#                to_keep.append(comic)
#
#    if with_covers != []:
#        dgroup = []
#        with_covers = sorted(with_covers, key=lambda to_keep: to_keep[1], reverse=True) # sorts by number of covers
#        max = with_covers[0][1] # max number of covers found
#            
#        for (comic,covers) in with_covers:
#            if covers < max:
#               with_covers.remove((comic,covers))
#               logfile.write('removed... '+ comic[FILENAME]+'\n')
#            else:
#               logfile.write('keeping... '+ comic[FILENAME]+'\n')
#            
#            dgroup.append(comic)
#
#        for comic in to_keep:
#            dgroup.append(comic)
#            logfile.write('keeping... '+ comic[FILENAME]+'\n')
#
#    return dgroup
#
#
#
#
## ==============================================================================================
#
#def keep_filesize_largest(item, dgroup, logfile):
#    ''' Keeps from the 'group' the largest comic'''
#    
#    logfile.write('_________________KEEP_FILESIZE_MOST______________\n')
#
#
#    to_keep = []     
#
#    by_size = sorted(dgroup, key=lambda dgroup: dgroup[item], reverse=True) # sorts by filesize of covers
#                         
#    for comic in by_size[1:]:
#        dgroup.by_size(comic)
#        logfile.write('removed... '+ comic[FILENAME]+'(size '+comic[item]+')\n')
#
#    logfile.write('keeping... '+ by_size[0][3]+'(size '+by_size[0][item]+')\n') 
#    
#    
#    return dgroup
#
#
## ==============================================================================================
#
#def keep_filesize_smallest(item, dgroup, logfile):
#    ''' Keeps from the 'group' the smallest comic'''
#    
#    logfile.write('_________________KEEP_FILESIZE_MOST______________\n')
#
#
#    to_keep = []     
#
#    by_size = sorted(dgroup, key=lambda dgroup: dgroup[item], reverse=False) # sorts by filesize of covers
#                         
#    for comic in by_size[1:]:
#        by_size.remove(comic)
#        logfile.write('removed... '+ comic[FILENAME]+'(size '+comic[item]+')\n')
#
#    logfile.write('keeping... '+ by_size[0][3]+'(size '+by_size[0][item]+')\n') 
#    
#    
#    return dgroup
#
#
## ==============================================================================================
#
#def keep_pagecount_largest(item, dgroup, logfile):
#    ''' Keeps from the 'group' the one with most pages'''
#    
#    logfile.write('_________________KEEP_PAGECOUNT_MOST______________\n')
#
#
#    to_keep = []     
#
#    by_size = sorted(dgroup, key=lambda dgroup: dgroup[item], reverse=True) # sorts by number of pages
#    for comic in by_size:
#        logfile.write(comic[FILENAME]+' (pages '+comic[item]+')\n')
#    for comic in by_size[1:]:
#        logfile.write(comic[FILENAME]+' (pages '+comic[item]+')\n')
#
#                       
#    for comic in by_size[1:]:
#        dgroup.remove(comic)
#        logfile.write('removed... '+ comic[FILENAME]+' (pages '+comic[item]+')\n')
#
#    logfile.write('keeping... '+ by_size[0][FILENAME]+' (pages '+by_size[0][item]+')\n') 
#    
#    
#    return dgroup
#
#
## ==============================================================================================
#
#def keep_pagecoutn_smallest(item, dgroup, logfile):
#    ''' Keeps from the 'group' the one with less pages'''
#    
#    logfile.write('_________________KEEP_PAGECOUNT_LESS______________\n')
#
#
#         
#
#    by_size = sorted(dgroup, key=lambda dgroup: dgroup[item], reverse=False) # sorts by number of pages
#                         
#    for comic in by_size[1:]:
#        dgroup.remove(comic)
#        logfile.write('removed... '+ comic[FILENAME]+' (pages '+comic[item]+')\n')
#
#    logfile.write('keeping... '+ by_size[0][FILENAME]+' (pages '+by_size[0][item]+')\n') 
#    
#    
#    return dgroup
#
#
## ==============================================================================================
#
#def keep_pagecount_noads(item, dgroup, logfile):
#    ''' Keeps from the 'group' the ones that seem to be 'noads' (less pages)'''
#    
#    logfile.write('_________________KEEP_PAGECOUNT_NOADS______________\n')
#
#    to_keep = []
#
#    by_size = sorted(dgroup, key=lambda dgroup: dgroup[item], reverse=False) # sorts by filesize of covers
#           
#    i=0                               #keeps the first one
#    to_keep.append(by_size[i])
#    logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+by_size[i][item]+')\n')
#           
#    while (i<len(by_size)-1) and (int(by_size[i+1][item]) < (int(by_size[i][item]) + C2C_NOADS_GAP)):
#            to_keep.append(by_size[i+1])
#            logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+by_size[i+1][item]+')\n') 
#            i = i+1
#    for j in range (i+1,len(by_size)):
#        logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+by_size[j][item]+')\n')
#            
#    dgroup = to_keep[:]
#    
#    return dgroup
#

# ==============================================================================================

def keep_pagecount_c2c(item, dgroup, logfile):
    ''' Keeps from the 'group' the ones that seem to be 'noads' (less pages)'''
    
    #logfile.write('_________________KEEP_PAGECOUNT_C2C______________\n')

    #to_keep = []

    #by_size = sorted(dgroup, key=lambda dgroup: dgroup[item], reverse=True) # sorts by filesize of covers
           
    #i=0                               #keeps the first one
    #to_keep.append(by_size[i])
    #logfile.write('keeping... '+ by_size[i][FILENAME]+' (pages '+str(by_size[i][item])+')\n')
           
    #print str(len(by_size))
    #print(by_size[i][item])
    
    #while (i<len(by_size)-1) and (int(by_size[i+1][item]) > (int(by_size[i][item]) - int(C2C_NOADS_GAP))):
    #        to_keep.append(by_size[i+1])
     #       logfile.write('keeping... '+ by_size[i+1][FILENAME]+' (pages '+str(by_size[i+1][item])+')\n') 
    #        i = i+1
    #for j in range (i+1,len(by_size)):
    #    logfile.write('removed... '+ by_size[j][FILENAME]+' (pages '+str(by_size[j][item])+')\n')
            
    #dgroup = to_keep[:]
    
    return dgroup


# ==============================================================================================
#
#def remove_pagecount_fileless(item, dgroup, logfile):
#    ''' Removes fileless comics '''
#    
#    logfile.write('_________________REMOVE_FILELESS_______________\n')
#
#    to_keep = dgroup[:]
#
#    for comic in dgroup:
#        if comic[FILENAME] == "Fileless":
#            to_keep.remove(comic)
#        
#    if len(to_keep) > 0:
#            dgroup = to_keep[:]
#    
#    return dgroup
