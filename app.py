import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Text AI Chat", page_icon="💬")

st.title("💬 Text AI Chat")


@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")


qa_model = load_model()


def chat(message: str) -> str:
    if not message.strip():
        return "Please write a question."

    prompt = f"Q: {message}\nA:"

    response = qa_model(
        prompt,
        max_length=80,
        do_sample=True,
        temperature=0.7
    )

    return response[0]["generated_text"].replace(prompt, "").strip()


text_input = st.text_input("Write your question")

if st.button("Send"):
    with st.spinner("Thinking..."):
        answer = chat(text_input)
    st.text_area("Answer", value=answer, height=150)
