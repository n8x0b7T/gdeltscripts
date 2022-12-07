import streamlit as st
import pandas as pd
import spacy
from transformers import pipeline
from spacy import displacy
from nltk.corpus import stopwords
import re
import argparse
from wordcloud import WordCloud
from matplotlib import pyplot as plt

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


def highlight_text(text, words, tag):
    matches = []
    text = text.lower()
    for i in words:
        for item in re.finditer(i, text):
            match = {}
            match['start'], match['end'] = item.span()
            match['label'] = tag
            matches.append(match)
    return matches


def get_verbs(doc):
    verbs = set([i.text for i in doc if i.pos_ == "VERB"])
    verbs = [i for i in verbs if str(i).lower() not in stop_words]
    return verbs


def get_wordcloud(text):
    wordcloud = WordCloud(width=1500, height=800,
                          background_color="#0e1117").generate(text)
    fig, ax = plt.subplots()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.figure(facecolor='k')
    plt.tight_layout(pad=0)
    fig.padding = 0
    # plt.gcf().set_facecolor('red')
    # plt.margins(0)
    plt.tight_layout(pad=0)
    for pos in ['right', 'top', 'bottom', 'left']:
        plt.gca().spines[pos].set_visible(False)

    # Selecting the axis-X making the bottom and top axes False.
    plt.tick_params(axis='x', which='both', bottom=False,
                    top=False, labelbottom=False)

    # Selecting the axis-Y making the right and left axes False
    plt.tick_params(axis='y', which='both', right=False,
                    left=False, labelleft=False)
    for item in [fig, ax]:
        item.patch.set_visible(False)
    return fig


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


doc = nlp(cur_row['body_tr'])
highlighted_text = displacy.parse_ents(doc)
accepted_labels = ["DATE", "EVENT", "FAC", "GPE", "LAW",
                   "LOC", "NORP", "ORG", "PERSON", "PRODUCT", "TIME"]
highlighted_text['ents'] = [
    i for i in highlighted_text['ents'] if i['label'] in accepted_labels]
verbs = get_verbs(doc)
highlighted_text['ents'] += highlight_text(cur_row['body_tr'], verbs, "VRB")

keywords = ["demand", "demands", "uprising", "uprising", "demonstrations",
            "demonstrations", "protest", "protests", "corruption", "reform", "violence"]
highlighted_text['ents'] += highlight_text(
    cur_row['body_tr'], keywords, "KWRD")


highlighted_text = displacy.render(
    highlighted_text, style='ent', manual=True, options={"colors": {"KWRD": "#13f4ad"}})

# title
st.subheader(cur_row['title_tr'])


tab1, tab2 = st.tabs(["Text", "WordCloud"])
with tab1:
    st.markdown(highlighted_text, unsafe_allow_html=True)
with tab2:
    st.pyplot(get_wordcloud(cur_row['body_tr']))

# sentiment
st.write(sentiment_text, unsafe_allow_html=True)

# radio selection
with st.form("label_form", clear_on_submit=True):
    option = st.radio("Protest", options=(
        '-', 'Yes', 'No', 'Trash'), horizontal=True)
    st.form_submit_button("Label")

if option == "Yes":
    pass
elif option == "No":
    pass
elif option == "Trash":
    pass
else:
    pass


# update index
st.session_state.num += 1
