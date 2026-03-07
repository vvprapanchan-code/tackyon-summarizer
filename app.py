import streamlit as st
import time
import base64
import os
import random
import json
import google.generativeai as genai
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi

# ==========================================
# 1. EXECUTIVE THEME & COSMETIC ARCHITECTURE
# ==========================================
st.set_page_config(
    page_title="Tackyon AI | Executive Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep-UI Styling for Premium Metallic Feel
st.markdown("""
    <style>
    /* Global UI Hiding */
    header, [data-testid="stHeader"], .stAppHeader {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Optimized Vertical Alignment */
    .block-container {
        padding-top: 0px !important;
        margin-top: -30px !important;
    }

    /* Kural Wisdom Bar - Golden Executive Design */
    .kural-box {
        background-color: #FFFFFF;
        border-bottom: 4px solid #D4AC0D;
        padding: 25px;
        text-align: center;
        width: 100%;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border-radius: 0 0 20px 20px;
    }
    .kural-line1 { 
        font-size: 1.6em; 
        font-weight: 800; 
        color: #1B2631; 
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    .kural-line2 { 
        font-size: 1.4em; 
        color: #5D6D7E; 
        font-style: italic;
        font-weight: 400;
    }

    /* Center-Stage Executive Card */
    .executive-card {
        background: #FFFFFF; 
        padding: 55px; 
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15); 
        border-top: 10px solid #1B2631;
        text-align: center; 
        max-width: 950px; 
        margin: auto;
        transition: transform 0.3s ease;
    }

    /* The Metallic T-Logo Pulse Animation */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(0,0,0,0)); brightness(100%); }
        50% { transform: scale(1.08); filter: drop-shadow(0 0 20px rgba(212, 172, 13, 0.4)); brightness(130%); }
        100% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(0,0,0,0)); brightness(100%); }
    }
    .pulse-layer { 
        animation: t-pulse 3s infinite ease-in-out; 
    }

    /* High-Definition Analysis Result Display */
    .analysis-result {
        background: #FDFEFE; 
        padding: 40px; 
        border-radius: 20px;
        border-left: 12px solid #1B2631; 
        text-align: left;
        margin-top: 30px; 
        color: #1C2833; 
        line-height: 2.0;
        font-size: 1.1em;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        box-shadow: inset 0 4px 15px rgba(0,0,0,0.05);
        border-right: 1px solid #EAECEE;
        border-bottom: 1px solid #EAECEE;
    }
    
    /* Custom Sidebar Branding */
    .sidebar-brand {
        text-align: center;
        padding: 20px;
        background: #F4F6F7;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGO ENGINE (MULTI-EXTENSION SUPPORT)
# ==========================================
def load_logo_proven():
    """Searches for logo file with robust error handling for double extensions."""
    try:
        search_list = ["logo.jpg", "logo.jpg.jpeg", "logo.jpeg", "tackyon logo.jpg"]
        for f in search_list:
            if os.path.exists(f):
                with open(f, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        # Secondary directory scan
        for file in os.listdir("."):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                with open(file, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None
    return None

logo_b64_data = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    """Universal logo renderer for onboarding and sidebar."""
    if logo_b64_data:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 25px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64_data}" style="width:{size}; border-radius: 25px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(f'<div style="text-align: center; font-size: 40px; font-weight: 900; color: #1B2631;">TACKYON AI</div>', unsafe_allow_html=True)

# ==========================================
# 3. WISDOM ENGINE (KURAL LOADER)
# ==========================================
def get_random_kural():
    """Pulls wisdom from the verified thirukural.json database."""
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except:
        pass
    # Global fallback verse
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# ==========================================
# 4. INTELLIGENCE DECODER (YOUTUBE + GEMINI 2.0)
# ==========================================
def get_video_data(url):
    """Extracts High-Fidelity metadata and transcripts."""
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': False}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info['id']
            metadata = {
                "title": info.get('title', 'Unknown Intelligence Resource'),
                "channel": info.get('uploader', 'Independent Authority'),
                "subs": info.get('subscriber_count', 'Private'),
                "likes": info.get('like_count', 'High Engagement'),
                "views": info.get('view_count', '0'),
                "description": info.get('description', 'No description provided.')[:1500]
            }
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([t['text'] for t in transcript_list])
                return metadata, transcript_text, "full"
            except:
                # Branding/Metadata fallback for Music or Shorts
                return metadata, None, "meta_only"
    except:
        return None, None, "error"

def generate_ai_analysis(transcript, metadata, style, lang, mode):
    """Core Intelligence Engine using Gemini 2.0 Flash."""
    try:
        # Secure API Configuration
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # DEFINED MODEL: Gemini 2.0 Flash (Latest Intelligence Engine)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Strict logic for exhaustive length
        length_constraint = "You must provide a minimum of 10-15 detailed paragraphs. Be extremely exhaustive, deep, and verbose."
        
        if mode == "meta_only":
            prompt = f"""
            Act as a Lead Intelligence Strategist. {length_constraint}
            The resource '{metadata['title']}' has no transcript (Music/Short). 
            Based on Title and Description: {metadata['description']}, 
            provide a massive {style} in {lang} language. 
            Analyze the cultural impact, branding, and creator authority in deep detail.
            """
        else:
            prompt = f"""
            Act as an Executive Analysis Officer. {length_constraint}
            Analyze this full transcript: {transcript}. 
            Generate a massive, world-class {style} in {lang} language. 
            Do not summarize briefly; explain every nuance, concept, and sub-topic mentioned in the video.
            """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"System Alert: AI Engine could not initialize. Please verify Gemini 2.0 Access. Error: {str(e)}"

# ==========================================
# 5. THE EXECUTIVE SYSTEM WORKFLOW
# ==========================================

# Initialize Session State
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = get_random_kural()

# --- STAGE 1: METALLIC STARTUP ANIMATION ---
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="400px", animate=True)
    time.sleep(2.8)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# --- STAGE 2: EXECUTIVE ONBOARDING ---
elif st.session_state.flow_stage == "onboarding":
    # Top Kural Box
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_value = st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="110px") 
    st.title("Executive Identification")
    st.write("Secure Intelligence Portal Entry")
    
    col1, col2, col3 = st.columns(3)
    with col1: user_name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with col2: user_gender = st.selectbox("Gender Identity", ["Male", "Female", "Executive", "Other"])
    with col3: user_age = st.number_input("System Age", 18, 99, 19)
    
    if st.button("Initialize Gateway", use_container_width=True):
        if user_name:
            st.session_state.user = {"name": user_name, "gender": user_gender, "age": user_age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- STAGE 3: INTELLIGENCE GATEWAY ---
elif st.session_state.flow_stage == "gateway":
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="95px")
    st.subheader("Reflection & Authentication")
    st.info(f"Identity Verified: Executive {st.session_state.user['name']}. Access Granted.")
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- STAGE 4: PRIMARY INTELLIGENCE HUB ---
else:
    # Sidebar Logo & Profile
    st.sidebar.markdown("<div class='sidebar-brand'>", unsafe_allow_html=True)
    render_t_logo(size="160px") 
    st.sidebar.markdown(f"**Executive:** {st.session_state.user['name']} <br> **Status:** Active", unsafe_allow_html=True)
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    st.write("Deep Resource Analysis Terminal")
    
    with st.expander("📥 Primary Resource Acquisition", expanded=True):
        url_input = st.text_input("Resource URL", placeholder="Paste YouTube Link (Vlogs, Music, or Shorts)")
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            intel_lang = st.selectbox("Intelligence Language", [
                "Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada", 
                "French", "German", "Spanish", "Japanese", "Chinese", "Arabic"
            ])
        with c2: 
            intel_style = st.selectbox("Analysis Output Style", [
                "Deep Comprehensive Summary", "Exhaustive Strategic Points", 
                "Full Exam Point of View", "Actionable Deep-Dive", "Twitter Intelligence Thread"
            ])
        with c3: 
            st.selectbox("Visual Typography", ["Inter Pro", "Arima Silk"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            if url_input:
                with st.spinner("Decrypting Resource Intelligence via Gemini 2.0..."):
                    v_meta, v_trans, v_mode = get_video_data(url_input)
                    
                    if v_mode == "error":
                        st.error("System Failure: Resource denied or connection interrupted.")
                    else:
                        st.markdown(f"### 📑 Analysis Report: {v_meta['title']}")
                        st.markdown(f"**Channel:** {v_meta['channel']} | **Authority:** {v_meta['subs']} Subs | **Engagement:** {v_meta['likes']} Likes")
                        
                        try:
                            # TRIGGER LONG-FORM AI ANALYSIS
                            final_result = generate_ai_analysis(v_trans, v_meta, intel_style, intel_lang, v_mode)
                            st.markdown(f'<div class="analysis-result"><b>{intel_style} ({intel_lang}):</b><br><br>{final_result}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.warning("AI Node Interrupted. Displaying metadata summary:")
                            st.markdown(f'<div class="analysis-result">{v_meta["description"]}</div>', unsafe_allow_html=True)
            else:
                st.warning("Action Required: A valid YouTube URL is mandatory.")

# --- END OF 275+ LINE BUILD ---