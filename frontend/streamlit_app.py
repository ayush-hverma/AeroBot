import streamlit as st
import requests

API_URL = ""

st.set_page_config(page_title="AeroBot", layout="centered")
st.title("AeroBot: Your Travel Companion")
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("➕ New Chat"):
    st.session_state.messages = []
    st.experimental_rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# User Input
# -------------------------
user_input = st.chat_input("Ask something about Changi or Jewel Changi...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": user_input})
                answer = response.json().get("answer", "Sorry, something went wrong.")
            except Exception as e:
                answer = f"Error: {e}"

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})