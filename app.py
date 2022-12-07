# https://towardsdatascience.com/building-web-applications-with-streamlit-for-nlp-projects-cdc1cf0b38db
# Necessary imports
import streamlit as st
import pandas as pd
import spacy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input', help='CSV of extracted websites', required=True)
parser.add_argument('-o',
                    '--output',  help='where to write output')
args = parser.parse_args()


hide_streamlit_style = """
            <style>
            #MainMenu {display: none;}
            footer {visibility: hidden}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

nlp = spacy.load("en_core_web_sm")


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
st.write(cur_row['body_tr'])

choice = st.button('Yes')
st.button('No')


if choice:
    st.write("YUH")
else:
    st.write("nah")

st.write(st.session_state.num)

st.session_state.num += 1
