import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Legal AI Chatbot", layout="centered")

st.title("⚖️ Legal AI Chatbot")
st.write("Ask about legal sections or FIR procedures")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your question...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    response = run_agent(user_input)

    # Show bot message
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
