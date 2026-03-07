import streamlit as st
import time
import base64
import os
import random
import json
import google.generativeai as genai
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi

# --- 1. THEME & DYNAMIC HEADER (EXECUTIVE ARCHITECTURE) ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* Hide default headers but keep space for our custom Kural bar */
    header, [data-testid="stHeader"], .stAppHeader {
        display: none !important;
        visibility: hidden !important;
    }
    
    .block-container {
        padding-top: 0px !important;
        margin-top: -30px !important;
    }

    /* Kural Box - Fixed at top with Golden Border */
    .kural-box {
        background-color: #FDFEFE;
        border-bottom: 2px solid #D4AC0D;
        padding: 15px;
        text-align: center;
        width: 100%;
        margin-bottom: 30px;
    }
    .kural-line1 { font-size: 1.4em; font-weight: bold; color: #1B2631; margin-bottom: 5px; }
    .kural-line2 { font-size: 1.2em; color: #5D6D7E; }

    /* Executive Card Styling - Polished and Professional */
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 6px solid #1B2631;
        text-align: center; max-width: 850px; margin: auto;
    }

    /* Metallic T-Pulse Animation - Every Startup */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%); }
        50% { transform: scale(1.05); filter: brightness(125%); }
        100% { transform: scale(1); filter: brightness(100%); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }

    /* Intelligence Result Display */
    .analysis-result {
        background: #F4F6F7; padding: 25px; border-radius: 15px;
        border-left: 8px solid #1B2631; text-align: left;
        margin-top: 20px; color: #1B2631; line-height: 1.7;
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PROVEN LOGO ENGINE (ROBUST SCANNER) ---
def load_logo_proven():
    """
    Scans the folder for logo.jpg or any image file. 
    Maintains the logo.jpg requirement.
    """
    try:
        # Search for specific names based on your GitHub file
        search_list = ["logo.jpg", "logo.jpg.jpeg", "tackyon logo", "logo.jpeg"]
        for f in search_list:
            if os.path.exists(f):
                with open(f, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        # Fallback: Deep folder scan
        for file in os.listdir("."):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                with open(file, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
    except:
        return None
    return None

logo_b64 = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    """Renders the metallic logo with optional pulse."""
    if logo_b64:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 20px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 15px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(f'<div style="text-align: center; font-size: 30px; font-weight: bold; color: #1B2631;">TACKYON AI</div>', unsafe_allow_html=True)

# --- 3. DATABASE ENGINE (1,330 / 50 KURAL LOADER) ---
def get_random_kural():
    """Loads random kural from the JSON you uploaded to GitHub."""
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except:
        pass
    # Safety Backup verse in 4-3 format
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 4. INTELLIGENCE ENGINE (THE BRAIN) ---
def get_video_data(url):
    """Extracts metadata and transcript. Error-proof for Music/Shorts."""
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info['id']
            metadata = {
                "title": info.get('title', 'Unknown Title'),
                "channel": info.get('uploader', 'Unknown Channel'),
                "subs": info.get('subscriber_count', 'Private'),
                "likes": info.get('like_count', 'N/A'),
                "views": info.get('view_count', '0'),
                "description": info.get('description', '')[:1000]
            }
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = " ".join([t['text'] for t in transcript_list])
                return metadata, transcript, "full"
            except:
                # No transcript mode (Music, Shorts, etc.)
                return metadata, None, "meta_only"
    except:
        return None, None, "error"

def generate_ai_analysis(transcript, metadata, style, lang, mode):
    """Connected to your verified Gemini API Key."""
    # YOUR VERIFIED KEY INTEGRATED HERE
    genai.configure(api_key="AIzaSyAowiGHQc-1BdRWbB0KMlyraQcsaT5ktBA")
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if mode == "meta_only":
        prompt = f"""
        Act as a professional YouTube brand analyst. This video has no transcript. 
        Based on the Title: {metadata['title']} and Description: {metadata['description']}, 
        provide a deep {style} in {lang} language. 
        Analyze the artist/creator, the channel's impact, and the content's purpose.
        """
    else:
        prompt = f"""
        Act as an Executive Intelligence Analyst. Analyze this transcript: {transcript}. 
        Provide a highly professional {style} in the {lang} language. 
        Highlight key takeaways, strategic insights, and essential data points.
        """
    
    response = model.generate_content(prompt)
    return response.text

# --- 5. THE EXECUTIVE FLOW (180+ LINES PRESERVED) ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = get_random_kural()

# STAGE 1: LOGO ANIMATION (Every opening)
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="350px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: ONBOARDING (Kural in top box + Logo)
elif st.session_state.flow_stage == "onboarding":
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="90px") 
    st.title("Executive Onboarding")
    st.write("Welcome to Tackyon AI Intelligence Portal")
    col1, col2, col3 = st.columns(3)
    with col1: name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with col2: gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with col3: age = st.number_input("Age", 18, 99, 19)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: GATEWAY (Same Kural + Logo)
elif st.session_state.flow_stage == "gateway":
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="80px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    st.info(f"Authorized: Executive {st.session_state.user['name']}. System Online.")
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB (Logo in sidebar, NO Kural)
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    render_t_logo(size="140px") 
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<h3 style='text-align: center;'>Executive: {st.session_state.user['name']}</h3>", unsafe_allow_html=True)
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link (Vlog, Music, or Shorts)")
        c1, c2, c3 = st.columns(3)
        with c1: lang = st.selectbox("Intelligence Language", [
            "Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada", 
            "French", "German", "Spanish", "Japanese", "Chinese"
        ])
        with c2: style = st.selectbox("Output Style", [
            "Executive Summary", "Strategic Points", "Exam Point of View", 
            "Twitter Thread", "Actionable Steps"
        ])
        with c3: st.selectbox("Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            if url:
                with st.spinner("Decrypting Intelligence..."):
                    meta, trans, mode = get_video_data(url)
                    if mode == "error":
                        st.error("Access Denied: Invalid URL or System Timeout.")
                    else:
                        st.markdown(f"### 📊 Analysis: {meta['title']}")
                        st.markdown(f"**Channel:** {meta['channel']} | **Subscribers:** {meta['subs']} | **Likes:** {meta['likes']}")
                        try:
                            result = generate_ai_analysis(trans, meta, style, lang, mode)
                            st.markdown(f'<div class="analysis-result"><b>{style} ({lang}):</b><br><br>{result}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.warning("AI Engine Offline. Showing metadata fallback:")
                            st.markdown(f'<div class="analysis-result">{meta["description"]}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please provide a valid YouTube Link.")