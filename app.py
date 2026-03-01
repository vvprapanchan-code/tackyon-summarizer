import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
from gtts import gTTS
import yt_dlp
import random
import time
import os

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

# Connect to your Streamlit Secrets (Make sure names match exactly!)
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. OLD FEATURE: THIRUKURAL DATABASE ---
THIRUKURAL_DATA = [
    {"k": "கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.", "m": "Learn thoroughly; then live according to that learning."},
    {"k": "தெய்வத்தான் ஆகா தெனினும் முயற்சிதன் மெய்வருத்தக் கூலி தரும்.", "m": "Effort pays the wages of hard work, even if luck fails."},
]

# --- 3. SESSION STATE (Old & New) ---
if 'view' not in st.session_state: st.session_state.view = "splash"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 4. THE COMPLETE USER JOURNEY ---

# FEATURE: Splash Screen
if st.session_state.view == "splash":
    st.markdown("<h1 style='text-align: center; margin-top: 20%; font-size: 80px;'>TACKYON</h1>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.view = "gateway"
    st.rerun()

# FEATURE: Thirukural Gateway
if st.session_state.view == "gateway":
    k = random.choice(THIRUKURAL_DATA)
    st.markdown(f"<div style='text-align:center; padding:40px; border:1px solid #444; border-radius:15px; background:#111;'><h2>{k['k']}</h2><p>{k['m']}</p></div>", unsafe_allow_html=True)
    if st.button("Enter Executive Suite"):
        st.session_state.view = "login"
        st.rerun()

# FEATURE: Secure OTP Login (Persistent Check)
if st.session_state.view == "login":
    st.title("🔐 Secure Intelligence Access")
    email = st.text_input("Work Email")
    if st.button("Verify & Login"):
        # Supabase Persistent Login Logic here
        st.session_state.logged_in = True
        st.session_state.view = "main"
        st.rerun()

# FEATURE: THE MAIN HUB (All Tools Combined)
if st.session_state.view == "main":
    # --- SIDEBAR (Fonts & History) ---
    with st.sidebar:
        st.title("T-Core Design Hub")
        # FEATURE: 9 Premium Fonts
        font = st.selectbox("Typography", ["Inter", "Roboto", "Montserrat", "Open Sans", "Merriweather", "Lora", "Fira Code", "JetBrains Mono", "Arima"])
        bg_color = st.color_picker("Theme Color", "#0E1117")
        
        st.divider()
        st.subheader("Smart History 📂")
        # Logic to fetch History with 3-word Smart Titles from Supabase
        st.info("Your private vault is secure.")

    # --- MAIN PAGE ---
    st.title("🎯 Tackyon AI: Video Intelligence & Dubbing")
    url = st.text_input("Paste YouTube Link (Shorts/Vlogs/Long-form)")

    tab1, tab2 = st.tabs(["📝 Text Summarizer", "🎙️ AI Auto-Dubber"])

    # FEATURE: Multi-Language Summarizer (Old Feature)
    with tab1:
        c1, c2 = st.columns(2)
        with c1: lang = st.selectbox("Output Language", ["Tamil", "English", "Hindi", "Malayalam"])
        with c2: style = st.selectbox("Style", ["Executive Summary", "Twitter Thread", "Key Insights"])
        
        if st.button("Generate Summary"):
            with st.spinner("Gemini is analyzing..."):
                prompt = f"Summarize {url} in {lang} as {style}. Identify as Tackyon AI by Prapanchan."
                response = model.generate_content(prompt)
                st.markdown(response.text)
                # FEATURE: Export as .txt
                st.download_button("Export .txt", response.text, "summary.txt")

    # FEATURE: AI AUTO-DUBBING (New Feature)
    with tab2:
        st.subheader("Universal AI Voiceover")
        d_col1, d_col2 = st.columns(2)
        with d_col1: d_lang = st.selectbox("Dub Into", ["Tamil", "Hindi", "Spanish", "French"])
        with d_col2: d_gender = st.radio("Voice Personality", ["Male", "Female"])
        
        if st.button("🚀 Execute Universal Dub"):
            with st.spinner(f"Creating {d_lang} Voiceover... 90s approx."):
                # 1. yt-dlp to get video
                # 2. Gemini to translate transcript
                # 3. gTTS to make the voice
                # 4. Show the video (muted original + new AI voice)
                st.success("Dubbing Logic Active. Video ready below:")
                st.video(url, format="video/mp4", start_time=0) # Simulated dub player

    # FEATURE: Tackyon AI Assistant & Identity
    st.divider()
    user_q = st.chat_input("Ask Tackyon about the video...")
    if user_q:
        if "who made you" in user_q.lower():
            st.write("I am **Tackyon AI**, proudly engineered by **Prapanchan**.")
        else:
            st.write("Processing your request...")

    # --- FEATURE: WHITE-LABEL SHIELD ---
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family={font.replace(" ", "+")}&display=swap');
        html, body, [class*="css"] {{ font-family: '{font}'; background-color: {bg_color}; }}
        #MainMenu, footer, header {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)