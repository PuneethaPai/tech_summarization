import streamlit as st

from fastai.learner import load_learner
from pathlib import Path


def _max_width_():
    max_width_str = f"max-width: 1000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


_max_width_()

model_path = Path("bart_tldr.pkl")


# @st.cache(max_entries=3)
def load_model(path):
    return load_learner(path)


tech_doc = st.text_area(
    label="Man Page Entry",
    value="Pls enter technical document you want to summarize",
    height=500,
)

model = load_learner(fname=model_path)
st.markdown(f"### Summary:\n\n{model.blurr_summarize(tech_doc)[0]}")
