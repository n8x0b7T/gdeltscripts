# https://towardsdatascience.com/building-web-applications-with-streamlit-for-nlp-projects-cdc1cf0b38db
# Necessary imports
import streamlit as st
import pandas as pd
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


st.set_page_config(
    page_title="GDELT Classifier",
    page_icon="🧐",
    layout="wide",
)

hide_streamlit_style = """
            <style>
            #MainMenu {display: none;}
            footer {visibility: hidden}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

def highlight_text(text, verbs):
    # styled_text = ""
    # for t in str(text).split(" "):
    #     no_punct = re.sub(r'[^\w\s]', '', t)
    #     if no_punct in verbs:
    #         styled_text += f" **{t}**"
    #     else:
    #         styled_text += f" {t}"
    # return (styled_text[2:])
    matches = []

    for i in verbs:
        for item in re.finditer(i,text):
            match = {}
            match['start'], match['end'] = item.span() 
            match['label'] = 'VRB' # The tag/label that you would like to display
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



doc = nlp(cur_row['body_tr'])
highlighted_text = displacy.parse_ents(doc)

verbs = get_verbs(doc)
highlighted_text['ents'] += highlight_text(cur_row['body_tr'], verbs)

print(displacy.parse_ents(doc))
ent_html = displacy.render(highlighted_text, style='ent', manual=True, jupyter=False)
# Display the entity visualization in the browser:
st.markdown(ent_html, unsafe_allow_html=True)

choice = st.button('Yes')
st.button('No')


if choice:
    st.write("YUH")
else:
    st.write("nah")

st.write(st.session_state.num)

st.session_state.num += 1
