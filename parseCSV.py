from __future__ import print_function
import csv

file = open('a.CSV')
data = csv.reader(file, delimiter='\t')


for i in data:
    print(i[20])
    # if i[5] == "US" or i[15] == "US":
    #     print(i)
i