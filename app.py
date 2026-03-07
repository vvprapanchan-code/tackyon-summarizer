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
    /* 1. HIDE DEFAULT UI ELEMENTS */
    header, [data-testid="stHeader"], .stAppHeader {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 2. PAGE SPACING OPTIMIZATION */
    .block-container {
        padding-top: 0px !important;
        margin-top: -30px !important;
    }

    /* 3. KURAL BOX - THE WISDOM BAR */
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

    /* 4. EXECUTIVE CARD DESIGN */
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

    /* 5. METALLIC T-PULSE ANIMATION */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%); }
        50% { transform: scale(1.06); filter: brightness(130%); }
        100% { transform: scale(1); filter: brightness(100%); }
    }
    .pulse-layer { animation: t-pulse 2.5s infinite ease-in-out; }

    /* 6. INTELLIGENCE OUTPUT BOX */
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
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PROVEN LOGO ENGINE (ROBUST SCANNER) ---
def load_logo_proven():
    """
    Scans the local directory for the logo file.
    Supports specific Tackyon filenames.
    """
    try:
        # Check for specific files detected in your environment
        search_list = ["logo.jpg", "logo.jpg.jpeg", "tackyon logo", "logo.jpeg"]
        for f in search_list:
            if os.path.exists(f):
                with open(f, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        # Fallback for generic image files
        for file in os.listdir("."):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                with open(file, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
    except:
        return None
    return None

logo_b64_data = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    """Renders the logo with a professional pulse effect."""
    if logo_b64_data:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 25px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64_data}" style="width:{size}; border-radius: 20px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(f'<div style="text-align: center; font-size: 35px; font-weight: bold; color: #1B2631; margin-bottom:20px;">TACKYON AI</div>', unsafe_allow_html=True)

# --- 3. DATABASE ENGINE (KURAL RETRIEVAL) ---
def get_random_kural():
    """Accesses the 50-verse JSON database you created."""
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except Exception as e:
        pass
    # Professional fallback verse
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 4. THE INTELLIGENCE ENGINE (SECURED) ---
def get_video_data(url):
    """Extracts YouTube metadata and transcripts."""
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': False}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info['id']
            metadata = {
                "title": info.get('title', 'Unknown Resource'),
                "channel": info.get('uploader', 'Independent Creator'),
                "subs": info.get('subscriber_count', 'N/A'),
                "likes": info.get('like_count', 'N/A'),
                "views": info.get('view_count', '0'),
                "description": info.get('description', '')[:1200]
            }
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([t['text'] for t in transcript_list])
                return metadata, transcript_text, "full"
            except:
                # Meta-only mode for music/shorts
                return metadata, None, "meta_only"
    except Exception as e:
        return None, None, "error"

def generate_ai_analysis(transcript, metadata, style, lang, mode):
    """Generates AI insights using SECURE Streamlit secrets."""
    try:
        # SECURE CONFIGURATION
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if mode == "meta_only":
            prompt = f"""
            Act as a Strategic Brand Consultant. This content has no transcript (Music/Short). 
            Based on Title: {metadata['title']} and Description: {metadata['description']}, 
            provide a {style} in {lang} language. 
            Analyze the creative impact and channel authority.
            """
        else:
            prompt = f"""
            Act as an Executive Intelligence Officer. Analyze this transcript: {transcript}. 
            Provide a world-class {style} in the {lang} language. 
            Focus on strategic takeaways and actionable wisdom.
            """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"System Alert: AI Engine could not initialize. Error: {str(e)}"

# --- 5. THE EXECUTIVE WORKFLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = get_random_kural()

# STAGE 1: LOGO ANIMATION (Every startup)
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="380px", animate=True)
    time.sleep(2.5)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: ONBOARDING
elif st.session_state.flow_stage == "onboarding":
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="100px") 
    st.title("Executive Identification")
    st.write("Welcome to the Tackyon AI Intelligence Gateway")
    col1, col2, col3 = st.columns(3)
    with col1: user_name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with col2: user_gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with col3: user_age = st.number_input("Age", 18, 99, 19)
    
    if st.button("Initialize System", use_container_width=True):
        if user_name:
            st.session_state.user = {"name": user_name, "gender": user_gender, "age": user_age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: GATEWAY
elif st.session_state.flow_stage == "gateway":
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="90px")
    st.subheader("System Readiness Confirmed")
    st.info(f"Identity Verified: Executive {st.session_state.user['name']}.")
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    render_t_logo(size="150px") 
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<h3 style='text-align: center;'>Executive: {st.session_state.user['name']}</h3>", unsafe_allow_html=True)
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    with st.expander("📥 Primary Resource Acquisition", expanded=True):
        url_input = st.text_input("Resource URL", placeholder="Paste YouTube Link (Vlogs, Music, or Shorts)")
        c1, c2, c3 = st.columns(3)
        with c1: intelligence_lang = st.selectbox("Intelligence Language", [
            "Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada", 
            "French", "German", "Spanish", "Japanese", "Chinese"
        ])
        with c2: intelligence_style = st.selectbox("Output Style", [
            "Executive Summary", "Strategic Points", "Exam Point of View", 
            "Twitter Thread", "Threads Post", "Actionable Steps"
        ])
        with c3: st.selectbox("Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            if url_input:
                with st.spinner("Decrypting Intelligence..."):
                    v_meta, v_trans, v_mode = get_video_data(url_input)
                    if v_mode == "error":
                        st.error("System Failure: Access denied to the provided URL.")
                    else:
                        st.markdown(f"### 📑 Analysis Report: {v_meta['title']}")
                        st.markdown(f"**Channel:** {v_meta['channel']} | **Authority:** {v_meta['subs']} Subs | **Engagement:** {v_meta['likes']} Likes")
                        try:
                            final_result = generate_ai_analysis(v_trans, v_meta, intelligence_style, intelligence_lang, v_mode)
                            st.markdown(f'<div class="analysis-result"><b>{intelligence_style} ({intelligence_lang}):</b><br><br>{final_result}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.warning("AI Node Interrupted. Showing metadata summary:")
                            st.markdown(f'<div class="analysis-result">{v_meta["description"]}</div>', unsafe_allow_html=True)
            else:
                st.warning("Action Required: Please provide a valid Resource URL.")