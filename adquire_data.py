##### Temporary reading comics from the Comic List file:

import re
from utils_noiron import __cleanup_series

#import System
#import clr


def getcomiclist():
    '''
    Temporary reading comics from a csv file. Returns a list
    '''
    
    comiclist = [] 

    with open('test data\\comicslist.txt') as f:
        comiclist_temp = list(f.readlines())
    
    for i in comiclist_temp:
        comiclist.append(i.split(';'))
        
    #clean series names to make easier find duplicates
    for i in comiclist:
        i.insert(0, __cleanup_series(i[0],False))
        
    return comiclist



