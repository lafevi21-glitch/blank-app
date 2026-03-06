import streamlit as st
from google import genai
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Hysterial AI", page_icon="🤖")
st.title("Hysterial AI")

# --- API SETUP ---
# Securely get your API key from Streamlit Secrets
# In local development, you can use: os.environ.get("GEMINI_API_KEY")
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please add your GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("Settings")
    # Updated to Gemini 3 Flash for maximum speed in 2026
    model_choice = st.selectbox("Model", ["gemini-3-flash", "gemini-2.0-flash"])
    temp = st.slider("Creativity", 0.1, 1.5, 0.7)
    if st.button("Clear Chat"):
        st.session_state.chat_session = client.chats.create(model=model_choice)
        st.session_state.messages = []
        st.rerun()

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Gemini handles history automatically with chat sessions
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
        
        # FIX: Wrap the client and stream in a context manager
        with genai.Client(api_key=api_key) as client:
            # Re-create the session inside the context or use the one from state
            # Note: For streaming, creating a fresh chat session inside the 'with' 
            # block is the safest way to prevent 'client closed' errors.
            chat = client.chats.create(model=model_choice, history=st.session_state.messages[:-1])
            
            stream = chat.send_message_stream(prompt)
            
            for chunk in stream:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
            
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})