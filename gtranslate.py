import time
import csv
from googletrans import Translator

translator = Translator()

translated_text = []

f = csv.reader(open('./extracted_text.csv'), delimiter='\t')
output_csv = csv.writer(open("translated.csv", "w"), delimiter="\t")

for g in f:
    time.sleep(3)
    try:
        translation = translator.translate(f'{g[2]}>>>>{g[3]}', dest='en').text.split('>>>>')
        to_write = g
        to_write[2] = translation[0]
        to_write[3] = translation[1]
        output_csv.writerow(to_write)
    except:
        pass

