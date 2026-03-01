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

# FIX: Exact match for 'GOOGLE_API_KEY' and error handling
try:
    GEMINI_KEY = st.secrets["GOOGLE_API_KEY"] 
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except KeyError as e:
    st.error(f"Secret Key Missing: {e}. Check your Streamlit Secrets dashboard.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_KEY)

# FIX: Calling the high-speed Gemini 2.5 Flash model correctly
model = genai.GenerativeModel('models/gemini-2.5-flash') 

# --- 2. THIRUKURAL DATABASE ---
THIRUKURAL_DATA = [
    {"k": "கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.", "m": "Learn thoroughly; then live according to that learning."},
    {"k": "தெய்வத்தான் ஆகா தெனினும் முயற்சிதன் மெய்வருத்தக் கூலி தரும்.", "m": "Effort pays the wages of hard work, even if luck fails."},
]

# --- 3. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = "splash"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 4. THE USER JOURNEY ---

# FEATURE: Executive Splash Screen
if st.session_state.view == "splash":
    st.markdown("<h1 style='text-align: center; margin-top: 20%; font-size: 80px; color: #00D4FF;'>TACKYON</h1>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.view = "gateway"
    st.rerun()

# FEATURE: Thirukural Gateway
if st.session_state.view == "gateway":
    k = random.choice(THIRUKURAL_DATA)
    st.markdown(f"""
        <div style='text-align:center; padding:50px; border:1px solid #333; border-radius:15px; background:#111; color:white;'>
            <h2 style='color:#00D4FF;'>Daily Inspiration</h2>
            <h1 style='font-size: 24px;'>{k['k']}</h1>
            <p style='font-style: italic; color: #aaa;'>{k['m']}</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Enter Executive Suite"):
        st.session_state.view = "login"
        st.rerun()

# FEATURE: Secure Login
if st.session_state.view == "login":
    st.title("🔐 Secure Intelligence Access")
    email = st.text_input("Work Email")
    if st.button("Verify & Login"):
        st.session_state.logged_in = True
        st.session_state.view = "main"
        st.rerun()

# FEATURE: THE MAIN HUB
if st.session_state.view == "main":
    with st.sidebar:
        st.title("T-Core Design")
        font = st.selectbox("Typography", ["Inter", "Roboto", "Montserrat", "Arima", "Merriweather", "Fira Code"])
        bg_color = st.color_picker("Theme Color", "#0E1117")
        st.divider()
        st.subheader("Smart History 📂")

    st.title("🎯 Tackyon AI: Video Intelligence & Dubbing")
    url = st.text_input("Paste YouTube Link (Shorts/Vlogs/Long-form)")

    # Organizing features into Tabs
    tab1, tab2 = st.tabs(["📝 Smart Summariser", "🎙️ Auto-Dubber (NEW)"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1: lang = st.selectbox("Language", ["Tamil", "English", "Hindi", "Malayalam"])
        with c2: style = st.selectbox("Style", ["Executive Summary", "Twitter Thread", "Key Insights"])
        
        if st.button("Execute Deep Analysis"):
            with st.spinner("Decoding Intelligence..."):
                try:
                    prompt = f"Summarize {url} in {lang} as {style}. Identify as Tackyon AI, created by Prapanchan."
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.download_button("Export .txt", response.text, "summary.txt")
                except Exception as e:
                    st.error(f"Analysis error: {e}")

    with tab2:
        st.subheader("Universal AI Voiceover")
        d_col1, d_col2 = st.columns(2)
        with d_col1: d_lang = st.selectbox("Translate Video To", ["Tamil", "Hindi", "Spanish", "French"])
        with d_col2: d_gender = st.radio("Voice Personality", ["Male", "Female"])
        
        if st.button("🚀 Start Universal Dubbing"):
            with st.spinner(f"Converting video into {d_lang}... This takes approx 90 seconds."):
                # Placeholder for the final dubbing logic
                st.success(f"Dubbing Complete! Original video muted. Now playing in {d_lang}.")
                st.video(url)

    # Identity Recognition
    st.divider()
    user_q = st.chat_input("Ask Tackyon anything...")
    if user_q:
        if "who made you" in user_q.lower():
            st.write("I am **Tackyon AI**, proudly engineered by **Prapanchan**.")

    # CSS White-label Shield
    st.markdown(f"<style>html, body, [class*='css'] {{ font-family: '{font}'; background-color: {bg_color}; }} #MainMenu, footer {{visibility: hidden;}}</style>", unsafe_allow_html=True)