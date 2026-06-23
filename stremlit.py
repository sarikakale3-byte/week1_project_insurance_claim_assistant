import streamlit as st
import random
import requests
import time
import uuid
from dotenv import load_dotenv
#from app import askllm, SYSTEM_PROMPT
from utils.guardrails import detect_pii, detect_injection, is_off_topic
import re

FASTAPI_URL = "http://localhost:8000"

def is_greeting(text):
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    return text.lower().strip() in greetings

# Load environment variables
load_dotenv()

st.set_page_config(page_title="SK Insurance Chat Bot")

st.title("SK Insurance Chat Bot")

# Default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask your insurance question..."):

    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        
        if is_greeting(prompt):
            response = "Hello! I'm your Insurance Claims Assistant. How can I help you today?"
            st.markdown(response)

        # GUARDRAILS CHECK 
        elif detect_injection(prompt):
            response = "Suspicious input detected. Please follow allowed usage."
            st.error(response)

        elif detect_pii(prompt):
            response = "Please avoid sharing sensitive personal information."
            st.warning(response)

        elif is_off_topic(prompt):
            response = "Please ask questions about SK Insurance products only."
            st.info(response)

        else:
            # SAFE → call LLM
            #stream = askllm(prompt, SYSTEM_PROMPT)
            resp = requests.post(
                f"{FASTAPI_URL}/chat",
                json={
                    "message": prompt,
                    "session_id": st.session_state.session_id,
                },
                timeout=60,
            )
            if resp.status_code==200:
                data = resp.json()
                response_text = data["response"]
            else:
                response_text =f"Error in the request"

            # Remove JSON part
            clean_text = re.sub(
                r"JSON:\s*\{.*\}",
                "",
                response_text,
                flags=re.DOTALL
            ).strip()

            # Remove "Answer:" label
            clean_text = clean_text.replace("Answer:", "").strip()

            st.markdown(clean_text)

            response = clean_text

    # Store final response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
