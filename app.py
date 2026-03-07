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

# --- PYTHON 3.13 AUDIO FIX ---
try:
    import audioop
except ImportError:
    import audioop_lts as audioop
# ----------------------------------------------

from pydub import AudioSegment

# --- 1. THEME & EXECUTIVE ARCHITECTURE (PROTECTED) ---
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

logo_data_b64 = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    if logo_data_b64:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(f'<div class="{anim_class}" style="text-align: center; margin-bottom: 25px;"><img src="data:image/jpeg;base64,{logo_data_b64}" style="width:{size}; border-radius: 20px;"></div>', unsafe_allow_html=True)
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

# --- 4. INTELLIGENCE & DUBBING ENGINES ---
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
                "thumbnail": info.get('thumbnail', ''),
                "url": url,
                "id": info['id'],
                "description": info.get('description', '')[:1200]
            }
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
    except Exception as e:
        return f"Error: {str(e)}"

def run_auto_dubbing(transcript, target_lang_code):
    try:
        if not os.path.exists("temp"): os.makedirs("temp")
        translate_prompt = f"Translate this text perfectly to the language with code '{target_lang_code}'. Only return the translated text: {transcript}"
        translated_text = generate_ai_content(translate_prompt)
        tts = gTTS(text=translated_text, lang=target_lang_code, slow=False)
        dub_path = f"temp/dubbed_{int(time.time())}.mp3"
        tts.save(dub_path)
        return dub_path
    except Exception as e:
        st.error(f"Dubbing Failed: {str(e)}")
        return None

# --- 5. THE EXECUTIVE WORKFLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = get_random_kural()
    st.session_state.history = []

if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="380px", animate=True)
    progress_bar = st.progress(0)
    for p in range(100):
        time.sleep(0.02)
        progress_bar.progress(p + 1)
    st.session_state.flow_stage = "onboarding"
    if st.button("Enter Portal", use_container_width=True): st.rerun()
    time.sleep(0.5)
    st.rerun()

elif st.session_state.flow_stage == "onboarding":
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="100px") 
    st.title("Executive Identification")
    c1, c2, c3 = st.columns(3)
    with c1: u_name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with c2: u_gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with c3: u_age = st.number_input("Age", 18, 99, 19)
    if st.button("Initialize System", use_container_width=True):
        if u_name:
            st.session_state.user = {"name": u_name, "gender": u_gender, "age": u_age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.flow_stage == "gateway":
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="90px")
    st.info(f"Identity Verified: Executive {st.session_state.user['name']}.")
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- NAVIGATION & HISTORY SIDEBAR ---
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    render_t_logo(size="130px") 
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    app_mode = st.sidebar.selectbox("Choose Mode", ["Intelligence Hub", "Universal Dubbing Studio"])
    
    st.sidebar.divider()
    st.sidebar.markdown("### 🕒 Intelligence History")
    if not st.session_state.history:
        st.sidebar.write("No history recorded.")
    else:
        for item in reversed(st.session_state.history):
            st.sidebar.markdown(f'<div class="history-card"><b>{item["title"][:40]}...</b><br><a href="{item["url"]}" target="_blank">View Video</a></div>', unsafe_allow_html=True)

    if app_mode == "Intelligence Hub":
        st.title("Executive Intelligence Hub")
        with st.expander("📥 Primary Resource Acquisition", expanded=True):
            url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
            c1, c2 = st.columns(2)
            with c1: lang = st.selectbox("Language", ["Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada", "French", "German", "Spanish", "Japanese"])
            with c2: style = st.selectbox("Style", ["Comprehensive Long Summary", "Detailed Strategic Points", "Exam Preparation Guide", "Actionable Deep Dive"])
            
            if st.button("Execute Deep Analysis", use_container_width=True):
                if url:
                    with st.spinner("Decrypting Intelligence..."):
                        m, t, mode = get_video_data(url)
                        if mode == "error": st.error("Access denied to the provided URL.")
                        else:
                            st.markdown(f"### 📑 Analysis: {m['title']}")
                            instr = "Provide an extremely long, exhaustive analysis. Do not be brief."
                            prompt = f"Act as an Executive Analyst. {instr} Analyze: {t}. Style: {style} in {lang}."
                            res = generate_ai_content(prompt)
                            if not any(h['url'] == url for h in st.session_state.history):
                                st.session_state.history.append({"title": m['title'], "url": url})
                            st.markdown(f'<div class="analysis-result"><b>{style} ({lang}):</b><br><br>{res}</div>', unsafe_allow_html=True)

    elif app_mode == "Universal Dubbing Studio":
        st.title("Universal Dubbing Studio")
        st.write("Translate any video audio into a new voice instantly.")
        
        # INDENTATION FIXED HERE
        dub_url = st.text_input("Video URL to Dub", placeholder="Paste YouTube Link")
        lang_map = {"Tamil": "ta", "English": "en", "Hindi": "hi", "Malayalam": "ml", "Telugu": "te", "Kannada": "kn", "French": "fr", "German": "de"}
        target_lang = st.selectbox("Select Dubbing Language", list(lang_map.keys()))
        
        if st.button("Start Auto-Dubbing Engine", use_container_width=True):
            if dub_url:
                with st.spinner("Processing Voice Synthesis... This may take a minute."):
                    m, t, mode = get_video_data(dub_url)
                    if t:
                        audio_file = run_auto_dubbing(t, lang_map[target_lang])
                        if audio_file:
                            st.success(f"Dubbing Complete! Listen to {m['title']} in {target_lang} below.")
                            st.audio(audio_file)
                            st.video(dub_url)
                    else: st.error("No speech found in video to dub.")
            else: st.warning("Please provide a video URL.")