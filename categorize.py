from transformers import pipeline
import csv
import spacy
import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input', help='CSV of extracted websites',  required=True)
parser.add_argument('-o',
                    '--output',  help='where to write output')
args = parser.parse_args()

sa = pipeline('text-classification',
              model='CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment')
nlp = spacy.load("en_core_web_trf")

f = csv.reader(open('with_orig.csv'), delimiter='\t')

labels = ['ORG', 'PERSON', 'GPE', 'LOC', 'MONEY', 'LAW', 'EVENT']

for i in f:
    # print(i)
    # break
    try:
        # print(i[-1])
        print(sa(i[-1][:400]))
        doc = nlp(i[-2])
        print([i for i in doc if i.pos_ == "VERB"])
        #print(set([w.text for w in doc.ents if w.label_ in labels]))
        print("The text:\n", i[-2])
        input("(Yes/No)")
        print("\n\n\n")
    except Exception as e:
        print(e)
        pass

# text = "عراق إحباط محاولة ميليشيات شيعية خطف نائبة ومحافظ سنيي"
# sentences = ['']

# print(sa(text))

if __name__ == "__main__":
    df = pd.read_csv(args.input)
