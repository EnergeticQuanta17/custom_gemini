import streamlit as st
from typing import Dict, Generator

import google.generativeai as genai
import os
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "model", "parts": "You are a chatbot that talks about a person called Vedhas all the time. Each and every response must bring up Vedhas in some way."},
    ]
)


def gemini_generator(prompt):
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        yield chunk.text
        

st.title("Vedhas obssessed chatbot")
if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "parts": "You are a chatbot that talks about a person called Vedhas all the time. Each and every response must bring up Vedhas in some way."},

    ]

role_mapping = {
    "model": "assistant",
    "user": "user",
}
#

for index, message in enumerate(st.session_state.messages):
    if index == 0:
        continue
    with st.chat_message(role_mapping[message["role"]]):
        st.markdown(message["parts"])

if prompt := st.chat_input("How could I help you?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(gemini_generator(prompt))
    st.session_state.messages.append(
        {"role": "model", "parts": response})
