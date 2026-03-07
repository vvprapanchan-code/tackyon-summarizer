import streamlit as st
import time
import base64
import os
import random
import json
import google.generativeai as genai
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. THEME & EXECUTIVE ARCHITECTURE (PROTECTED) ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    header, [data-testid="stHeader"], .stAppHeader { display: none !important; visibility: hidden !important; }
    .block-container { padding-top: 0px !important; margin-top: -30px !important; }
    
    .kural-box {
        background-color: #FDFEFE;
        border-bottom: 3px solid #D4AC0D;
        padding: 20px;
        text-align: center;
        width: 100%;
        margin-bottom: 35px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .kural-line1 { font-size: 1.5em; font-weight: bold; color: #1B2631; margin-bottom: 8px; }
    .kural-line2 { font-size: 1.3em; color: #5D6D7E; font-style: italic; }

    .executive-card {
        background: white; 
        padding: 45px; 
        border-radius: 25px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.12); 
        border-top: 8px solid #1B2631;
        text-align: center; 
        max-width: 900px; 
        margin: auto;
    }

    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%); }
        50% { transform: scale(1.06); filter: brightness(130%); }
        100% { transform: scale(1); filter: brightness(100%); }
    }
    .pulse-layer { animation: t-pulse 2.5s infinite ease-in-out; }

    .analysis-result {
        background: #F8F9F9; 
        padding: 30px; 
        border-radius: 18px;
        border-left: 10px solid #1B2631; 
        text-align: left;
        margin-top: 25px; 
        color: #1C2833; 
        line-height: 1.8;
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO ENGINE ---
def load_logo_proven():
    try:
        search_list = ["logo.jpg", "logo.jpg.jpeg", "tackyon logo", "logo.jpeg"]
        for f in search_list:
            if os.path.exists(f):
                with open(f, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
        for file in os.listdir("."):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                with open(file, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return None
    return None

logo_data = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    if logo_data:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(f'<div class="{anim_class}" style="text-align: center; margin-bottom: 25px;"><img src="data:image/jpeg;base64,{logo_data}" style="width:{size}; border-radius: 20px;"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: center; font-size: 35px; font-weight: bold; color: #1B2631;">TACKYON AI</div>', unsafe_allow_html=True)

# --- 3. DATABASE ENGINE (KURAL) ---
def get_random_kural():
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except: pass
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 4. INTELLIGENCE ENGINE (SECURE & LONG) ---
def get_video_data(url):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            metadata = {
                "title": info.get('title', 'Unknown Resource'),
                "channel": info.get('uploader', 'Independent Creator'),
                "subs": info.get('subscriber_count', 'N/A'),
                "likes": info.get('like_count', 'N/A'),
                "description": info.get('description', '')[:1200]
            }
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(info['id'])
                transcript = " ".join([t['text'] for t in transcript_list])
                return metadata, transcript, "full"
            except: return metadata, None, "meta_only"
    except: return None, None, "error"

def generate_ai_analysis(transcript, metadata, style, lang, mode):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        long_instr = "Provide an extremely long, exhaustive, and detailed analysis. Do not summarize briefly."
        if mode == "meta_only":
            prompt = f"Act as a Brand Expert. {long_instr} No transcript available. Based on Title: {metadata['title']} and Description: {metadata['description']}, provide a {style} in {lang}."
        else:
            prompt = f"Act as an Executive Analyst. {long_instr} Analyze this transcript: {transcript}. Provide a professional and deep {style} in {lang} language."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Intelligence Hub Offline. Error: {str(e)}"

# --- 5. THE EXECUTIVE WORKFLOW WITH MEMORY ---

# CHECK IF USER IS ALREADY KNOWN (Permanent Memory Logic)
if "user" not in st.session_state:
    # Look for name in URL parameters (Simple Browser Memory)
    params = st.query_params
    if "exec_name" in params:
        st.session_state.user = {"name": params["exec_name"], "gender": "Executive", "age": 25}
        st.session_state.flow_stage = "hub"
    else:
        st.session_state.flow_stage = "animation"

if "daily_kural" not in st.session_state:
    st.session_state.daily_kural = get_random_kural()

# STAGE 1: ANIMATION
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="380px", animate=True)
    time.sleep(2.5)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: ONBOARDING
elif st.session_state.flow_stage == "onboarding":
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="100px") 
    st.title("Executive Onboarding")
    col1, col2, col3 = st.columns(3)
    with col1: u_name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with col2: u_gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with col3: u_age = st.number_input("Age", 18, 99, 19)
    if st.button("Initialize", use_container_width=True):
        if u_name:
            st.session_state.user = {"name": u_name, "gender": u_gender, "age": u_age}
            # SAVE TO BROWSER MEMORY
            st.query_params["exec_name"] = u_name
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: GATEWAY
elif st.session_state.flow_stage == "gateway":
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="90px")
    st.info(f"Identity Confirmed: Executive {st.session_state.user['name']}.")
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    render_t_logo(size="150px") 
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    if st.sidebar.button("Logout / Reset Memory"):
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    with st.expander("📥 Primary Resource Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
        c1, c2, c3 = st.columns(3)
        with c1: lang = st.selectbox("Language", ["Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada", "French", "German", "Spanish", "Japanese"])
        with c2: style = st.selectbox("Style", ["Comprehensive Long Summary", "Detailed Strategic Points", "Exam Preparation Guide", "Actionable Deep Dive"])
        with c3: st.selectbox("Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            if url:
                with st.spinner("Decrypting Intelligence..."):
                    m, t, mode = get_video_data(url)
                    if mode == "error": st.error("Access denied to the provided URL.")
                    else:
                        st.markdown(f"### 📑 Analysis Report: {m['title']}")
                        st.markdown(f"**Channel:** {m['channel']} | **Authority:** {m['subs']} Subs | **Engagement:** {m['likes']} Likes")
                        res = generate_ai_analysis(t, m, style, lang, mode)
                        st.markdown(f'<div class="analysis-result"><b>{style} Results ({lang}):</b><br><br>{res}</div>', unsafe_allow_html=True)