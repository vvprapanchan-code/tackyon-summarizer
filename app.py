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
# This section ensures the polished, high-end look of Tackyon AI.
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
        text-align: right; font-size: 10px; color: #BDC3C7;
        font-weight: 900; letter-spacing: 2px; margin-top: 15px;
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
# This ensures users only enter their details once.
USER_FILE = "tackyon_identity.json"

def save_user_info(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f)

def load_user_info():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return None

# --- 3. LOGO ENGINE (STABLE SCANNER) ---
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

# --- 4. DATABASE ENGINE (KURAL LOADER) ---
def get_random_kural():
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except: pass
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 5. SAFE AD ENGINE (TEST UNIT) ---
def render_tackyon_ad(is_test=True):
    """Renders official Google Test Ads to prevent account blocking."""
    st.markdown('<div class="ad-slot-frame">', unsafe_allow_html=True)
    st.caption("STRATEGIC PARTNER ADVERTISEMENT (SAFE TEST MODE)")
    
    # Official Google AdMob Test Publisher ID
    pub_id = "ca-pub-3940256099942544" if is_test else "YOUR_REAL_ID"
    
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

# --- 6. INTELLIGENCE ENGINE ---
def get_video_data(url):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            metadata = {
                "title": info.get('title', 'Unknown Resource'),
                "channel": info.get('uploader', 'Independent Creator'),
                "description": info.get('description', '')[:2000],
                "id": info.get('id', '')
            }
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(info['id'])
                transcript = " ".join([t['text'] for t in transcript_list])
                return metadata, transcript, "full"
            except: 
                return metadata, None, "meta_only"
    except: return None, None, "error"

def generate_ai_analysis(transcript, metadata, style, lang, mode):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        if mode == "meta_only":
            prompt = f"Act as a Brand Expert. Based on Title: {metadata['title']} and Description: {metadata['description']}, provide a detailed {style} in {lang}."
        else:
            prompt = f"Act as an Executive Analyst. Analyze: {transcript}. Provide a deep {style} in {lang}."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Intelligence Hub Offline. Error: {str(e)}"

def execute_neural_dubbing(transcript, metadata, lang_name, mode):
    try:
        target_code = "en" # Example default
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        context = transcript if transcript else metadata['description']
        dub_prompt = f"Translate and adapt this for a natural spoken script in {lang_name}. Output ONLY the speech: {context[:3000]}"
        script = model.generate_content(dub_prompt).text
        tts = gTTS(text=script, lang='en', slow=False)
        tts.save("dubbed_audio.mp3")
        return "dubbed_audio.mp3"
    except: return None

# --- 7. THE EXECUTIVE WORKFLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.daily_kural = get_random_kural()
    st.session_state.chat_history = []
    
    # Check for existing login
    saved_identity = load_user_info()
    if saved_identity:
        st.session_state.user = saved_identity
        st.session_state.flow_stage = "animation"
    else:
        st.session_state.flow_stage = "onboarding"

# ONE-TIME LOGIN STAGE
if st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="100px") 
    st.title("Executive Onboarding")
    st.write("Register your identity once for persistent device access.")
    u_name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    col1, col2 = st.columns(2)
    with col1: u_gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with col2: u_age = st.number_input("Age", 18, 99, 19)
    if st.button("AUTHORIZE SESSION", use_container_width=True):
        if u_name:
            user_data = {"name": u_name, "gender": u_gender, "age": u_age, "token": uuid.uuid4().hex[:6].upper()}
            save_user_info(user_data)
            st.session_state.user = user_data
            st.session_state.flow_stage = "animation"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# PULSE ANIMATION STAGE
elif st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="380px", animate=True)
    time.sleep(2.5)
    st.session_state.flow_stage = "hub"
    st.rerun()

# MAIN HUB STAGE
else:
    with st.sidebar:
        render_t_logo(size="120px") 
        st.title("Tackyon AI")
        st.markdown(f"**Executive:** {st.session_state.user['name']}")
        st.caption(f"Hardware Token: {st.session_state.user['token']}")
        st.divider()
        if st.button("Reset Identity"):
            if os.path.exists(USER_FILE): os.remove(USER_FILE)
            st.session_state.clear()
            st.rerun()

    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    
    st.title("Executive Intelligence Hub")
    url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
    
    tab_sum, tab_dub, tab_ast = st.tabs(["Intelligence Summary", "Neural Dubbing Studio", "Assistant"])

    with tab_sum:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        lang_sum = st.selectbox("Language", ["Tamil", "English", "Hindi", "French", "German"])
        if st.button("Execute Deep Analysis", use_container_width=True):
            if url:
                with st.spinner("Decoding via Gemini 2.5 Flash..."):
                    m, t, mode = get_video_data(url)
                    if mode == "error": st.error("Access Denied.")
                    else:
                        res = generate_ai_analysis(t, m, "Summary", lang_sum, mode)
                        st.markdown(f'<div class="analysis-result">{res}<div class="report-watermark">(T) TACKYON AI</div></div>', unsafe_allow_html=True)
                        # TEST AD SHOWING AFTER REPORT
                        render_tackyon_ad(is_test=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_dub:
        st.info("Dubbing Engine Ready. Enter URL above to generate audio overdubs.")

    with tab_ast:
        st.markdown('<div class="assistant-header"><div class="assistant-icon">T</div><b>Tackyon AI Assistant</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="assistant-body">Ask anything about your processed resources.</div>', unsafe_allow_html=True)

# FINAL SYSTEM FOOTER
st.divider()
st.caption("Tackyon AI Studio v4.2 | Authored by Prapanchan")