import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import os
import random
import json
import uuid
import google.generativeai as genai
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
from gtts import gTTS

# --- 1. THEME & EXECUTIVE ARCHITECTURE (PROTECTED) ---
# This section defines the visual identity of Tackyon AI
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
        margin-bottom: 30px;
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

    .ad-slot-frame {
        margin-top: 20px;
        padding: 15px;
        border: 1px dashed #BDC3C7;
        border-radius: 12px;
        background: #F4F6F7;
    }

    .report-watermark {
        text-align: right; 
        font-size: 10px; 
        color: #BDC3C7;
        font-weight: 900; 
        letter-spacing: 2px; 
        margin-top: 15px;
    }

    .assistant-header {
        display: flex; align-items: center; margin-top: 30px;
        padding: 15px; background: #1B2631; color: white; border-radius: 15px 15px 0 0;
    }
    .assistant-icon {
        width: 30px; height: 30px; background: white; color: #1B2631;
        border-radius: 50%; display: flex; align-items: center;
        justify-content: center; font-weight: 900; margin-right: 12px;
    }
    .assistant-body {
        background: white; border: 1px solid #1B2631;
        border-radius: 0 0 15px 15px; padding: 20px; margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. IDENTITY PERSISTENCE ENGINE ---
# Ensures the user only fills details once
USER_CONFIG = "tackyon_user.json"

def save_identity(data):
    with open(USER_CONFIG, "w") as f:
        json.dump(data, f)

def load_identity():
    if os.path.exists(USER_CONFIG):
        with open(USER_CONFIG, "r") as f:
            return json.load(f)
    return None

# --- 3. LOGO ENGINE (STABLE SCANNER) ---
def load_logo_proven():
    try:
        search_list = ["logo.jpg", "logo.png", "logo.jpeg"]
        for f in search_list:
            if os.path.exists(f):
                with open(f, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return None
    return None

logo_data = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    if logo_data:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(f'<div class="{anim_class}" style="text-align: center; margin-bottom: 25px;"><img src="data:image/jpeg;base64,{logo_data}" style="width:{size}; border-radius: 20px;"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: center; font-size: 35px; font-weight: bold; color: #1B2631;">TACKYON AI</div>', unsafe_allow_html=True)

# --- 4. DATABASE ENGINE (KURAL LOADER) ---
def get_random_kural():
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except: pass
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 5. SAFE AD ENGINE (TEST MODE) ---
def render_tackyon_ad(is_test=True):
    """Renders official Google Test Ads to prevent account blocking."""
    st.markdown('<div class="ad-slot-frame">', unsafe_allow_html=True)
    st.caption("STRATEGIC PARTNER ADVERTISEMENT (TEST MODE ACTIVE)")
    
    # Official Google Test Publisher ID
    pub_id = "ca-pub-3940256099942544" if is_test else "YOUR_REAL_PUB_ID"
    
    ad_code = f"""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={pub_id}"
     crossorigin="anonymous"></script>
    <ins class="adsbygoogle"
     style="display:block"
     data-ad-client="{pub_id}"
     data-ad-slot="YOUR_SLOT_ID"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
    <script> (adsbygoogle = window.adsbygoogle || []).push({{}}); </script>
    """
    components.html(ad_code, height=200)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. INTELLIGENCE & DUBBING ENGINES ---
def get_video_data(url):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            metadata = {
                "title": info.get('title', 'Unknown Resource'),
                "channel": info.get('uploader', 'Independent Creator'),
                "desc": info.get('description', '')[:1500],
                "id": info.get('id', '')
            }
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(info['id'])
                transcript = " ".join([t['text'] for t in transcript_list])
                return metadata, transcript, "full"
            except: return metadata, None, "meta_only"
    except: return None, None, "error"

def generate_ai_analysis(transcript, metadata, style, lang, mode):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        context = transcript if transcript else metadata['desc']
        prompt = f"Act as Tackyon AI Executive Analyst. Summarize this for {style} in {lang}: {context}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Intelligence Offline. Error: {str(e)}"

def run_neural_dub(transcript, metadata, lang_name, mode):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        context = transcript if transcript else metadata['desc']
        prompt = f"Translate and adapt this for a natural spoken script in {lang_name}. Output ONLY the speech: {context[:3000]}"
        script = model.generate_content(prompt).text
        tts = gTTS(text=script, lang='en', slow=False) # Simplified for demo
        tts.save("dub_audio.mp3")
        return "dub_audio.mp3"
    except: return None

# --- 7. THE EXECUTIVE WORKFLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.daily_kural = get_random_kural()
    # Check if identity is already saved
    saved_user = load_identity()
    if saved_user:
        st.session_state.user = saved_user
        st.session_state.flow_stage = "animation"
    else:
        st.session_state.flow_stage = "onboarding"

# STAGE: ONBOARDING (ONE-TIME ONLY)
if st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="100px")
    st.title("Executive Onboarding")
    st.write("Authorize your device for Tackyon AI Hub access.")
    u_name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    col1, col2 = st.columns(2)
    with col1: u_gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with col2: u_age = st.number_input("Age", 18, 99, 19)
    if st.button("INITIALIZE SESSION", use_container_width=True):
        if u_name:
            user_data = {"name": u_name, "gender": u_gender, "age": u_age, "token": uuid.uuid4().hex[:6].upper()}
            save_identity(user_data)
            st.session_state.user = user_data
            st.session_state.flow_stage = "animation"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE: ANIMATION
elif st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="350px", animate=True)
    time.sleep(2.5)
    st.session_state.flow_stage = "hub"
    st.rerun()

# STAGE: INTELLIGENCE HUB
else:
    # Sidebar persistence
    with st.sidebar:
        render_t_logo(size="120px")
        st.title("Tackyon AI")
        st.write(f"Executive: **{st.session_state.user['name']}**")
        st.caption(f"Status: Authenticated | Token: {st.session_state.user['token']}")
        st.divider()
        if st.button("Reset Identity"):
            if os.path.exists(USER_CONFIG): os.remove(USER_CONFIG)
            st.session_state.clear()
            st.rerun()

    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    
    st.title("Executive Intelligence Hub")
    resource_url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
    
    tab1, tab2, tab3 = st.tabs(["Intelligence Report", "Neural Dubbing Studio", "Tackyon Assistant"])

    with tab1:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: lang_sum = st.selectbox("Report Language", ["Tamil", "English", "Hindi", "French", "German"])
        with c2: style_sum = st.selectbox("Style", ["Comprehensive", "Strategic", "Exam Guide"])
        
        if st.button("Execute Analysis", use_container_width=True):
            if resource_url:
                with st.spinner("Decoding..."):
                    m, t, mode = get_video_data(resource_url)
                    if mode == "error": st.error("Access Denied.")
                    else:
                        res = generate_ai_analysis(t, m, style_sum, lang_sum, mode)
                        st.markdown(f"### Report: {m['title']}")
                        st.markdown(f'<div class="analysis-result">{res}<div class="report-watermark">(T) TACKYON AI</div></div>', unsafe_allow_html=True)
                        # EXPORT OPTION
                        st.download_button("📥 Download Branded Report", f"TACKYON REPORT\n{res}", file_name="Tackyon_Report.txt")
                        # AD UNIT
                        render_tackyon_ad(is_test=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.subheader("Neural Dubbing Studio")
        dub_lang = st.selectbox("Dubbing Language", ["Tamil", "English", "Hindi"])
        if st.button("Generate Dubbed Audio", use_container_width=True):
            if resource_url:
                with st.spinner("Synthesizing..."):
                    m, t, mode = get_video_data(resource_url)
                    aud = run_neural_dub(t, m, dub_lang, mode)
                    if aud:
                        st.success("Dubbing Complete.")
                        st.audio(aud)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="assistant-header"><div class="assistant-icon">T</div><b>Tackyon AI Assistant</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="assistant-body">The Assistant is active and monitoring your workspace.</div>', unsafe_allow_html=True)

# FINAL AD FOOTER FOR TESTING
st.divider()
st.caption("Tackyon AI System v4.0 | Powered by Gemini 2.5 Flash")