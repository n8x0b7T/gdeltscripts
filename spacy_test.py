import spacy
import argparse
import csv

nlp = spacy.load("en_core_web_trf")

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='CSV of extracted websites',  required=True)
parser.add_argument('--output', '-o', help='where to write output',  default='translated.csv')
args = parser.parse_args()

f = csv.reader(open(args.input, 'r'), delimiter='\t')


for i in f:
    doc = nlp(i[3])
    print([(w.text, w.pos_) for w in doc if w.pos_ == "VERB" or w.pos_ == "PROPN"], "\n\n\n\n")
