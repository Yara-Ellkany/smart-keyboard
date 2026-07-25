import streamlit as st
from spellchecker import SpellChecker

spell = SpellChecker()

st.title(" Smart Keyboard")

word = st.text_input("Type a word")

if word:
    word = word.lower()

    if word in spell:
        st.success(f" '{word}' is correct!")
    else:
        correction = spell.correction(word)
        suggestions = list(spell.candidates(word) or [])

        st.error(" Incorrect spelling")

        if correction:
            st.success(f"Did you mean: {correction}")

        if suggestions:
            st.write("Suggestions:")
            for s in suggestions:
                st.write("•", s)
