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
def lf_keyword_gaza(x):
    return PROTEST if "غزة" in x.body_tr.lower() else ABSTAIN


@labeling_function()
def lf_short(x):
    return TRASH if len(x.body_tr) < 200 else ABSTAIN



# Arabic rules
@labeling_function()
def lf_ar_keyword_protest(x):
    return PROTEST if "احتج" in x.body_tr else ABSTAIN

@labeling_function()
def lf_ar_keyword_corruption(x):
    return PROTEST if "افساد" in x.body else ABSTAIN

@labeling_function()
def lf_ar_keyword_demonstrations(x):
    return PROTEST if "مظاهرات" in x.body else ABSTAIN

@labeling_function()
def lf_ar_keyword_confusion(x):
    return PROTEST if "بلبلة" in x.body else ABSTAIN

@labeling_function()
def lf_ar_keyword_disturbances(x):
    return PROTEST if "اضطرابات" in x.body else ABSTAIN


# ar_keywords = [lf_ar_keyword_protest, lf_ar_keyword_corruption,
#                lf_ar_keyword_demonstrations, lf_ar_keyword_confusion, lf_ar_keyword_disturbances]

lfs = [lf_keyword_activist, lf_keyword_demonstration_yesterday, lf_keyword_popular_crowd, lf_keyword_lawyer, lf_keyword_protest, lf_keyword_demand, lf_keyword_uprising, lf_keyword_demonstration,
       lf_keyword_corruption, lf_keyword_reform, lf_keyword_peaceful, lf_keyword_violence, lf_keyword_crowd, lf_keyword_march, lf_keyword_oppress, lf_keyword_streets, lf_keyword_searchsort, lf_short, lf_sentiment,
       lf_ar_keyword_protest, lf_ar_keyword_corruption,
       lf_ar_keyword_demonstrations, lf_ar_keyword_confusion, lf_ar_keyword_disturbances]


# lfs += ar_keywords

# # non-protest rules
# lfs = [lf_keyword_activist, lf_keyword_demonstration_yesterday, lf_keyword_popular_crowd, lf_keyword_protest, lf_keyword_demand, lf_keyword_uprising, lf_keyword_demonstration,
#        lf_keyword_corruption, lf_keyword_violence, lf_keyword_crowd, lf_keyword_oppress, lf_keyword_searchsort, lf_short]

applier = PandasLFApplier(lfs)
L_train = applier.apply(df)

label_model = LabelModel(cardinality=3, verbose=True, device="cpu")
label_model.fit(L_train, n_epochs=5, log_freq=50, seed=123)
df["snorkel_label"] = label_model.predict(
    L=L_train, tie_break_policy="abstain")
df.to_csv(file, index=False)
