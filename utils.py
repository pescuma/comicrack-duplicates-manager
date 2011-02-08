'''
This module contains a variety of generally useful utility methods.

@author: Cory Banack
'''


import re

# clr.AddReference('System')
# from System.IO import File

# clr.AddReference('System.Drawing')
# from System.Drawing import Graphics, Bitmap

# clr.AddReference('IronPython')
# from IronPython.Compiler import CallTarget0 

#==============================================================================
def convert_roman_numerals(num_s):
   '''
   Converts the given string into an positive or negative integer value, 
   throwing an exception if it can't.  The given string can be a integer value
   in regular arabic form (1, 2, 3,...) or roman form (i, ii, iii, iv,...).
   The returned value will be an integer.
   
   Note that roman numerals outside the range [-20, 20] and 0 are not supported.
   '''
   
   roman_mapping = {'i':1, 'ii':2,'iii':3,'iv':4,'v':5,'vi':6,'vii':7,'viii':8,
                    'ix':9,'x':10,'xi':11,'xii':12,'xiii':13,'xiv':14,'xv':15,
                    'xvi':16,'xvii':17,'xviii':18,'xix':19,'xx':20}
   
   num_s = num_s.replace(' ', '').strip().lower();
   negative = num_s.startswith('-')
   if negative:
      num_s = num_s[1:]
   
   retval = None
   try:
      retval = int(num_s)
   except:
      retval = roman_mapping[num_s]
   
   return retval * -1 if negative else retval


#==============================================================================
def convert_number_words(phrase_s, expand_b):
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



#==============================================================================
def __cleanup_series(series_name):
   '''
   Returns a cleaned up version of the given search terms.  The terms are 
   cleaned by removing, replacing, and massaging certain keywords to make the
   Comic Vine search more likely to return the results that the user really
   wants.
   
   'series_name' -> the search terms to clean up
   'alt_b' -> true to attempt to produce an alternate search string by also
              replacing numerical digits with their corresponding english words
              and vice versa (i.e. "8" <-> "eight")
   '''
   # All of the symbols below cause inconsistency in title searches
   series_name = series_name.lower()
   series_name = series_name.replace('.', '')
   series_name = series_name.replace('_', ' ')
   series_name = series_name.replace('-', ' ')
   series_name = series_name.replace("'", ' ')
   series_name = re.sub(r'\b(vs\.?|versus|and|or|the|an|of|a|is)\b','', series_name)
   series_name = re.sub(r'giantsize', r'giant size', series_name)
   series_name = re.sub(r'giant[- ]*sized', r'giant size', series_name)
   series_name = re.sub(r'kingsize', r'king size', series_name)
   series_name = re.sub(r'king[- ]*sized', r'king size', series_name)
   series_name = re.sub(r"directors", r"director's", series_name)
   series_name = re.sub(r"\bvolume\b", r"\bvol\b", series_name)
   series_name = re.sub(r"\bvol\.\b", r"\bvol\b", series_name)

   #series_name = re.sub(r'gijoe', r'gi joe', series_name)
   
   series_name = re.sub(r' *', r'', series_name)

   # try to expand single number
   # words, and if that fails, try to contract them.
   # orig_series_name = series_name
   # if alt_b:
      # series_name = utils.convert_number_words(series_name, True)
   # if alt_b and series_name == orig_series_name:
      # series_name = utils.convert_number_words(series_name, False)
      
   # # strip out punctuation
   # word = re.compile(r'[\w]{1,}')
   # series_name = ' '.join(word.findall(series_name))
   
   return series_name
   
   
   
   #################### Book wrapper based in pescuma's
   
