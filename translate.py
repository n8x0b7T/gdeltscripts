#!/usr/bin/env python3

from cgitb import text
import requests
import csv


f = csv.reader(open('extracted_text.csv'), delimiter='\t')

texts = []
for i in f:
    texts.append(i[1])

for i in texts:
    r = requests.post("http://localhost:5000/translate", json={
        'q': i,
        'source': 'auto',
        'target': 'en'
    })

    print(r.text)
