import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from gtts import gTTS
import os
import re

# 1. CORE CONFIG
st.set_page_config(page_title="Tackyon AI", layout="wide")

try:
    # Using your dashboard's exact key name
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Using 1.5-flash for maximum stability
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Missing GOOGLE_API_KEY in Secrets dashboard.")
    st.stop()

def get_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# 2. MAIN INTERFACE
st.title("🎯 Tackyon AI: Intelligence & Dubbing")
url = st.text_input("Paste YouTube Link")

tab1, tab2 = st.tabs(["📝 Smart Summary", "🎙️ Auto-Dubber"])

with tab1:
    lang = st.selectbox("Language", ["Tamil", "English", "Hindi"])
    if st.button("Execute Deep Analysis"):
        with st.spinner("Decoding Intelligence..."):
            try:
                v_id = get_id(url)
                # FIXED: Method must be all lowercase 'get_transcript'
                data = YouTubeTranscriptApi.get_transcript(v_id)
                text = " ".join([i['text'] for i in data])
                res = model.generate_content(f"Summarize in {lang}: {text}").text
                st.write(res)
            except Exception as e:
                st.error(f"Transcript Error: {e}. Check if the video has captions.")

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

# 3. IDENTITY
st.divider()
chat = st.chat_input("Ask Tackyon anything...")
if chat and "who made you" in chat.lower():
    st.write("I am **Tackyon AI**, engineered by **Prapanchan**.")

# CLEAN STYLE
st.markdown("<style>#MainMenu, footer {visibility: hidden;}</style>", unsafe_allow_html=True)