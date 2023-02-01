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
parser.add_argument('-o',
                    '--open', help='CSV of extracted websites', required=True)
parser.add_argument('--remove-helpers',
                    help='CSV of extracted websites', action='store_true')
args = parser.parse_args()


st.set_page_config(
    page_title="GDELT Classifier",
    page_icon="🧐",
    layout="wide",
)
if args.open == "":
    print("Please specify an input file")
    st.stop()
    exit()

# MainMenu {display: none}
# header {visibility: hidden}
hide_streamlit_style = """
            <style>
            footer {visibility: hidden}
            div[role="radiogroup"] > :first-child {display: none !important}
            .entity span {display: none}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
def load_model():
    return spacy.load("en_core_web_trf")


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
    wordcloud = WordCloud(width=1000, height=500,
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


@st.cache(allow_output_mutation=True)
def open_csv():
    df = pd.read_csv(args.open)
    if "label" not in df:
        df["label"] = None
    df = df.sort_values(by='label')
    length = len(df)
    current = df[~df["label"].isin([0, 1, -1])].first_valid_index()
    # print("yee", df.at[current, 'label'])
    if current is None:
        return df, length, length
    if df.at[current, 'label'] in [0, 1, -1]:
        current += 1
    # len(df[df['label'] != None])
    return df, current, length


df, current, length = open_csv()

# Initialization
if 'num' not in st.session_state:
    st.session_state.num = current


if st.session_state.num >= length:
    df.to_csv(args.open, index=False)
    st.write("Finished labeling CSV")
    st.stop()


# status bar
st.text(f"{st.session_state.num}/{length}")
my_bar = st.progress(st.session_state.num/length)


# st.write(st.session_state.num)
cur_row = df.iloc[st.session_state.num]

sentiment_text = ""
highlighted_text = ""

if not args.remove_helpers:
    sentiment = sa(cur_row['body'][:250])
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

    keywords = set(["demand", "demands", "uprising", "uprising", "demonstrations",
                    "demonstrations", "protest", "protests", "corruption", "reform", "violence",
                    "peaceful", "march", "protestors", "crowd", "oppressed", "oppression"])

    verb_highlights = highlight_text(cur_row['body_tr'], verbs, "VRB")
    verb_highlights = [i for i in verb_highlights if cur_row['body_tr'][i['start']:i['end']] not in keywords]
    highlighted_text['ents'] += verb_highlights

    highlighted_text['ents'] += highlight_text(
        cur_row['body_tr'], keywords, "KWRD")

    highlighted_text = displacy.render(
        highlighted_text, style='ent', manual=True, options={"colors": {"KWRD": "#13f4ad"}})
else:
    highlighted_text = cur_row['body_tr']

# title
st.subheader(cur_row['title_tr'])


tab1, tab2 = st.tabs(["Text", "WordCloud"])
with tab1:
    st.markdown(highlighted_text, unsafe_allow_html=True)


st.write(sentiment_text, unsafe_allow_html=True)


def handle_label(option):
    # st.session_state.num += 1
    if option == "Yes":
        df.at[st.session_state.num, 'label'] = 1
        st.session_state.num += 1
    elif option == "No":
        df.at[st.session_state.num, 'label'] = 0
        st.session_state.num += 1
    elif option == "Trash":
        df.at[st.session_state.num, 'label'] = -1
        st.session_state.num += 1
    else:
        pass


# radio selection
option = st.radio("Protest", options=(
    '-', 'Yes', 'No', 'Trash'), horizontal=True)
st.button("Label", on_click=handle_label, args=[option])

with tab2:
    cloud_col1, cloud_col2, cloud_col3 = st.columns([1, 5, 1])
    if not args.remove_helpers:
        with cloud_col2:
            st.pyplot(get_wordcloud(cur_row['body_tr']))


if st.button("Save and Exit"):
    df.to_csv(args.open, index=False)
    st.write("done")
    st.empty()
    # st.experimental_rerun()
