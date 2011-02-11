#####################################################################################################
##
##      utilsbycory.py - part of duplicatemanager, a script for comicrack
##
##      Author: perezmu after cbanack
##
##      Copyleft perezmu 2011. 
##
######################################################################################################

#### Original declarations
''' 
This module contains utility methods for working with ComicRack
ComicBook objects (i.e. 'book' objects).

@author: Cory Banack
'''
####


import re

def cleanupseries(series_name):
    
    # All of the symbols below cause inconsistency in title searches
    series_name = series_name.lower()
    series_name = series_name.replace('.', '')
    series_name = series_name.replace('_', ' ')
    series_name = series_name.replace('-', ' ')
    series_name = series_name.replace("'", ' ')
    series_name = series_name.replace(":", ' ')
    series_name = re.sub(r'\b(vs\.?|versus|and|or|the|an|of|a|is)\b','', series_name)
    series_name = re.sub(r'giantsize', r'giant size', series_name)
    series_name = re.sub(r'giant[- ]*sized', r'giant size', series_name)
    series_name = re.sub(r'kingsize', r'king size', series_name)
    series_name = re.sub(r'king[- ]*sized', r'king size', series_name)
    series_name = re.sub(r"directors", r"director's", series_name)
    series_name = re.sub(r"\bvolume\b", r"\bvol\b", series_name)
    series_name = re.sub(r"\bvol\.\b", r"\bvol\b", series_name)

    series_name = re.sub(r'[ ]*', r'', series_name)
 
    return series_name
    
    
def convertnumberwords(phrase_s, expand_b):
   """
   Converts all of the number words (as defined by regular expression 'words')
   in the given phrase, either expanding or contracting them as specified.
   When expanding, words like '1' and '2nd' will be transformed into 'one'
   and 'second' in the returned string.   When contracting, the transformation
   goes in reverse.
   
   This method only works for numbers up to 20, and it only works properly
   on lower case strings. 
   """
   number_map = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three',\
      '4': 'four', '5': 'five', '6': 'six','7': 'seven', '8': 'eight',\
      '9': 'nine', '10': 'ten', '11': 'eleven', '12': 'twelve',\
      '13': 'thirteen', '14': 'fourteen', '15': 'fifteen',\
      '16': 'sixteen', '17': 'seventeen', '18': 'eighteen', '19': 'nineteen',\
      '20': 'twenty', '0th': 'zeroth', '1rst': 'first', '2nd': 'second',\
      '3rd': 'third', '4th': 'fourth', '5th': 'fifth', '6th': 'sixth',\
      '7th': 'seventh', '8th': 'eighth', '9th': 'ninth', '10th': 'tenth',\
      '11th': 'eleventh', '12th': 'twelveth', '13th': 'thirteenth',\
      '14th': 'fourteenth', '15th': 'fifteenth', '16th': 'sixteenth',\
      '17th': 'seventeenth', '18th': 'eighteenth', '19th': 'nineteenth',\
      '20th': 'twentieth'}

   b = r'\b'
   if expand_b:
      for (x,y) in number_map.iteritems():
         phrase_s = re.sub(b+x+b, y, phrase_s);
      phrase_s = re.sub(r'\b1st\b', 'first', phrase_s);
   else:
      for (x,y) in number_map.iteritems():
         phrase_s = re.sub(b+y+b, x, phrase_s);
      phrase_s = re.sub(r'\btwelfth\b', '12th', phrase_s);
      phrase_s = re.sub(r'\beightteenth\b', '18th', phrase_s);
   return phrase_s