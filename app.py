import streamlit as st
from rapidfuzz import process

st.set_page_config(page_title="Smart Keyboard", page_icon="⌨️")

st.title(" Smart Keyboard for Kids")

with open("words.txt", "r") as f:
    words = [w.strip() for w in f.readlines()]

if "text" not in st.session_state:
    st.session_state.text = ""

text = st.text_input(
    "Type here...",
    value=st.session_state.text,
    key="input_text"
)

last_word = text.split()[-1] if text else ""

if last_word:

    suggestions = process.extract(
        last_word,
        words,
        limit=5
    )

    st.write("### 💡 Suggestions")

    cols = st.columns(len(suggestions))

    for i, (word, score, _) in enumerate(suggestions):

        if cols[i].button(word):

            parts = text.split()

            parts[-1] = word

            st.session_state.text = " ".join(parts)

            st.rerun()
