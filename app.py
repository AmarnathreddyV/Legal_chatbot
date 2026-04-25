import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Legal AI Chatbot")

st.title("⚖️ Legal AI Chatbot")

user_input = st.text_input("Ask your legal question:")

if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            response = run_agent(user_input)
        st.write(response)
    else:
        st.warning("Please enter a question.")
