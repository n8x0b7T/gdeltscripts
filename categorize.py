import pandas as pd
import argparse
import spacy
import os
import re
import nltk
from nltk.corpus import stopwords
from transformers import pipeline
from termcolor import colored

nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')
os.system('clear')


stop_words = set(stopwords.words('english'))

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input', help='CSV of extracted websites', required=True)
parser.add_argument('-o',
                    '--output',  help='where to write output')
args = parser.parse_args()

sa = pipeline('text-classification',
              model='CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment')


def highlight_text(text, words):
    formattedText = []
    for t in str(text).split(" "):
        no_punct = re.sub(r'[^\w\s]', '', t)
        if no_punct in words:
            formattedText.append(colored(t, 'white', attrs=["bold"]))
        else:
            formattedText.append(colored(t, 'white', attrs=['dark']))
    return (" ".join(formattedText))


def get_verbs(s):
    verbs = set([i.text for i in nlp(s) if i.pos_ == "VERB"])
    verbs = [i for i in verbs if str(i).lower() not in stop_words]
    return verbs


def get_info(row):
    verbs = get_verbs(row['body_tr'])
    text = highlight_text(row['body_tr'], verbs)
    sentiment = sa(row['body'][:450])
    print(f"{int(sentiment[0]['score']*100)}% {sentiment[0]['label']}")
    print(text)
    print()


if __name__ == "__main__":
    df = pd.read_csv(args.input).sample(2)
    # df = df.iloc()[6]
    for i in df.to_dict("records"):
        get_info(i)

    exit()


labels = ['ORG', 'PERSON', 'GPE', 'LOC', 'MONEY', 'LAW', 'EVENT']

# print(set([w.text for w in doc.ents if w.label_ in labels]))
