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
import subprocess

# --- PYTHON 3.13 AUDIO ENGINE FIX ---
try:
    import audioop
except ImportError:
    import audioop_lts as audioop
# ---------------------------------------------------------

from pydub import AudioSegment

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
    }
    
    .history-card {
        background: #EBEDEF;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 12px;
        border-left: 5px solid #D4AC0D;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO & DATA ENGINES ---
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

def get_random_kural():
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except: pass
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 3. DUBBING STUDIO ENGINE (FFMPEG MERGE) ---
def get_video_and_audio(url):
    try:
        if not os.path.exists("temp"): os.makedirs("temp")
        file_id = int(time.time())
        
        # 1. Extraction of Video Metadata & Video File
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 
            'outtmpl': f'temp/video_{file_id}.mp4',
            'quiet': True,
            'no_warnings': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'Tackyon Dubbed Result')
            video_id = info['id']
            metadata = {
                "title": video_title,
                "channel": info.get('uploader', 'Independent Creator'),
                "likes": info.get('like_count', 'N/A'),
                "views": info.get('view_count', '0')
            }
        
        # 2. Transcription Retrieval
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([t['text'] for t in transcript_list])
            return metadata, transcript, f'temp/video_{file_id}.mp4', file_id
        except: 
            return metadata, None, f'temp/video_{file_id}.mp4', file_id
            
    except Exception as e:
        return None, None, None, None

def create_dubbed_video(video_path, transcript, lang_code, file_id, voice_type):
    try:
        # 1. AI Script Generation (Avoids 0-sec audio errors)
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Process in chunks if extremely long
        prompt = f"Convert this transcript into a natural, storytelling script in the language with code '{lang_code}'. The goal is a professional dubbing script: {transcript[:4500]}"
        dub_script = model.generate_content(prompt).text
        
        # 2. Neural Speech Synthesis
        tts = gTTS(text=dub_script, lang=lang_code, slow=False)
        audio_path = f"temp/audio_{file_id}.mp3"
        tts.save(audio_path)
        
        # 3. Executive FFmpeg Merge (Mute Original + Overlay AI Voice)
        output_path = f"temp/Tackyon_Dubbed_{file_id}.mp4"
        # -an mutes original audio; -map 0:v:0 takes original video; -map 1:a:0 takes new audio
        cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest {output_path} -y"
        subprocess.run(cmd, shell=True)
        
        return output_path
    except Exception as e:
        st.error(f"Media Merge Error: {str(e)}")
        return None

# --- 4. THE EXECUTIVE WORKFLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.update({
        "flow_stage": "animation", 
        "history": [], 
        "daily_kural": get_random_kural(),
        "user": None
    })

# STAGE 1: BRAND ANIMATION
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="380px", animate=True)
    pb = st.progress(0)
    for p in range(100):
        time.sleep(0.01)
        pb.progress(p + 1)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: ONBOARDING PORTAL
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
            st.session_state.flow_stage = "hub"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: MAIN HUB
else:
    # Sidebar Setup
    with st.sidebar:
        render_t_logo(size="130px") 
        st.markdown(f"### Executive: {st.session_state.user['name']}")
        st.divider()
        st.markdown("### 🕒 Intelligence History")
        if not st.session_state.history: st.write("No session records found.")
        for item in reversed(st.session_state.history):
            st.markdown(f'<div class="history-card"><b>{item["title"][:30]}...</b></div>', unsafe_allow_html=True)

    st.title("Executive Intelligence Hub")
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)

    # Intelligence & Dubbing Dashboard
    with st.expander("📥 Primary Resource Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link Here")
        
        col1, col2, col3 = st.columns(3)
        with col1: analysis_lang = st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi", "Malayalam"])
        with col2: style = st.selectbox("Output Style", ["Comprehensive Long Summary", "Strategic Points", "Exam Prep Guide", "Actionable Deep Dive"])
        with col3: dub_lang = st.selectbox("🎙️ Universal Dubbing", ["No Dubbing", "Tamil", "English", "Hindi"])

    if st.button("Execute Deep Analysis & Video Dubbing", use_container_width=True):
        if url:
            with st.spinner("Initializing Neural Production Studio... This involves downloading and processing video files."):
                m, transcript, video_path, f_id = get_video_and_audio(url)
                
                if transcript:
                    # 1. GENERATE LONG-FORM ANALYSIS
                    st.subheader(f"📑 Intelligence Report: {m['title']}")
                    st.markdown(f"**Channel:** {m['channel']} | **Engagement:** {m['likes']} Likes | **Views:** {m['views']}")
                    
                    api_key = st.secrets["GEMINI_API_KEY"]
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    analysis_prompt = f"Provide an extremely long, exhaustive, and highly detailed {style} in the {analysis_lang} language for the following transcript: {transcript[:6000]}"
                    analysis_output = model.generate_content(analysis_prompt).text
                    
                    if not any(h['title'] == m['title'] for h in st.session_state.history):
                        st.session_state.history.append({"title": m['title']})
                    
                    st.markdown(f'<div class="analysis-result">{analysis_output}</div>', unsafe_allow_html=True)
                    
                    # 2. GENERATE DUBBED VIDEO IF SELECTED
                    if dub_lang != "No Dubbing":
                        with st.spinner(f"Synthesizing Neural Voice ({dub_lang})... Please wait while we merge the media."):
                            l_map = {"Tamil": "ta", "English": "en", "Hindi": "hi"}
                            dubbed_video_path = create_dubbed_video(video_path, transcript, l_map[dub_lang], f_id, "Executive")
                            
                            if dubbed_video_path:
                                st.divider()
                                st.subheader(f"📽️ Dubbed Executive Playback ({dub_lang})")
                                st.video(dubbed_video_path)
                                st.success("Neural Dubbing Engine Complete. Original audio muted; AI voice overlaid.")
                                
                                # Download Capability
                                with open(dubbed_video_path, "rb") as file:
                                    st.download_button(
                                        label="📥 Download Dubbed Executive Video", 
                                        data=file, 
                                        file_name=f"Tackyon_Dubbed_{f_id}.mp4", 
                                        mime="video/mp4"
                                    )
                            else: st.error("Neural Dubbing Engine failed during merge stage.")
                else:
                    st.error("Access Failure: No transcript found or resource is restricted.")
        else:
            st.warning("Action Required: Please provide a valid Resource URL.")