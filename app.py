import streamlit as st
import time
import base64
import os
import random
import json
import google.generativeai as genai
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from gtts import gTTS

# --- PYTHON 3.13 AUDIO ENGINE PATCH ---
try:
    import audioop
except ImportError:
    import audioop_lts as audioop
# ----------------------------------------------------------------

from pydub import AudioSegment

# --- 1. THEME & EXECUTIVE INTERFACE ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    header, [data-testid="stHeader"], .stAppHeader { display: none !important; visibility: hidden !important; }
    .block-container { padding-top: 0px !important; margin-top: -30px !important; }
    .kural-box { background-color: #FDFEFE; border-bottom: 3px solid #D4AC0D; padding: 20px; text-align: center; width: 100%; margin-bottom: 35px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .kural-line1 { font-size: 1.5em; font-weight: bold; color: #1B2631; margin-bottom: 8px; }
    .kural-line2 { font-size: 1.3em; color: #5D6D7E; font-style: italic; }
    .executive-card { background: white; padding: 45px; border-radius: 25px; box-shadow: 0 15px 50px rgba(0,0,0,0.12); border-top: 8px solid #1B2631; text-align: center; max-width: 900px; margin: auto; }
    @keyframes t-pulse { 0% { transform: scale(1); filter: brightness(100%); } 50% { transform: scale(1.06); filter: brightness(130%); } 100% { transform: scale(1); filter: brightness(100%); } }
    .pulse-layer { animation: t-pulse 2.5s infinite ease-in-out; }
    .analysis-result { background: #F8F9F9; padding: 30px; border-radius: 18px; border-left: 10px solid #1B2631; text-align: left; margin-top: 25px; color: #1C2833; line-height: 1.8; }
    .history-card { background: #EBEDEF; padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #D4AC0D; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO & DATA LOADER ---
def load_logo_proven():
    try:
        for f in ["logo.jpg", "logo.jpg.jpeg", "logo.jpeg"]:
            if os.path.exists(f):
                with open(f, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return None
    return None

logo_data_b64 = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    if logo_data_b64:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(f'<div class="{anim_class}" style="text-align: center; margin-bottom: 25px;"><img src="data:image/jpeg;base64,{logo_data_b64}" style="width:{size}; border-radius: 20px;"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: center; font-size: 35px; font-weight: bold; color: #1B2631;">TACKYON AI</div>', unsafe_allow_html=True)

def get_random_kural():
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except: pass
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 3. AI & DUBBING CORE ---
def get_video_data(url):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            metadata = {"title": info.get('title', 'Resource'), "url": url, "id": info['id']}
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(info['id'])
                transcript = " ".join([t['text'] for t in transcript_list])
                return metadata, transcript, "full"
            except: return metadata, None, "meta_only"
    except: return None, None, "error"

def generate_ai_content(prompt_text):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # Using 1.5 Flash for the "Brain"
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e: return f"Error: {str(e)}"

def run_auto_dubbing(transcript, lang_code):
    try:
        if not os.path.exists("temp"): os.makedirs("temp")
        trans_p = f"Translate this text perfectly to language code '{lang_code}': {transcript}"
        translated = generate_ai_content(trans_p)
        tts = gTTS(text=translated, lang=lang_code, slow=False)
        path = f"temp/dub_{int(time.time())}.mp3"
        tts.save(path)
        return path
    except: return None

# --- 4. NAVIGATION FLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.update({"flow_stage": "animation", "history": [], "daily_kural": get_random_kural()})

if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="380px", animate=True)
    pb = st.progress(0)
    for p in range(100):
        time.sleep(0.02)
        pb.progress(p + 1)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

elif st.session_state.flow_stage == "onboarding":
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="100px")
    st.title("Executive Identification")
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    age = st.number_input("Age", 18, 99, 19)
    if st.button("Initialize System"):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "hub"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- SIDEBAR CONTROL CENTER ---
    with st.sidebar:
        render_t_logo(size="120px")
        st.markdown(f"### Executive: {st.session_state.user['name']}")
        st.divider()
        # Page Selection
        mode = st.selectbox("🎯 SELECT MODE", ["Intelligence Hub", "Universal Dubbing Studio"])
        st.divider()
        st.markdown("### 🕒 Recent History")
        for item in reversed(st.session_state.history):
            st.sidebar.markdown(f'<div class="history-card"><b>{item["title"][:25]}...</b></div>', unsafe_allow_html=True)

    # --- MAIN STAGE ---
    if mode == "Intelligence Hub":
        st.title("Executive Intelligence Hub")
        url = st.text_input("YouTube URL")
        lang = st.selectbox("Analysis Language", ["Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada"])
        style = st.selectbox("Summary Style", ["Comprehensive Long Summary", "Strategic Points", "Exam Prep"])
        if st.button("Deep Analysis"):
            with st.spinner("Analyzing..."):
                m, t, res = get_video_data(url)
                if res != "error":
                    output = generate_ai_content(f"Provide a deep, exhaustive analysis in {lang} with {style} style for this text: {t}")
                    if not any(h['title'] == m['title'] for h in st.session_state.history):
                        st.session_state.history.append({"title": m['title']})
                    st.markdown(f'<div class="analysis-result">{output}</div>', unsafe_allow_html=True)

    elif mode == "Universal Dubbing Studio":
        st.title("Universal Dubbing Studio")
        st.info("Translate Video Voice Instantly")
        
        dub_url = st.text_input("Video URL to Dub")
        target_l = st.selectbox("Translate Voice To", ["Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada"])
        l_map = {"Tamil": "ta", "English": "en", "Hindi": "hi", "Malayalam": "ml", "Telugu": "te", "Kannada": "kn"}
        if st.button("Start Auto-Dubbing"):
            with st.spinner("Dubbing Voice..."):
                m, t, res = get_video_data(dub_url)
                if t:
                    audio = run_auto_dubbing(t, l_map[target_l])
                    if audio:
                        st.success("Dubbing Complete!")
                        st.audio(audio)
                        st.video(dub_url)
                else: st.error("No speech found to dub.")