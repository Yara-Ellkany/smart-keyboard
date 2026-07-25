import streamlit as st
import language_tool_python

st.title(" Smart Keyboard for Kids")

tool = language_tool_python.LanguageTool('en-US')

text = st.text_area("Type your sentence:")

if st.button("Correct"):
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)

    st.write("### Corrected Sentence")
    st.success(corrected)
