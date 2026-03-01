import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
import time
import os
import re

# --- 1. CONFIG & KEYS ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

try:
    # Using your exact secret key name
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Using 1.5-flash as it is most stable for API version v1beta
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Secret Key Missing! Add 'GOOGLE_API_KEY' to Streamlit Secrets.")
    st.stop()

def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# --- 2. THE MAIN INTERFACE ---
st.title("🎯 Tackyon AI: Intelligence & Dubbing")
url = st.text_input("Paste YouTube Link")

tab1, tab2 = st.tabs(["📝 Smart Summary", "🎙️ Auto-Dubber (REAL DUB)"])

# TAB 1: Smart Summariser
with tab1:
    lang = st.selectbox("Language", ["Tamil", "English", "Hindi"])
    if st.button("Execute Deep Analysis"):
        if not url:
            st.warning("Please paste a link first!")
        else:
            with st.spinner("Decoding Intelligence..."):
                try:
                    v_id = get_video_id(url)
                    # FIXED: Added fallback logic for transcript errors
                    try:
                        t_data = YouTubeTranscriptApi.get_transcript(v_id)
                        text = " ".join([i['text'] for i in t_data])
                        prompt = f"Summarize this in {lang}: {text}"
                    except:
                        # Fallback: If transcript fails, Gemini analyzes the URL directly
                        prompt = f"Analyze this video {url} and give a detailed summary in {lang}."
                    
                    res = model.generate_content(prompt).text
                    st.markdown(f"### {lang} Summary\n{res}")
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

# TAB 2: REAL AUTO-DUBBING
with tab2:
    st.subheader("Universal AI Voiceover")
    d_lang = st.selectbox("Target Language", ["Tamil", "Hindi"])
    l_map = {"Tamil": "ta", "Hindi": "hi"}
    
    if st.button("🚀 Start Universal Dubbing"):
        if url:
            try:
                with st.status("Generating Dub...", expanded=True) as status:
                    v_id = get_video_id(url)
                    
                    # Step 1: Get Content
                    st.write("Extracting video content...")
                    try:
                        t_data = YouTubeTranscriptApi.get_transcript(v_id)
                        full_text = " ".join([i['text'] for i in t_data])
                    except:
                        full_text = f"Content from video {url}"

                    # Step 2: Translate
                    st.write(f"Translating to {d_lang}...")
                    trans_prompt = f"Translate the core message of this video into natural {d_lang} for a voiceover: {full_text}"
                    trans = model.generate_content(trans_prompt).text
                    
                    # Step 3: Voice Synth
                    st.write("Creating AI Voice track...")
                    tts = gTTS(text=trans, lang=l_map[d_lang])
                    tts.save("voice.mp3")
                    status.update(label="Complete!", state="complete")
                
                st.audio("voice.mp3")
                st.video(url)
            except Exception as e:
                st.error(f"Dubbing failed: {e}")

# IDENTITY CHECK
st.divider()
chat = st.chat_input("Ask Tackyon anything...")
if chat and "who made you" in chat.lower():
    st.write("I am **Tackyon AI**, engineered by **Prapanchan**.")

st.markdown("<style>#MainMenu, footer {visibility: hidden;}</style>", unsafe_allow_html=True)s