from dotenv import load_dotenv
import httpx
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(
    page_title="💬Chatbot",
    page_icon=":robot:",
    layout="centered"
)

st.title("💬Generative AI Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.1,
    http_client=httpx.Client(verify=False),
)

user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    response = llm.invoke(
        input = [{"role": "system", "content": "You are a helpful chatbot. Be concise and accurate."}, *st.session_state.chat_history]
    )   

    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
