#!/usr/bin/env python3

from cgitb import text
import requests
import csv


f = csv.reader(open('extracted_text.csv'), delimiter='\t')

# texts = []
# for i in f:
#     texts.append(i[2])

csvwriter = csv.writer(file, delimiter="\t")


with open("translated_text.csv", 'w') as file:
    csvwriter = csv.writer(file, delimiter="\t")
    for i in f:
        body = requests.post("http://localhost:5000/translate", json={
            'q': i[2],
            'source': 'auto',
            'target': 'en'
        }).text
        title = requests.post("http://localhost:5000/translate", json={
            'q': [1],
            'source': 'auto',
            'target': 'en'
        }).text
        
        csvwriter.writerow([title, body, i[-1]])
        # print(r.text)
