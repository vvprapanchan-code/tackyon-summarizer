import streamlit as st
import time
import base64
import os
import random
import uuid
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
from datetime import datetime

# ==========================================
# STAGE 1: EXECUTIVE DESIGN SYSTEM (CSS)
# ==========================================
st.set_page_config(page_title="Tackyon AI", page_icon="🎙️", layout="centered")

def apply_executive_theme(font_name="Inter", accent="#1B2631"):
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Playfair+Display:wght@700&display=swap');
        
        /* Hide Streamlit Branding */
        header, [data-testid="stHeader"], .stAppHeader {{ display: none !important; }}
        footer {{ visibility: hidden; }}
        
        /* Main Workspace App-like feel */
        .stApp {{ background-color: #F8F9FA; }}
        .block-container {{ padding: 2rem !important; max-width: 600px !important; }}
        
        /* Single Column Card Design */
        .executive-card {{
            background: white; padding: 30px; border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 20px;
            border: 1px solid #EDEDED; font-family: '{font_name}', sans-serif;
        }}
        
        /* 4-3 Thirukural Formatting */
        .kural-box {{
            text-align: center; padding: 40px 20px; background: #1B2631;
            color: #D4AC0D; border-radius: 20px; margin-bottom: 30px;
        }}
        .kural-line-1 {{ font-size: 1.5em; font-weight: 700; margin-bottom: 10px; word-spacing: 15px; }}
        .kural-line-2 {{ font-size: 1.3em; font-weight: 500; word-spacing: 15px; opacity: 0.9; }}

        /* T-Logo Splash Animation */
        .logo-container {{
            display: flex; justify-content: center; align-items: center; height: 80vh;
        }}
        .metallic-t {{
            font-size: 100px; font-weight: 900; color: #1B2631;
            animation: pulse 2s infinite ease-in-out;
        }}
        @keyframes pulse {{ 0% {{ transform: scale(1); opacity: 1; }} 50% {{ transform: scale(1.1); opacity: 0.7; }} 100% {{ transform: scale(1); opacity: 1; }} }}
        
        /* Assistant Bubble */
        .assistant-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 15px; }}
        .assistant-logo {{ width: 30px; height: 30px; background: #1B2631; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 14px; }}
        
        /* Watermark */
        .t-watermark {{ text-align: right; font-size: 10px; color: #BDC3C7; font-weight: 900; letter-spacing: 2px; margin-top: 10px; }}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# STAGE 2: DATA & IDENTITY ENGINES
# ==========================================

def get_kural():
    """Returns random Kural in 4-3 word format."""
    kurals = [
        {"l1": "அகர முதல எழுத்தெல்லாம்", "l2": "ஆதி பகவன் முதற்றே உலகு"},
        {"l1": "கற்க கசடறக் கற்பவை", "l2": "கற்றபின் நிற்க அதற்குத் தக"},
        {"l1": "எப்பொருள் யார்யார்வாய்க் கேட்பினும்", "l2": "அப்பொருள் மெய்ப்பொருள் காண்ப தறிவு"}
    ]
    return random.choice(kurals)

def get_logo():
    """Fetches T-Logo from Local/GitHub Assets."""
    for ext in ['png', 'jpg', 'jpeg']:
        path = f"t_logo.{ext}"
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

# ==========================================
# STAGE 3: CORE INTELLIGENCE (GEMINI 2.5)
# ==========================================

def extract_intelligence(url):
    """Bypasses errors to get any content available."""
    try:
        v_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
        raw_t = YouTubeTranscriptApi.get_transcript(v_id)
        return " ".join([t['text'] for t in raw_t]), "Full Analysis"
    except:
        try:
            with YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return f"Title: {info['title']}. Description: {info.get('description','')}", "Metadata Summary"
        except: return "No data found.", "Error"

def ask_tackyon(content, prompt, lang):
    """Gemini 2.5 Flash Processor."""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        full_p = f"Translate to {lang} and answer precisely as Tackyon AI: {prompt}. Content: {content[:5000]}"
        return model.generate_content(full_p).text
    except: return "Intelligence Engine Busy."

# ==========================================
# STAGE 4: THE APP FLOW
# ==========================================

if "page" not in st.session_state: st.session_state.page = "splash"
if "theme" not in st.session_state: st.session_state.theme = {"font": "Inter", "color": "#1B2631"}

apply_executive_theme(st.session_state.theme["font"], st.session_state.theme["color"])

# --- SPLASH SCREEN (LOGO ANIMATION) ---
if st.session_state.page == "splash":
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    logo_b64 = get_logo()
    if logo_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150" style="animation: pulse 2s infinite;">', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metallic-t">T</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.page = "onboarding"
    st.rerun()

# --- ONBOARDING (NAME/AGE/GENDER) ---
elif st.session_state.page == "onboarding":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.subheader("Personalize Workspace")
    name = st.text_input("First Name")
    age = st.number_input("Age", 18, 99, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    if st.button("Initialize Tackyon"):
        if name:
            st.session_state.user = {"name": name, "age": age, "gender": gender}
            st.session_state.page = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- THIRUKURAL GATEWAY (4-3 FORMAT) ---
elif st.session_state.page == "gateway":
    k = get_kural()
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line-1">{k['l1']}</div>
            <div class="kural-line-2">{k['l2']}</div>
            <p style="margin-top:30px; font-size:10px; letter-spacing:3px;">INITIALIZING...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.page = "workspace"
    st.rerun()

# --- THE MAIN WORKSPACE ---
else:
    # Sidebar Command Center
    with st.sidebar:
        st.subheader("Theme & Typography")
        st.session_state.theme["font"] = st.radio("Font Selection", ["Inter", "Playfair Display"])
        st.session_state.theme["color"] = st.color_picker("Accent Color", "#1B2631")
        st.markdown("---")
        st.caption(f"User: {st.session_state.user['name']}")
        st.caption(f"Tackyon ID: {uuid.uuid4().hex[:8].upper()}")

    st.title(f"Tackyon AI")
    
    # SINGLE COLUMN INPUT
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    url = st.text_input("Paste YouTube URL Here", placeholder="https://youtube.com/...")
    
    lang_list = ["Tamil", "English", "French", "German", "Hindi", "Japanese", "Spanish", "Arabic", "Russian", "Korean", "Chinese", "Italian"]
    lang = st.selectbox("Intelligence Language", lang_list)
    
    style = st.selectbox("Style", ["Executive Summary", "Key Insights", "Exam Point of View", "Twitter Thread"])
    format_type = st.selectbox("Format", ["Point-wise Bullets", "Clean Paragraphs"])
    
    if st.button("Generate Intelligence Report", use_container_width=True):
        if url:
            data, source = extract_intelligence(url)
            report = ask_tackyon(data, f"Give me a {style} in {format_type}", lang)
            st.session_state.last_report = report
            st.markdown(f"""
                <div style="background:#F1F2F6; padding:20px; border-radius:15px; margin-top:20px;">
                    <p style="white-space: pre-wrap;">{report}</p>
                    <div class="t-watermark">TACKYON T</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Export Option
            st.download_button("📥 Download Branded Report", f"TACKYON REPORT\n\n{report}\n\n(T) Symbol - Branded", file_name="Tackyon_Report.txt")
    st.markdown('</div>', unsafe_allow_html=True)

    # TACKYON ASSISTANT (CARD WITH LOGO)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<div class="assistant-header"><div class="assistant-logo">T</div><b>Tackyon Assistant</b></div>', unsafe_allow_html=True)
    if "chat" not in st.session_state: st.session_state.chat = []
    
    user_q = st.chat_input("Ask about the video...")
    if user_q:
        ans = ask_tackyon(st.session_state.get('last_report', ''), user_q, lang)
        st.session_state.chat.append({"q": user_q, "a": ans})
        
    for c in st.session_state.chat:
        st.write(f"👤: {c['q']}")
        st.write(f"🎙️: {c['a']}")
    st.markdown('</div>', unsafe_allow_html=True)