import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
import time
import os
import re

# --- 1. CONFIG & KEYS ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

# Exact secret match for GOOGLE_API_KEY
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Please add 'GOOGLE_API_KEY' to your Streamlit Secrets.")
    st.stop()

def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# --- 2. THE JOURNEY ---
if 'view' not in st.session_state: st.session_state.view = "main"

if st.session_state.view == "main":
    with st.sidebar:
        st.title("T-Core Design")
        font = st.selectbox("Font", ["Inter", "Roboto", "Arima"])

    st.title("🎯 Tackyon AI: Intelligence & Dubbing")
    url = st.text_input("Paste YouTube Link")

    tab1, tab2 = st.tabs(["📝 Smart Summary", "🎙️ Auto-Dubber (REAL DUB)"])

    # TAB 1: Smart Summariser
    with tab1:
        lang = st.selectbox("Language", ["Tamil", "English", "Hindi"])
        if st.button("Execute Deep Analysis"):
            with st.spinner("Decoding..."):
                try:
                    v_id = get_video_id(url)
                    # Use the correct lowercase method
                    t_data = YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([i['text'] for i in t_data])
                    res = model.generate_content(f"Summarize in {lang}: {text}").text
                    st.write(res)
                except Exception as e:
                    st.error(f"Error: {e}")

    # TAB 2: REAL AUTO-DUBBING
    with tab2:
        st.subheader("Universal AI Voiceover")
        d_lang = st.selectbox("Target Language", ["Tamil", "Hindi"])
        l_map = {"Tamil": "ta", "Hindi": "hi"}
        
        if st.button("🚀 Start Universal Dubbing"):
            if url:
                try:
                    with st.status("Dubbing...", expanded=True):
                        v_id = get_video_id(url)
                        # Correct method call to fix AttributeError
                        t_data = YouTubeTranscriptApi.get_transcript(v_id)
                        full_text = " ".join([i['text'] for i in t_data])
                        
                        st.write("Translating script...")
                        trans = model.generate_content(f"Translate to {d_lang}: {full_text}").text
                        
                        st.write("Generating voice...")
                        tts = gTTS(text=trans, lang=l_map[d_lang])
                        tts.save("voice.mp3")
                    
                    st.audio("voice.mp3")
                    st.video(url)
                except Exception as e:
                    st.error(f"Dubbing failed: {e}")

    st.divider()
    chat = st.chat_input("Ask Tackyon anything...")
    if chat and "who made you" in chat.lower():
        st.write("I am **Tackyon AI**, engineered by **Prapanchan**.")

    st.markdown(f"<style>html, body {{ font-family: '{font}'; }} #MainMenu, footer {{visibility: hidden;}}</style>", unsafe_allow_html=True)