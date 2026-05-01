import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
import os
from streamlit_mic_recorder import speech_to_text

# --- PROTOCOLO DE INTERFAZ ---
st.set_page_config(page_title="JARVIS OS", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffff; }
    [data-testid="stChatMessage"] { background-color: #0e1117; border: 1px solid #00ffff; }
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
import re

def hablar(text):
    # 1. LIMPIEZA TOTAL: Borra asteriscos, guiones y símbolos de diseño
    # Esto evita que JARVIS diga "asterisco" o se quede pegado.
    text_limpio = re.sub(r'[*#_>-]', '', text)
    
    # 2. VOZ MASCULINA: Usamos 'es-us' (Español de EE.UU.)
    # Google suele asignar una voz de hombre para este código de región.
    tts = gTTS(text=text_limpio, lang='es-us')
    
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # El audio se reproduce automáticamente al recibir la respuesta
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_html=True)
    os.remove("temp.mp3")



# --- ENTRADA DE VOZ (MANOS LIBRES/BOTÓN) ---
st.write("Presiona el micrófono para hablar con JARVIS:")
# Esto convierte tu voz a texto directamente
voz_usuario = speech_to_text(language='es', start_prompt="🎤 ESCUCHANDO...", key='audio_input')

# --- LÓGICA DE PROCESAMIENTO ---
prompt = st.chat_input("Diga su comando, Señor...")

# Si el usuario habla o escribe
if voz_usuario or prompt:
    entrada = voz_usuario if voz_usuario else prompt
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(entrada)
    
    # Generar respuesta de JARVIS
    try:
        response = st.session_state.chat.send_message(entrada)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        # JARVIS habla la respuesta
        hablar(response.text)
    except Exception as e:
        st.error(f"Error de conexión: {e}")

# --- HISTORIAL VISUAL ---
for message in st.session_state.chat.history:
    if message.role == "model":
        with st.chat_message("assistant"):
            st.markdown(message.parts[0].text)
