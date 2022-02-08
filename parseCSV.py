import csv

file = open('temp.export.CSV')
data = csv.reader(file, delimiter='	')

for i in data:
    if i[5] == "IRQ" or i[15] == "IRQ":
        print(i)
