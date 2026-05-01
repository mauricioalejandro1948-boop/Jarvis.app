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
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')



if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- SALIDA DE VOZ ---
def import pyttsx3

def hablar(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Esto busca una voz masculina en tu sistema
    for voice in voices:
        if "spanish" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()


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
pyttsx3
