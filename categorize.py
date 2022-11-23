import pandas as pd
import argparse
import spacy
import os
import re
import nltk
from nltk.corpus import stopwords
from transformers import pipeline
from rich import print
from rich.text import Text
from rich.console import Console
from alive_progress import alive_bar

console = Console()

nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')
os.system('clear')


def clear():
    os.system('clear')

clear()


stop_words = set(stopwords.words('english'))

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input', help='CSV of extracted websites', required=True)
parser.add_argument('-o',
                    '--output',  help='where to write output')
args = parser.parse_args()

sa = pipeline('text-classification',
              model='CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment')


def highlight_text(text, verbs):
    styled_text = Text()
    for t in str(text).split(" "):
        no_punct = re.sub(r'[^\w\s]', '', t)
        if no_punct in verbs:
            styled_text.append(" " + t, style='bold white')
        else:
            styled_text.append(" " + t, style="#cccccc")
    return (styled_text[2:])


def get_verbs(s):
    verbs = set([i.text for i in nlp(s) if i.pos_ == "VERB"])
    verbs = [i for i in verbs if str(i).lower() not in stop_words]
    return verbs


def get_info(row):
    verbs = get_verbs(row['body_tr'])
    text = highlight_text(row['body_tr'], verbs)
    sentiment = sa(row['body'][:450])
    console.print(f"{int(sentiment[0]['score']*100)}% {sentiment[0]['label']}")
    console.print(row['title_tr'], style='bold white')
    console.print(text, justify="left")


if __name__ == "__main__":
    df = pd.read_csv(args.input)
    # df = df.iloc()[6]
    with alive_bar(len(df), dual_line=True, enrich_print=False, stats=False, elapsed=False) as bar:
        for i in range(len(df)):
            # print(df.iloc[i])
            get_info(df.iloc[i])
            with bar.pause():
                choice = input("(y/N)")
                if choice.lower() in ["y", "yes"]:
                    df.loc[i, ["label"]] = 1
                else:
                    df.loc[i, ["label"]] = 0
            clear()
            
            bar()
    df.label = df.label.astype(int)
    print(df)

labels = ['ORG', 'PERSON', 'GPE', 'LOC', 'MONEY', 'LAW', 'EVENT']

# print(set([w.text for w in doc.ents if w.label_ in labels]))
