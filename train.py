import os
import sklearn.metrics as skm
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
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
import pickle
import seaborn as sns
warnings.simplefilter("ignore", category=ConvergenceWarning)


file = sys.argv[1]

df = pd.read_csv(file)
df['pre_processed'] = df.pre_processed.apply(str)


def prepare_data(df):
    return train_test_split(df, test_size=0.1, random_state=0)


train, test = prepare_data(df)


rs = {'random_state': 61}


# Classification - Model Pipeline
def modelPipeline(X_train, y_train,  X_test, y_test):

    log_reg = LogisticRegression(**rs)
    nb = BernoulliNB()
    svm = SVC(**rs)
    dt = DecisionTreeClassifier(**rs)
    rf = RandomForestClassifier(**rs)

    clfs = [
        ('Naive Bayes', nb),
        ('SVM', svm),
        ('Logistic Regression', log_reg),
        ('Decision Tree', dt),
        ('Random Forest', rf),
    ]

    pipelines = []

    scores_df = pd.DataFrame(
        columns=['Model', 'F1_Score', 'Precision', 'Recall', 'Accuracy', 'ROC_AUC'])

    for clf_name, clf in clfs:

        pipeline = Pipeline(steps=[
            ('vect', TfidfVectorizer()),
            ('classifier', clf),
        ]
        )
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        # F1-Score
        fscore = skm.f1_score(y_test, y_pred)
        # Precision
        pres = skm.precision_score(y_test, y_pred)
        # Recall
        rcall = skm.recall_score(y_test, y_pred)
        # Accuracy
        accu = skm.accuracy_score(y_test, y_pred)
        # ROC_AUC
        roc_auc = skm.roc_auc_score(y_test, y_pred)

        print(clf_name)
        print(accu)

        pipelines.append(pipeline)

        # scores_df = pd.concat([pd.DataFrame({
        #                               'Model' : clf_name,
        #                               'F1_Score' : fscore,
        #                               'Precision' : pres,
        #                               'Recall' : rcall,
        #                               'Accuracy' : accu,
        #                               'ROC_AUC' : roc_auc

        #                               }), scores_df], ignoreIndex=True)

    return pipelines


def consensous(data, pipelines):
    results = []
    for pipeline in pipelines:
        results.append(pipeline.predict([data]))
    results = [i[0] for i in results]
    return max(set(results), key=results.count)


def get_combined_score(data, labels, pipelines):
    results = []
    for i in data:
        results.append(consensous(i, pipelines))

    a = np.array(results)
    b = np.array(labels.to_list())
    error = np.mean(a != b)
    return 1-error


print("not pre-processed")
pipelines = modelPipeline(
    train['body'], train['label'], test['body'], test['label'])
print("combined")
print(get_combined_score(test['body'], test['label'], pipelines))


with open("RFModel.pkl", 'wb') as file:
    pickle.dump(pipelines[-1], file)

# print("\npre-processed")
# pipelines = modelPipeline(
#     train['pre_processed'], train['label'], test['pre_processed'], test['label'])
# print("combined")
# print(get_combined_score(test['pre_processed'], test['label'], pipelines))
