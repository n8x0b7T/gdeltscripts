from snorkel.labeling import labeling_function
from snorkel.labeling import PandasLFApplier
from snorkel.labeling.model import LabelModel
from transformers import pipeline
import pandas as pd
import sys

file = sys.argv[1]

df = pd.read_csv(file)
df['body_tr'] = df.apply(lambda row: str(row['body_tr']), axis=1)


sa = pipeline('text-classification',
              model='CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment')

PROTEST = 1
NOT_PROTEST = 0
ABSTAIN = -1
TRASH = 2


@labeling_function()
def lf_keyword_protest(x):
    return PROTEST if "protest" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_demand(x):
    return PROTEST if "demand" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_uprising(x):
    return PROTEST if "uprising" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_demonstration(x):
    return PROTEST if "demonstration" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_corruption(x):
    return PROTEST if "corruption" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_reform(x):
    return PROTEST if "reform" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_peaceful(x):
    return PROTEST if "peaceful" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_violence(x):
    return PROTEST if "violence" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_demonstration_yesterday(x):
    return PROTEST if "demonstration yesterday" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_crowd(x):
    return PROTEST if "crowd" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_march(x):
    return PROTEST if "march" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_oppress(x):
    return PROTEST if "oppress" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_streets(x):
    return PROTEST if "streets" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_activist(x):
    return PROTEST if "activist" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_lawyer(x):
    return NOT_PROTEST if "lawyer" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_keyword_popular_crowd(x):
    return NOT_PROTEST if "popular crowd" in x.body_tr.lower() else ABSTAIN


# invalid articles
@labeling_function()
def lf_keyword_searchsort(x):
    return TRASH if "Searchsort by the date from the latest" in x.body_tr else ABSTAIN


@labeling_function()
def lf_short(x):
    return TRASH if len(x.body_tr) < 200 else ABSTAIN


@labeling_function()
def lf_sentiment(x):
    sentiment = sa(x.body[:250])
    return PROTEST if sentiment[0]['label'] == "negative" else ABSTAIN


# lfs = [lf_keyword_activist, lf_keyword_demonstration_yesterday, lf_keyword_popular_crowd, lf_keyword_lawyer, lf_keyword_protest, lf_keyword_demand, lf_keyword_uprising, lf_keyword_demonstration,
#        lf_keyword_corruption, lf_keyword_reform, lf_keyword_peaceful, lf_keyword_violence, lf_keyword_crowd, lf_keyword_march, lf_keyword_oppress, lf_keyword_streets, lf_keyword_searchsort, lf_short, lf_sentiment]



# non-protest rules
lfs = [lf_keyword_activist, lf_keyword_demonstration_yesterday, lf_keyword_popular_crowd, lf_keyword_protest, lf_keyword_demand, lf_keyword_uprising, lf_keyword_demonstration,
       lf_keyword_corruption, lf_keyword_violence, lf_keyword_crowd, lf_keyword_oppress, lf_keyword_searchsort, lf_short]

applier = PandasLFApplier(lfs)
L_train = applier.apply(df)

label_model = LabelModel(cardinality=3, verbose=True, device="cpu")
label_model.fit(L_train, n_epochs=5, log_freq=50, seed=123)
df["snorkel_label"] = label_model.predict(
    L=L_train, tie_break_policy="abstain")
df.to_csv(file, index=False)
