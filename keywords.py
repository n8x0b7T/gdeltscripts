import pandas as pd
import random
import re
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("./dataset.csv")


def pre_process(text):
    text = re.sub(r'\d', ' ', text)
    return text


df['body'] = df['body'].apply(lambda x: pre_process(x))


def get_stop_words(stop_file_path):
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()[1:-1]
        return list(set(i.strip() for i in stopwords))


# load a set of stop words
stopwords = get_stop_words("list.txt")




cv = CountVectorizer(max_df=0.80, stop_words=stopwords, ngram_range=(2, 3))
word_count_vector = cv.fit_transform(df["body"])

words = list(cv.vocabulary_.keys())
# random.shuffle(words)
for i in words[:30]:
    print(i)

