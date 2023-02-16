import warnings
from sklearn.exceptions import ConvergenceWarning
import pandas as pd
# from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
import sys
import seaborn as sns
warnings.simplefilter("ignore", category=ConvergenceWarning)


file = sys.argv[1]

df = pd.read_csv(file)


def prepare_data(df):
    # data = df["body"].to_list()
    # label = df["label"].to_list()
    return train_test_split(df, test_size=0.2, random_state=30)

train, test = prepare_data(df)
# print(train[1])

model = Pipeline([
    ('vect', TfidfVectorizer()),
    ('clf', LogisticRegression()),
])
model.fit(train['body'], train['label'])

predicted_categories = model.predict(test['body'])
print(f"The accuracy is {accuracy_score(test['label'], predicted_categories)}.\n")

plt.figure(figsize=(6, 4))
plt.title("title")
# plot the confusion matrix
mat = confusion_matrix(test['label'], predicted_categories)
sns.heatmap(mat.T, square = True, annot=True, fmt = "d", xticklabels=['spam', 'ham'],yticklabels=['spam', 'ham'])
plt.xlabel("true labels")
plt.ylabel("predicted label")
plt.show()