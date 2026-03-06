import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gemma 2 Local AI", page_icon="🤖")
st.title("💬 My Personal Gemma 2B")

# --- MODEL LOADING (Cached so it only happens once) ---
@st.cache_resource
def load_model():
    model_id = "google/gemma-2-2b-it"
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=quant_config,
        device_map="auto"
    )
    return tokenizer, model

tokenizer, model = load_model()

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("Settings")
    temp = st.slider("Creativity (Temperature)", 0.1, 1.0, 0.7)
    max_len = st.slider("Max Response Length", 64, 512, 256)
    if st.button("Clear Chat"):
        st.session_state.messages = []

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        # Format the conversation for Gemma
        input_text = tokenizer.apply_chat_template(
            st.session_state.messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
        
        outputs = model.generate(
            **inputs, 
            max_new_tokens=max_len, 
            temperature=temp,
            do_sample=True
        )
        
        response = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})