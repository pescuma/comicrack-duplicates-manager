# you have a list of dictionaries of employee data
# determine the average age of each department
# tested with Python24     vegaseat    05jul2006

import operator
import itertools
import pprint     # pretty print the lists

dic_list = [
{
'name': 'Felix',
'age': 34,
'dept': 22
},
{
'name': 'Mary',
'age': 27,
'dept': 23
},
{
'name': 'Kevin',
'age': 41,
'dept': 22
},
{
'name': 'Adam',
'age': 21,
'dept': 22
},
{
'name': 'Larry',
'age': 53,
'dept': 23
}
]
print "Original list:"
pprint.pprint(dic_list)

dic_list.sort(key=operator.itemgetter('dept'))

print "-"*50
print "List after sorting by 'dept':"
pprint.pprint(dic_list)

print "-"*50

# group the departments in lists
list1 = []
for key, items in itertools.groupby(dic_list, operator.itemgetter('dept')):
    list1.append(list(items))

print "After grouping the list by department:"
pprint.pprint(list1)  # test

print "-"*50

# create a list of department number and average age in each department
age_list = []
for item in list1:
    # the department number
    department = item[0]['dept']
    # the size of the department
    size = len(item)
    sum = 0
    for k in range(size):
        # sum up the ages of each department
        sum += int((item[k]['age']))
    average = sum/float(size)
    age_list.append((department, average))

for item in age_list:
    print "Department number %s has an average age of %0.1f" % (item[0], item[1])

"""
result -->
Original list:
[{'dept': 22, 'age': 34, 'name': 'Felix'},
 {'dept': 23, 'age': 27, 'name': 'Mary'},
 {'dept': 22, 'age': 41, 'name': 'Kevin'},
 {'dept': 22, 'age': 21, 'name': 'Adam'},
 {'dept': 23, 'age': 53, 'name': 'Larry'}]
--------------------------------------------------
List after sorting by 'dept':
[{'dept': 22, 'age': 34, 'name': 'Felix'},
 {'dept': 22, 'age': 41, 'name': 'Kevin'},
 {'dept': 22, 'age': 21, 'name': 'Adam'},
 {'dept': 23, 'age': 27, 'name': 'Mary'},
 {'dept': 23, 'age': 53, 'name': 'Larry'}]
--------------------------------------------------
After grouping the list by department:
[[{'dept': 22, 'age': 34, 'name': 'Felix'},
  {'dept': 22, 'age': 41, 'name': 'Kevin'},
  {'dept': 22, 'age': 21, 'name': 'Adam'}],
 [{'dept': 23, 'age': 27, 'name': 'Mary'},
  {'dept': 23, 'age': 53, 'name': 'Larry'}]]
--------------------------------------------------
Department number 22 has an average age of 32.0
Department number 23 has an average age of 40.0

"""
