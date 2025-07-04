import os
import time
import streamlit as st
import requests

backend_origin = os.getenv("BACKEND_ORIGIN")
if backend_origin is None:
    raise ValueError("BACKEND_ORIGIN is required")

title = "CalPal: An Appointment Booking Assistant"

st.set_page_config(page_title=title, page_icon="📅")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title(title)

# Chat Display
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Input Field
user_msg = st.chat_input("Ask me to book an appointment...")

if user_msg:
    # Add user message to chat
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    st.chat_message("user").write(user_msg)

    # Send to FastAPI backend
    res = requests.post(f"{backend_origin}/chat", json={
        "chat": user_msg
    })

    # Extract reply from response
    res_json = res.json()
    bot_reply = res_json.get("message", "We're are sorry but we are having some trouble with the backend")

    # Add bot reply to chat
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)
