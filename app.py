import streamlit as st
from spellchecker import SpellChecker

st.set_page_config(page_title="Smart Keyboard", page_icon="⌨️")

spell = SpellChecker()

st.title("⌨️ Smart Keyboard for Kids")

word = st.text_input("Type an English word:")

if word:
    word = word.lower()

    if word in spell:
        st.success(f"✅ Great! '{word}' is correct.")
    else:
        correction = spell.correction(word)
        suggestions = list(spell.candidates(word))

        st.error("❌ Incorrect spelling")

        if correction:
            st.write("### Did you mean?")
            st.success(correction)

        if suggestions:
            st.write("### Other suggestions")
            for s in sorted(suggestions):
                st.write("- ", s)
