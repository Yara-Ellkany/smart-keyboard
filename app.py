import streamlit as st
from transformers import pipeline

st.title(" Smart Keyboard for Kids")

@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="vennify/t5-base-grammar-correction"
    )

corrector = load_model()

text = st.text_area("Type your sentence")

if st.button("Correct"):
    if text:
        result = corrector("grammar: " + text, max_length=100)
        st.success(result[0]["generated_text"])
