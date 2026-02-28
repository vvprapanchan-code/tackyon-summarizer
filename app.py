import streamlit as st
import google.generativeai as genai
from supabase import create_client, Client
import random
import time

# --- 1. CONFIGURATION & CORE SETUP ---
st.set_page_config(page_title="Tackyon AI Summariser", page_icon="🎯", layout="wide")

# Replace with your actual secrets from .streamlit/secrets.toml
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)

# --- 2. THE THIRUKURAL DATABASE ---
THIRUKURAL_DATA = [
    {"kural": "அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு.", "meaning": "As the letter A is the first of all letters, so the ancient God is first in the world."},
    {"kural": "கற்க கசடறக் கற்பவை கற்றபின்\nநிற்க அதற்குத் தக.", "meaning": "Learn thoroughly what is to be learned, and then live according to that learning."},
    {"kural": "தெய்வத்தான் ஆகா தெனினும் முயற்சிதன்\nமெய்வருத்தக் கூலி தரும்.", "meaning": "Even if God cannot help, effort will pay the wages of the body's hard work."},
    {"kural": "எப்பொருள் யார்யார்வாய்க் கேட்பினும் அப்பொருள்\nமெய்ப்பொருள் காண்ப தறிவு.", "meaning": "To discern the truth in everything, no matter who says it, is wisdom."},
    {"kural": "தொட்டனைத் தூறும் மணற்கேணி மாந்தர்க்குக்\nகற்றனைத் தூறும் அறிவு.", "meaning": "As water flows from a sandy well as deep as you dig, so wisdom flows as deep as you learn."}
]

# --- 3. CUSTOM CSS: FONTS, SHIELD & SPLASH ---
font_map = {
    "Inter": "Inter", "Roboto": "Roboto", "Montserrat": "Montserrat", 
    "Open Sans": "Open Sans", "Merriweather": "Merriweather", "Lora": "Lora",
    "Fira Code": "Fira Code", "JetBrains Mono": "JetBrains Mono", "Arima": "Arima"
}

# --- 4. SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'view' not in st.session_state:
    st.session_state.view = "splash" # splash -> gateway -> login -> main

# --- 5. THE WORKFLOW LOGIC ---

# A. Splash Screen (Animation Simulation)
if st.session_state.view == "splash":
    st.markdown("<h1 style='text-align: center; margin-top: 20%;'>🚀 TACKYON</h1>", unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.view = "gateway"
    st.rerun()

# B. Thirukural Gateway
if st.session_state.view == "gateway":
    k = random.choice(THIRUKURAL_DATA)
    st.markdown(f"""
        <div style="text-align:center; padding: 50px; border: 2px solid #ddd; border-radius: 15px; margin-top: 10%;">
            <h2 style="color: #1E3A8A;">Daily Inspiration</h2>
            <h3 style="font-family: 'Arima', cursive;">{k['kural']}</h3>
            <p style="font-style: italic;">{k['meaning']}</p>
            <br>
            <button onclick="window.location.reload()">Enter App</button>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Proceed to Tackyon AI"):
        st.session_state.view = "login"
        st.rerun()

# C. Login & Persistent Check
if st.session_state.view == "login":
    # (Simplified for space: insert your existing Supabase OTP Login code here)
    st.title("🔒 Tackyon Secure Login")
    email = st.text_input("Enter Email")
    if st.button("Send OTP"):
        # Logic to send OTP via Supabase
        st.success("OTP Sent! (Persistence Enabled)")
        # On success:
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.session_state.view = "main"
        st.rerun()

# D. Main Application
if st.session_state.view == "main":
    # Sidebar Configuration
    with st.sidebar:
        st.image("https://your-logo-url.com/logo.png", width=100) # Replace with your T-Core logo
        st.title("Design Hub")
        sel_font = st.selectbox("Choose Typography", list(font_map.keys()))
        bg_color = st.color_picker("App Theme Color", "#0E1117")
        
        st.divider()
        st.subheader("Smart History 📂")
        # Logic to fetch history from Supabase for st.session_state.user_email
        # for item in history: st.button(item['smart_title'])
        
    # Main UI
    st.title("🎯 Tackyon AI Executive Summariser")
    url = st.text_input("Paste YouTube Link (Video/Shorts/Vlog)")
    
    col1, col2 = st.columns(2)
    with col1:
        lang = st.selectbox("Output Language", ["Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada"])
    with col2:
        style = st.selectbox("Intelligence Style", ["Executive Summary", "Twitter Thread", "Key Insights"])

    if st.button("🚀 Execute Deep Analysis"):
        with st.spinner("Gemini is decoding video intelligence..."):
            # 1. Extract transcript (yt-dlp)
            # 2. genai.generate_content -> summary
            # 3. Generate Smart Title
            # 4. Save to Supabase
            st.write(f"### {style} Analysis in {lang}")
            st.info("The summary would appear here based on the video context.")
            
            # Export Feature
            st.download_button("Download .txt Report", "Sample summary content", "tackyon_report.txt")

    # Tackyon AI Assistant
    st.divider()
    st.subheader("💬 Talk to Tackyon Assistant")
    user_q = st.chat_input("Ask me anything about the video...")
    if user_q:
        if "who made you" in user_q.lower():
            st.chat_message("assistant").write("I am a product of Tackyon, proudly created by **Prapanchan**.")
        else:
            st.chat_message("assistant").write("Analyzing your question based on the video data...")

# --- 6. GLOBAL CSS INJECTION (The Shield) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family={font_map[sel_font if 'sel_font' in locals() else 'Inter']}&display=swap');
    
    /* Shield: Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    html, body, [class*="css"] {{
        font-family: '{font_map[sel_font if 'sel_font' in locals() else 'Inter']}', sans-serif;
        background-color: {bg_color if 'bg_color' in locals() else '#0E1117'};
    }}
    </style>
""", unsafe_allow_html=True)