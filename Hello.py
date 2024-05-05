import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

df = pd.read_csv('./datasets/Processed_GlobalSuperstoreLite.csv')

LOGGER = get_logger(__name__)
st.set_page_config(
    page_title="Coursework | Dashboard",
    page_icon="👋"
)

def run():
    st.write("# Hello World!!!")
    df

if __name__ == "__main__":
    run()
