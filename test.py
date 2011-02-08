####
####
#

# Syntax:
#
#
#       filename    keep    word
#       filename    remove  word
#       filepath    keep    word
#       filepath    remove  word
#       covers      keep    all
#       covers      keep

#       filesize    keep    largest
#       filesize    keep    smallest

#       pagecount   keep    largest
#       pagecount   keep    smallest
#       pagecount   keep    noads
#       pagecount   keep    c2c
#       pagecount   remove  fileless



### Interesante para ordenar por numero:
###
### self.Issues = sorted(self.Issues, key=lambda book: ToFloat(book.Number))
###


from itertools import groupby
from adquire_data import *
from process_dupes import *


logfile = open('logfile.log','w')

(SERIES,NUMBER,VOLUME,FILENAME,PAGECOUNT,FILESIZE,ID,CVDB_ID,FILEPATH,BOOK) = range(10)

comiclist = getcomiclist()
comiclist.pop(0)
''' Remove headers line '''
comiclist.sort()
''' and sort the list '''

# I need to cleanup the series names and issues 1/2, 0.5, etc...
# Also, check for CVDB items first!

#cl_series = []
#''' lista de listas '''
#for key, group in groupby(comiclist, lambda x: x[0]):
#    cl_series.append(list(group))
#    '''groups by series'''
#

cl = {}
''' diccionario'''
for key, group in groupby(comiclist, lambda x: x[0]):
    cl[key] = list(group)
    '''groups by series'''

''' cl es un diccionario con la serie como clave'''


''' quito las series con solo un elemento '''

print 'Hay ', len(cl), 'series distintas'
remove = []
for i in cl.keys():
    if len(cl[i])==1:
        remove.append(i)
        
for i in remove:
    del cl[i]
print 'Hay ', len(cl), 'series distintas con mas de un numero'


''' ahora voy serie a serie, ordeno y reagrupo '''
for series in cl.keys():
    cl[series].sort()
    
    temp_dict = {} 
    for key, group in groupby(cl[series], lambda x: x[2]):
        temp_dict[key] = list(group)
    cl[series]= temp_dict
        
''' nueva limpieza de lo que no tiene suficientes repetidos '''
remove = []
for i in cl:
    for j in cl[i]:
        if len(cl[i][j])==1:
            remove.append((i,j))
            
for a in remove:
    del cl[a[0]][a[1]]
    
''' requiere una segunda pasada para los que han quedado huerfanos '''
remove = []
for i in cl:
    if len(cl[i])==0:
        remove.append(i)
for i in remove:
    del cl[i]

##''' print results '''
##for i in cl:
##	print cl[i][cl[i].keys()[0]][0][1]
##	for j in cl[i]:
##		print '\t',j,'\t', len(cl[i][j])
##
		
''' Now I have them sorted, I convert them to a simple list of lists (groups)...
each item in this list is a list of dupes '''

dupe_groups = []
for i in cl:
    for j in cl[i]:
        for k in range(len(cl[i][j])):
            del cl[i][j][k][0]
        dupe_groups.append(cl[i][j])

print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'


### example trying to keep only 'noads' comics from FILENAME:
##
##for i in range(len(dupe_groups)):
##
##    t_group = dupe_groups[i][:]
##
##    if len(t_group)>1:   # process group only if there is more than one comic
##        t_group = keep_with_word('bchry', FILENAME, t_group, logfile)
##        
##    dupe_groups[i] = t_group[:]
##
##
### cleaning groups with only 1 comic left...
##
##temp_groups = dupe_groups[:]
##for group in temp_groups:
##    if len(group) == 1: dupe_groups.remove(group)
##del temp_groups
##
##
##print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'
##
### example trying to keep only 'covers' comics:
##
##for i in range(len(dupe_groups)):
##
##    t_group = dupe_groups[i][:]
##
##    if len(t_group)>1:   # process group only if there is more than one comic
##        t_group = keep_with_word('covers', FILENAME, t_group, logfile)
##        
##    dupe_groups[i] = t_group[:]
##
##
### cleaning groups with only 1 comic left...
##
##temp_groups = dupe_groups[:]
##for group in temp_groups:
##    if len(group) == 1: dupe_groups.remove(group)
##del temp_groups
##
##
##print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'
##

# example trying to remove only 'noads' comics:


##for i in range(len(dupe_groups)):
##
##    t_group = dupe_groups[i][:]
##
##    if len(t_group)>1:   # process group only if there is more than one comic
##        t_group = keep_covers_most(True, FILENAME, t_group, logfile)
##        
##    dupe_groups[i] = t_group[:]
##
##    
##temp_groups = dupe_groups[:]
##for group in temp_groups:
##    if len(group) == 1: dupe_groups.remove(group)
##del temp_groups
##
##print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'
##
##
##for i in range(len(dupe_groups)):
##
##    t_group = dupe_groups[i][:]
##
##    if len(t_group)>1:   # process group only if there is more than one comic
##        t_group = keep_with_word('fixed', FILENAME, t_group, logfile)
##        
##    dupe_groups[i] = t_group[:]
##    
##
##temp_groups = dupe_groups[:]
##for group in temp_groups:
##    if len(group) == 1: dupe_groups.remove(group)
##del temp_groups
##
##print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'
##
##
##for i in range(len(dupe_groups)):
##
##    t_group = dupe_groups[i][:]
##
##    if len(t_group)>1:   # process group only if there is more than one comic
##        t_group = remove_with_word('noads', FILENAME, t_group, logfile)
##        
##    dupe_groups[i] = t_group[:]
##    
##
##temp_groups = dupe_groups[:]
##for group in temp_groups:
##    if len(group) == 1: dupe_groups.remove(group)
##del temp_groups
##
##print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'
##
##
##for i in range(len(dupe_groups)):
##
##    t_group = dupe_groups[i][:]
##
##    if len(t_group)>1:   # process group only if there is more than one comic
##        t_group = remove_with_word('c2c', FILENAME, t_group, logfile)
##        
##    dupe_groups[i] = t_group[:]
##
##temp_groups = dupe_groups[:]
##for group in temp_groups:
##    if len(group) == 1: dupe_groups.remove(group)
##del temp_groups
##
##print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'
##
##
##for i in range(len(dupe_groups)):
##
##    t_group = dupe_groups[i][:]
##
##    if len(t_group)>1:   # process group only if there is more than one comic
##        t_group = keep_with_word('DCP', FILENAME, t_group, logfile)
##        
##    dupe_groups[i] = t_group[:]
##
### cleaning groups with only 1 comic left...
##
##temp_groups = dupe_groups[:]
##for group in temp_groups:
##    if len(group) == 1: dupe_groups.remove(group)
##del temp_groups
##
##
##print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'
##
##
##print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'


for i in range(len(dupe_groups)):

    t_group = dupe_groups[i][:]

    if len(t_group)>1:   # process group only if there is more than one comic
        t_group = keep_pagecount_c2c(PAGECOUNT, t_group, logfile)
        
    dupe_groups[i] = t_group[:]

temp_groups = dupe_groups[:]
for group in temp_groups:
    if len(group) == 1: dupe_groups.remove(group)
del temp_groups

if len(dupe_groups)>=1:
    print 'Found ',len(dupe_groups), ' groups of dupes, with a total of ', len(reduce(list.__add__, dupe_groups)), ' comics.'



logfile.close()



#####cl_issues={}
#####for series in cl_series:
#####    series.sort()
#####    ''' sort each group '''
#####    for key, group in groupby(series, lambda x:x[0]):
#####        cl_issues[]=list(group)
#####        
###    
###
#
