
import pandas as pd
import argparse
import spacy
import os
from nltk.corpus import stopwords
from transformers import pipeline
nlp = spacy.load("en_core_web_sm")

os.system('clear')

stop_words = set(stopwords.words('english'))

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input', help='CSV of extracted websites',  required=True)
parser.add_argument('-o',
                    '--output',  help='where to write output')
args = parser.parse_args()

sa = pipeline('text-classification',
              model='CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment')

# print(stop_words)


def get_verbs(s):
    return [i for i in set(
        [i for i in nlp(s) if i.pos_ == "VERB"])
         if str(i).lower() not in stop_words]


def get_info(row):
    # print(row['body_tr'])
    # return
    # print(sa(row['body_tr'][:450]))
    print(get_verbs(row['body_tr']))


if __name__ == "__main__":
    df = pd.read_csv(args.input)
    for i in df.to_dict("records"):
        get_info(i)

    exit()


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
