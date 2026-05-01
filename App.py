import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import os

# --- PROTOCOLO DE INTERFAZ ---
st.set_page_config(page_title="JARVIS OS", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffff; }
    [data-testid="stChatMessage"] { background-color: #000d1a; border: 1px solid #00ffff; }
    h1 { color: #00ffff; text-shadow: 0 0 10px #00ffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 JARVIS SYSTEM MK-X")

# --- NÚCLEO DE INTELIGENCIA ---
genai.configure(api_key=st.secrets["AIzaSyBnpDuUaaLaoOR5ZDJQOmaQ3-XqsHYYHiI"])

model = genai.GenerativeModel('gemini-1.5-flash', 
    system_instruction="Eres JARVIS. Voz masculina aguda y británica. Eres el asistente de Mauricio. Llama al usuario Mauricio o Señor.")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- SALIDA DE VOZ ---
def hablar(text):
    tts = gTTS(text=text, lang='es-es')
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_html=True)

# --- CHAT ---
for message in st.session_state.chat.history:
    with st.chat_message("user" if message.role == "user" else "assistant"):
        st.markdown(message.parts[0].text)

prompt = st.chat_input("Diga su comando, Señor...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    response = st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)
        hablar(response.text)
