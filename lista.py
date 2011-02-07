##lista = []
##lista.append(('spiderman','1'))
##lista.append(('spiderman','2'))
##lista.append(('spiderman','3'))
##lista.append(('hulk','1'))
##lista.append(('hulk','2'))
##lista.append(('hulk','3'))
##lista.append(('spiderman','1'))
##lista.append(('hulk','3'))
##lista

import csv

comiclist=[]

with open('Comic List Short.txt') as f:
    reader = csv.reader(f)
''' This construction needed to ensure file f is closed'''
    for row in reader:
        comiclist.append(row)


