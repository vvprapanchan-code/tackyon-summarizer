import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from gtts import gTTS
import os
import re

# 1. SETUP
st.set_page_config(page_title="Tackyon AI", layout="wide")

try:
    # Exact match for your secret key
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Missing GOOGLE_API_KEY in Secrets!")
    st.stop()

def get_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 2. UI
st.title("🎯 Tackyon AI: Intelligence & Dubbing")
url = st.text_input("Paste YouTube Link")

tab1, tab2 = st.tabs(["📝 Smart Summary", "🎙️ Auto-Dubber"])

with tab1:
    lang = st.selectbox("Language", ["Tamil", "English", "Hindi"])
    if st.button("Execute Deep Analysis"):
        with st.spinner("Decoding..."):
            try:
                v_id = get_id(url)
                # FIXED: Correct lowercase call
                data = YouTubeTranscriptApi.get_transcript(v_id)
                text = " ".join([i['text'] for i in data])
                res = model.generate_content(f"Summarize in {lang}: {text}").text
                st.write(res)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("Universal AI Voiceover")
    target_lang = st.selectbox("Dub to Language", ["Tamil", "Hindi"])
    l_map = {"Tamil": "ta", "Hindi": "hi"}
    
    if st.button("🚀 Start Universal Dubbing"):
        if url:
            try:
                with st.status("Processing...", expanded=True):
                    v_id = get_id(url)
                    data = YouTubeTranscriptApi.get_transcript(v_id)
                    text = " ".join([i['text'] for i in data])
                    
                    st.write("Translating...")
                    trans = model.generate_content(f"Translate to {target_lang}: {text}").text
                    
                    st.write("Generating AI Voice...")
                    tts = gTTS(text=trans, lang=l_map[target_lang])
                    tts.save("voice.mp3")
                
                st.audio("voice.mp3")
                st.video(url)
            except Exception as e:
                st.error(f"Dubbing failed: {e}")

# IDENTITY
st.divider()
chat = st.chat_input("Ask Tackyon anything...")
if chat and "who made you" in chat.lower():
    st.write("I am **Tackyon AI**, engineered by **Prapanchan**.")

# SIMPLE STYLE (No Syntax Errors)
st.markdown("<style>#MainMenu, footer {visibility: hidden;}</style>", unsafe_allow_html=True)