#!/usr/bin/env python3

from cgitb import text
import requests
import csv
import json

f = csv.reader(open('extracted_text.csv'), delimiter='\t')

# texts = []
# for i in f:
#     texts.append(i[2])


with open("translated_text.csv", 'w') as file:
    csvwriter = csv.writer(file, delimiter="\t")
    for i in f:
        body = requests.post("http://localhost:5000/translate", json={
            'q': i[2],
            'source': 'auto',
            'target': 'en'
        }).text
        # title = requests.post("http://localhost:5000/translate", json={
        #     'q': [1],
        #     'source': 'auto',
        #     'target': 'en'
        # }).text


        # print(body)
        # if body == "\n" or title == "":
        #     break
            # if "translatedText" in json.loads(str(title)):
            #     #title = json.loads(title)["translatedText"] 
            #     pass
        # else:
        #     body = "none"

        try:
            body = json.loads(body)
            if "translatedText" in body:
                body = body["translatedText"]             
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            continue
            print('Decoding JSON has failed')

        if "{'error':" not in str(body):
            csvwriter.writerow([body, i[-1]])
        
        print(body)
        # print(r.text)
