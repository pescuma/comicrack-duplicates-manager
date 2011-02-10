#####################################################################################################
##
##      getcvdb.py - part of duplicatemanager, a script for comicrack
##
##      Author: cbanack, for his Comic Vine Scraper module
##
##      
######################################################################################################

### original credits
''' 
This module contains utility methods for working with ComicRack
ComicBook objects (i.e. 'book' objects).

@author: Cory Banack
'''
#########


import re

# =============================================================================
def extract_issue_ref(book):
   '''
   This method looks in the Tags and Notes fields of the given book for 
   evidence that the given ComicBook has been scraped before.   If possible, 
   it will construct an IssueRef based on that evidence, and return it.  
   If not, it will return None.   
   
   If the user has manually added a "skip" flag to one of those fields, this
   method will return the string "skip", which should be interpreted as 
   "never scrape this book".
   '''
   

   tag_found = re.search(r'(?i)CVDB(\d{1,})', book.Tags)
   if not tag_found:
      tag_found = re.search(r'(?i)CVDB(\d{1,})', book.Notes)
      if not tag_found:
         tag_found = re.search(r'(?i)ComicVine.?\[(\d{1,})', book.Notes)

   retval = None
   if tag_found:
      retval = tag_found.group(1).lower()
      
   return retval
