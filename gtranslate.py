import time
import csv
from googletrans import Translator
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--articles', help='CSV of extracted websites',  required=True)
parser.add_argument('--output', '-o', help='where to write output',  default='translated.csv')
args = parser.parse_args()

translator = Translator(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0')

translated_text = []

f = csv.reader(open(args.articles), delimiter='\t')
# filter out short articles
f = [i for i in f if len(i[3]) > 1000]

output_csv = csv.writer(open('translated.csv', 'w'), delimiter='\t')

for idx, val in enumerate(f):
    print(f'Translating {idx+1}/{len(f)} articles', end='\r')
    time.sleep(2)
    try:
        translation = translator.translate(f'{val[2]}>>>>{val[3]}', dest='en').text.split('>>>>')
        to_write = val
        to_write[2] = translation[0]
        to_write[3] = translation[1]
        output_csv.writerow(to_write)
    except:
        pass
