# https://towardsdatascience.com/building-web-applications-with-streamlit-for-nlp-projects-cdc1cf0b38db
# Necessary imports
import streamlit as st
import pandas as pd
from transformers import pipeline
import spacy
from spacy import displacy
from nltk.corpus import stopwords
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input', help='CSV of extracted websites', required=True)
parser.add_argument('-o',
                    '--output',  help='where to write output')
args = parser.parse_args()

if args.input == "":
    print("Please specify an input file")
    exit()

st.set_page_config(
    page_title="GDELT Classifier",
    page_icon="🧐",
    layout="wide",
)

hide_streamlit_style = """
            <style>
            #MainMenu {display: none}
            footer {visibility: hidden}
            header {visibility: hidden}
            div[role="radiogroup"] > :first-child {display: none !important}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
def load_model():
    return spacy.load("en_core_web_sm")


nlp = load_model()

stop_words = set(stopwords.words('english'))


@st.cache(allow_output_mutation=True)
def load_sa():
    return pipeline('text-classification', model='CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment')


sa = load_sa()


def highlight_text(text, verbs):
    matches = []

    for i in verbs:
        for item in re.finditer(i, text):
            match = {}
            match['start'], match['end'] = item.span()
            # The tag/label that you would like to display
            match['label'] = 'VRB'
            matches.append(match)
    return matches


def get_verbs(doc):
    verbs = set([i.text for i in doc if i.pos_ == "VERB"])
    verbs = [i for i in verbs if str(i).lower() not in stop_words]
    return verbs


df = pd.read_csv(args.input)
df = df.sample(15)


# Initialization
if 'num' not in st.session_state:
    st.session_state.num = 0

df_len = len(df)
my_bar = st.progress(st.session_state.num/len(df))

if st.session_state.num >= df_len:
    st.write("done")
    st.stop()
cur_row = df.iloc[st.session_state.num]

sentiment = sa(cur_row['body'][:450])
if sentiment[0]['label'] == "negative":
    sentiment_color = "red"
elif sentiment[0]['label'] == "positive":
    sentiment_color = "green"
else:
    sentiment_color = "inherit"

sentiment_text = f"<p style=\"margin:0;opacity:0.8\">Sentiment</p><h4 style=\"padding-top:0\">{int(sentiment[0]['score']*100)}% <span style=\"color:{sentiment_color}\">{sentiment[0]['label']}</h4>"
st.write(sentiment_text, unsafe_allow_html=True)


doc = nlp(cur_row['body_tr'])
highlighted_text = displacy.parse_ents(doc)

print(highlighted_text)
verbs = get_verbs(doc)
highlighted_text['ents'] += highlight_text(cur_row['body_tr'], verbs)

print(displacy.parse_ents(doc))
ent_html = displacy.render(
    highlighted_text, style='ent', manual=True)
# Display the entity visualization in the browser:
st.markdown(ent_html, unsafe_allow_html=True)

# choice = st.button('Yes')
# st.button('No')

st.write("<br>", unsafe_allow_html=True)
with st.form("label_form", clear_on_submit=True):
    option = st.radio("Protest", options=('-', 'Yes', 'No', 'Trash'), horizontal=True)
    st.form_submit_button("Label")


if option == "Yes":
    st.write("YUH")
elif option == "No":
    pass
else:
    st.write("nah")

st.session_state.num += 1
