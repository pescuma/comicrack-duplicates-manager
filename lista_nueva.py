
# ironpython no soporta csv

#import csv
#
#comiclist=[]
#
#with open('Comic List Long.csv') as f:
#    comiclist = list(csv.reader(f))



##### Temporary reading comics from the Comic List file:
 
with open('Comic List Long.csv') as f:
    comiclist = list(readlines(f))
  
filename = "test.dat"

file = open(filename,"w")

# Write all the lines at once:
FILE.writelines(namelist)
    
# Alternatively write them one by one:
for name in namelist:
    FILE.write(name)
    
FILE.close()

## Now I try to clean up the filenames
## Copied from CBANACK's Script

def __cleanup_series(series_name, alt_b):
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
   series_name = re.sub(r'\b(vs\.?|versus|and|or|the|an|of|a|is)\b',
      '', series_name)
   series_name = re.sub(r'giantsize', r'giant size', series_name)
   series_name = re.sub(r'giant[- ]*sized', r'giant size', series_name)
   series_name = re.sub(r'kingsize', r'king size', series_name)
   series_name = re.sub(r'king[- ]*sized', r'king size', series_name)
   series_name = re.sub(r"directors", r"director's", series_name)
   series_name = re.sub(r"\bvolume\b", r"\bvol\b", series_name)
   series_name = re.sub(r"\bvol\.\b", r"\bvol\b", series_name)

   # try to expand single number
   # words, and if that fails, try to contract them.
   orig_series_name = series_name
   if alt_b:
      series_name = utils.convert_number_words(series_name, True)
   if alt_b and series_name == orig_series_name:
      series_name = utils.convert_number_words(series_name, False)
      
   # strip out punctuation
   word = re.compile(r'[\w]{1,}')
   series_name = ' '.join(word.findall(series_name))
   
   return series_name