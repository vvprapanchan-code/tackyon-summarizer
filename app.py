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

# Using the fixed secret keys from your dashboard
try:
    GEMINI_KEY = st.secrets["GOOGLE_API_KEY"] 
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except KeyError as e:
    st.error(f"Secret Key Missing: {e}")
    st.stop()

genai.configure(api_key=GEMINI_KEY)
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

if st.session_state.view == "splash":
    st.markdown("<h1 style='text-align: center; margin-top: 20%; font-size: 80px; color: #00D4FF;'>TACKYON</h1>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.view = "gateway"
    st.rerun()

if st.session_state.view == "gateway":
    k = random.choice(THIRUKURAL_DATA)
    st.markdown(f"<div style='text-align:center; padding:50px; background:#111; color:white; border-radius:15px;'><h2>{k['k']}</h2><p>{k['m']}</p></div>", unsafe_allow_html=True)
    if st.button("Enter Executive Suite"):
        st.session_state.view = "login"
        st.rerun()

if st.session_state.view == "login":
    st.title("🔐 Secure Access")
    if st.button("Unlock Tackyon AI"):
        st.session_state.logged_in = True
        st.session_state.view = "main"
        st.rerun()

if st.session_state.view == "main":
    with st.sidebar:
        st.title("T-Core Design Hub")
        font = st.selectbox("Typography", ["Inter", "Roboto", "Arima"])
        bg_color = st.color_picker("Theme Color", "#0E1117")

    st.title("🎯 Tackyon AI: Video Intelligence")
    url = st.text_input("Paste YouTube Link")

    tab1, tab2 = st.tabs(["📝 Smart Summary", "🎙️ Auto-Dubber (REAL DUB)"])

    with tab1:
        if st.button("Execute Deep Analysis"):
            with st.spinner("Decoding Intelligence..."):
                prompt = f"Summarize {url} in Tamil. Identify as Tackyon AI created by Prapanchan."
                response = model.generate_content(prompt)
                st.markdown(response.text)

    # NEW: REAL DUBBING LOGIC
    with tab2:
        st.subheader("Universal AI Voiceover")
        d_lang = st.selectbox("Target Language", ["Tamil", "Hindi", "French"])
        lang_map = {"Tamil": "ta", "Hindi": "hi", "French": "fr"}
        
        if st.button("🚀 Start Universal Dubbing"):
            if url:
                with st.status("Dubbing in Progress...", expanded=True) as status:
                    # Step 1: Brain Analysis
                    st.write("Step 1: Gemini is translating the video script...")
                    t_prompt = f"Extract the main script from this video {url} and translate it perfectly into {d_lang} for a voiceover. Give only the translated text."
                    translated_script = model.generate_content(t_prompt).text
                    
                    # Step 2: Voice Generation
                    st.write(f"Step 2: Generating {d_lang} AI Voice...")
                    tts = gTTS(text=translated_script, lang=lang_map[d_lang])
                    tts.save("tackyon_voice.mp3")
                    
                    status.update(label="Dubbing Complete!", state="complete", expanded=False)
                
                st.success(f"Now playing {d_lang} Dub over the original video.")
                
                # Layout for Dubbed Experience
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.write("### AI Audio Track")
                    st.audio("tackyon_voice.mp3") # The actual generated voice
                with col_b:
                    st.write("### Visual Feed")
                    st.video(url) # Mute the volume on your device to hear the AI!
            else:
                st.warning("Please paste a link first, Boss!")

    # Identity & Shield
    st.divider()
    chat = st.chat_input("Ask Tackyon anything...")
    if chat and "who made you" in chat.lower():
        st.write("I am **Tackyon AI**, proudly engineered by **Prapanchan**.")

    st.markdown(f"<style>html, body, [class*='css'] {{ font-family: '{font}'; background-color: {bg_color}; }} #MainMenu, footer {{visibility: hidden;}}</style>", unsafe_allow_html=True)