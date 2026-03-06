import streamlit as st
from google import genai
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Hysterial AI", page_icon="💻")
st.title("Hysterial AI")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please add your GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Model", ["gemini-3-flash-preview", "gemini-2.5-flash"])
    temp = st.slider("Creativity", 0.1, 1.5, 0.7)
    if st.button("Clear Chat"):
        st.session_state.chat_session = client.chats.create(model=model_choice)
        st.session_state.messages = []
        st.rerun()

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_session = client.chats.create(model=model_choice)

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Ask Hysterial AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with genai.Client(api_key=api_key) as client:
                chat = client.chats.create(model=model_choice, history=gemini_history)
                stream = chat.send_message_stream(prompt)
                for chunk in stream:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                break # Success! Exit the retry loop
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2) # Wait 2 seconds before retrying
                continue
            else:
                st.error("Google's servers are a bit unstable right now.")
    
    gemini_history = []
    for m in st.session_state.messages[:-1]:
        role = "model" if m["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [{"text": m["content"]}]})

    with genai.Client(api_key=api_key) as client:
        chat = client.chats.create(model=model_choice, history=gemini_history)
        
        stream = chat.send_message_stream(prompt)
        
        for chunk in stream:
            if chunk.text:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")
            
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})