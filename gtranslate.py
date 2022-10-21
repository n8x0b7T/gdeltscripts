import time
import csv
from googletrans import Translator
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--articles', help='CSV of extracted websites',  required=True)
parser.add_argument('--output', '-o', help='where to write output',  default='translated.csv')
parser.add_argument('--no-filter-lang', default=False, action='store_true')
args = parser.parse_args()

translator = Translator(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0')

accepted_lang='ar'

translated_text = []
the_file = open(args.articles, 'r')
f = csv.reader(the_file, delimiter='\t')
f = list(f)
# print(len(list(f)))
# filter out short articles
# f = [i for i in f if len(i[3]) > 800]

f = [i for i in f if len(i[3]) > 100]


output_csv = csv.writer(open(args.output, 'w'), delimiter='\t')

for idx, val in enumerate(f):
    print(f'Translating {idx+1}/{len(f)} articles', end='\r')
    print(val)
    time.sleep(random.random()*1.8)
    try:
        t = translator.translate(f'{val[2]}>>>>{val[3]}', dest='en')
        text = t.text.split('>>>>')
        to_write = val

        if t.src == accepted_lang and not args.no_filter_lang:
            print(t.src)
        else:
            pass

        to_write[2] = text[0]
        to_write[3] = text[1]
        output_csv.writerow(to_write)
    except Exception as e:
        print(e)
        pass
