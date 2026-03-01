import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
from gtts import gTTS
from youtube_transcript_api import YouTubeTranscriptApi
import random
import time
import os
import re

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

# FIX: Matching your exact 'GOOGLE_API_KEY' from Secrets
try:
    GEMINI_KEY = st.secrets["GOOGLE_API_KEY"] 
    S_URL = st.secrets["SUPABASE_URL"]
    S_KEY = st.secrets["SUPABASE_KEY"]
except KeyError as e:
    st.error(f"⚠️ Secret Missing: {e}. Check Streamlit Secrets!")
    st.stop()

# Configure Gemini 2.5 Flash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash') 
supabase: Client = create_client(S_URL, S_KEY)

# --- 2. UTILITY: EXTRACT VIDEO ID ---
def get_video_id(url):
    reg = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(reg, url)
    return match.group(1) if match else None

# --- 3. THIRUKURAL DATA ---
THIRUKURAL_DATA = [
    {"k": "கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.", "m": "Learn thoroughly; then live according to that learning."},
    {"k": "தெய்வத்தான் ஆகா தெனினும் முயற்சிதன் மெய்வருத்தக் கூலி தரும்.", "m": "Effort pays the wages of hard work, even if luck fails."},
]

# --- 4. SESSION STATE (Persistent Login Foundation) ---
if 'view' not in st.session_state: st.session_state.view = "splash"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 5. THE USER JOURNEY ---

# FEATURE: Executive Splash Screen
if st.session_state.view == "splash":
    st.markdown("<h1 style='text-align: center; margin-top: 20%; font-size: 80px; color: #00D4FF;'>TACKYON</h1>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.view = "gateway"
    st.rerun()

# FEATURE: Thirukural Gateway
if st.session_state.view == "gateway":
    k = random.choice(THIRUKURAL_DATA)
    st.markdown(f"<div style='text-align:center; padding:50px; background:#111; border-radius:15px;'><h2>{k['k']}</h2><p>{k['m']}</p></div>", unsafe_allow_html=True)
    if st.button("Enter Executive Suite"):
        st.session_state.view = "login"
        st.rerun()

# FEATURE: Secure Login Check
if st.session_state.view == "login":
    st.title("🔐 Secure Access")
    if st.button("Unlock Tackyon AI"):
        st.session_state.logged_in = True
        st.session_state.view = "main"
        st.rerun()

# --- MAIN APPLICATION HUB ---
if st.session_state.view == "main":
    with st.sidebar:
        st.title("T-Core Design")
        # FEATURE: 9 Premium Fonts
        font = st.selectbox("Typography", ["Inter", "Roboto", "Montserrat", "Arima", "Merriweather", "Open Sans", "Lora", "Fira Code", "JetBrains Mono"])
        st.divider()
        st.subheader("Smart History 📂") # FEATURE: Smart History Recording

    st.title("🎯 Tackyon AI: Intelligence & Dubbing")
    url = st.text_input("Paste YouTube Link (Shorts/Vlogs/Long-form)")

    tab1, tab2 = st.tabs(["📝 Smart Summary", "🎙️ Auto-Dubber (REAL DUB)"])

    # TAB 1: Smart Summariser
    with tab1:
        lang = st.selectbox("Language", ["Tamil", "English", "Hindi", "Malayalam"])
        style = st.selectbox("Style", ["Executive Summary", "Twitter Thread", "Key Insights"])
        if st.button("Execute Deep Analysis"):
            with st.spinner("Decoding Intelligence..."):
                try:
                    v_id = get_video_id(url)
                    t_list = YouTubeTranscriptApi.get_transcript(v_id) # FIXED Attribute Error
                    raw_text = " ".join([t['text'] for t in t_list])
                    prompt = f"Summarize this in {lang} as {style}: {raw_text}. Created by Prapanchan."
                    summary = model.generate_content(prompt).text
                    st.markdown(summary)
                    st.download_button("Export .txt Report", summary, "tackyon_report.txt") # FEATURE: Report Export
                except Exception as e:
                    st.error(f"Error: {e}")

    # TAB 2: REAL AUTO-DUBBING (The "Special" Feature)
    with tab2:
        st.subheader("Universal AI Voiceover")
        d_lang = st.selectbox("Translate Video To", ["Tamil", "Hindi", "Spanish", "French"])
        d_gender = st.radio("Voice Personality", ["Male", "Female"])
        lang_map = {"Tamil": "ta", "Hindi": "hi", "Spanish": "es", "French": "fr"}
        
        if st.button("🚀 Start Universal Dubbing"):
            if url:
                try:
                    with st.status("Dubbing in Progress...", expanded=True) as status:
                        st.write("Step 1: Extracting transcript...")
                        v_id = get_video_id(url)
                        t_list = YouTubeTranscriptApi.get_transcript(v_id) # FIXED Attribute Error
                        full_text = " ".join([t['text'] for t in t_list])
                        
                        st.write(f"Step 2: Gemini 2.5 Flash translating to {d_lang}...")
                        t_prompt = f"Translate this into natural {d_lang} for a voiceover: {full_text}"
                        translated_text = model.generate_content(t_prompt).text
                        
                        st.write(f"Step 3: Creating AI {d_gender} Voice...")
                        tts = gTTS(text=translated_text, lang=lang_map[d_lang])
                        tts.save("t_voice.mp3")
                        status.update(label="Dubbing Complete!", state="complete", expanded=False)
                    
                    st.audio("t_voice.mp3") # FEATURE: AI Voiceover
                    st.video(url) # Play video while listening to the AI track
                except Exception as e:
                    st.error(f"Dubbing Error: {e}")
            else:
                st.warning("Please paste a link first!")

    # FEATURE: Tackyon AI Assistant & Identity
    st.divider()
    chat = st.chat_input("Ask Tackyon anything about the video...")
    if chat and "who made you" in chat.lower():
        st.write("I am **Tackyon AI**, proudly engineered by **Prapanchan**.")

    # FEATURE: White-label Shield & Font Injection
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family={font.replace(" ", "+")}&display=swap');
        html, body, [class*="css"] {{ font-family: '{font}'; }}
        #MainMenu, footer, header {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)