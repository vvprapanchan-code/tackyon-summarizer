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

# Matching your exact 'GOOGLE_API_KEY' from Secrets dashboard
try:
    GEMINI_KEY = st.secrets["GOOGLE_API_KEY"] 
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except KeyError as e:
    st.error(f"⚠️ Secret Missing: {e}. Check Streamlit Secrets!")
    st.stop()

# Configure Gemini 2.5 Flash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash') 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. UTILITY: EXTRACT VIDEO ID ---
def get_video_id(url):
    """Extracts ID from any YouTube link (Standard, Shorts, or Mobile)."""
    reg = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(reg, url)
    return match.group(1) if match else None

# --- 3. THIRUKURAL DATABASE ---
THIRUKURAL_DATA = [
    {"k": "கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.", "m": "Learn thoroughly; then live according to that learning."},
    {"k": "தெய்வத்தான் ஆகா தெனினும் முயற்சிதன் மெய்வருத்தக் கூலி தரும்.", "m": "Effort pays the wages of hard work, even if luck fails."},
]

# --- 4. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = "splash"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 5. THE USER JOURNEY ---

# Splash Screen
if st.session_state.view == "splash":
    st.markdown("<h1 style='text-align: center; margin-top: 20%; font-size: 80px; color: #00D4FF;'>TACKYON</h1>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.view = "gateway"
    st.rerun()

# Thirukural Gateway
if st.session_state.view == "gateway":
    k = random.choice(THIRUKURAL_DATA)
    st.markdown(f"<div style='text-align:center; padding:50px; background:#111; border-radius:15px;'><h2>{k['k']}</h2><p>{k['m']}</p></div>", unsafe_allow_html=True)
    if st.button("Enter Executive Suite"):
        st.session_state.view = "login"
        st.rerun()

# Login & Main Hub
if st.session_state.view == "login":
    st.title("🔐 Secure Access")
    if st.button("Unlock Tackyon AI"):
        st.session_state.logged_in = True
        st.session_state.view = "main"
        st.rerun()

if st.session_state.view == "main":
    with st.sidebar:
        st.title("T-Core Design")
        font = st.selectbox("Typography", ["Inter", "Roboto", "Arima"])
        st.divider()
        st.subheader("Smart History 📂")

    st.title("🎯 Tackyon AI: Intelligence Hub")
    url = st.text_input("Paste YouTube Link")

    tab1, tab2 = st.tabs(["📝 Smart Summary", "🎙️ Auto-Dubber (REAL DUB)"])

    # TAB 1: Smart Summariser
    with tab1:
        lang = st.selectbox("Language", ["Tamil", "English", "Hindi"])
        if st.button("Execute Deep Analysis"):
            with st.spinner("Decoding..."):
                try:
                    v_id = get_video_id(url)
                    t_list = YouTubeTranscriptApi.get_transcript(v_id) # FIXED TYPO
                    raw_text = " ".join([t['text'] for t in t_list])
                    prompt = f"Summarize this in {lang}: {raw_text}. Identify as Tackyon AI by Prapanchan."
                    st.markdown(model.generate_content(prompt).text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # TAB 2: REAL AUTO-DUBBING
    with tab2:
        st.subheader("Universal AI Voiceover")
        d_lang = st.selectbox("Translate Video To", ["Tamil", "Hindi", "French"])
        d_gender = st.radio("Voice Personality", ["Male", "Female"])
        lang_map = {"Tamil": "ta", "Hindi": "hi", "French": "fr"}
        
        if st.button("🚀 Start Universal Dubbing"):
            if url:
                try:
                    with st.status("Dubbing in Progress...", expanded=True) as status:
                        st.write("Step 1: Extracting script...")
                        v_id = get_video_id(url)
                        t_list = YouTubeTranscriptApi.get_transcript(v_id) # FIXED TYPO
                        full_text = " ".join([t['text'] for t in t_list])
                        
                        st.write(f"Step 2: Translating to {d_lang}...")
                        t_prompt = f"Translate this for a voiceover into natural {d_lang}: {full_text}"
                        translated_text = model.generate_content(t_prompt).text
                        
                        st.write(f"Step 3: Creating {d_gender} Audio...")
                        tts = gTTS(text=translated_text, lang=lang_map[d_lang])
                        tts.save("t_voice.mp3")
                        status.update(label="Complete!", state="complete", expanded=False)
                    
                    st.audio("t_voice.mp3")
                    st.video(url)
                except Exception as e:
                    st.error(f"Dubbing Error: {e}")
            else:
                st.warning("Please paste a link!")

    # Identity Recognition
    st.divider()
    chat = st.chat_input("Ask Tackyon anything...")
    if chat and "who made you" in chat.lower():
        st.write("I am **Tackyon AI**, proudly engineered by **Prapanchan**.")

    st.markdown(f"<style>html, body, [class*='css'] {{ font-family: '{font}'; }} #MainMenu, footer {{visibility: hidden;}}</style>", unsafe_allow_html=True)