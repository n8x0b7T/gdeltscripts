import spacy
import argparse
import csv

nlp = spacy.load("en_core_web_trf")

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='CSV of extracted websites', required=True)
parser.add_argument('--output',
                    '-o',
                    help='where to write output',
                    default='translated.csv')
args = parser.parse_args()

f = csv.reader(open(args.input, 'r'), delimiter='\t')

wanted_labels = set([])

labeled_articles = []

for i in f:
    labels = ['ORG', 'PERSON', 'GPE', 'LOC', 'MONEY', 'LAW', 'EVENT']
    cur_article = [{
        'ORG': [],
        'PERSON': [],
        'GPE': [],
        'LOC': [],
        'MONEY': [],
        'LAW': [],
        'EVENT': []
    }]

    doc = nlp(i[3])

    for j in labels:
        cur_article[0][j] = set([w.text for w in doc.ents if w.label_ == j])
    a = cur_article + i
    labeled_articles.append(a)

csv.writer(open(args.output, 'w'), delimiter='\t').writerows(labeled_articles)

