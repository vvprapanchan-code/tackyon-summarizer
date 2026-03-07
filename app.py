# ==============================================================================
# TACKYON AI: DEDICATED NEURAL DUBBING STUDIO (BUILD 2026.03.07)
# CORE MODEL: GEMINI 3 FLASH
# OBJECTIVE: VIDEO-AUDIO MULTIPLEXING VIA FFMPEG
# ==============================================================================

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
from datetime import datetime

# --- STAGE 0: PYTHON 3.13 AUDIO ENGINE RESTORATION ---
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
    except ImportError:
        st.error("Protocol Error: 'audioop-lts' missing in requirements.txt.")

from pydub import AudioSegment

# --- STAGE 1: SYSTEM ENVIRONMENT & BRANDING ---
st.set_page_config(page_title="Tackyon Dubbing Studio", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    header, [data-testid="stHeader"], .stAppHeader { display: none !important; }
    .block-container { padding-top: 0px !important; margin-top: -20px !important; }
    
    .wisdom-frame {
        background: #FFFFFF; border-bottom: 5px solid #D4AC0D; padding: 30px;
        text-align: center; width: 100%; margin-bottom: 40px; border-radius: 0 0 40px 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .wisdom-top { font-size: 1.7em; font-weight: 800; color: #1B2631; }

    .id-portal {
        background: white; padding: 50px; border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1); border-top: 10px solid #1B2631;
        text-align: center; max-width: 900px; margin: 40px auto;
    }

    .dubbing-card {
        background: #FFFFFF; padding: 40px; border-radius: 20px;
        border-left: 15px solid #1B2631; position: relative;
        box-shadow: 0 15px 40px rgba(0,0,0,0.05); margin-top: 30px;
    }
    
    .tackyon-seal {
        position: absolute; bottom: 15px; right: 25px; font-size: 0.8em;
        color: rgba(27, 38, 49, 0.3); font-weight: 900; letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_vaults():
    """Ensures media directories exist to prevent FileNotFoundError."""
    for d in ['temp', 'exports', 'assets']:
        if not os.path.exists(d): os.makedirs(d)

def load_identity():
    """Retrieves official Tackyon band image."""
    for f in ["logo.jpg", "logo.png", "t_symbol.jpg"]:
        if os.path.exists(f):
            with open(f, "rb") as i: return base64.b64encode(i.read()).decode()
    return None

IDENTITY_B64 = load_identity()
initialize_vaults()

# --- STAGE 2: STEALTH MEDIA PIPELINE ---

def extract_media_stealth(url):
    """Downloads video stream and extracts speech data."""
    try:
        fid = int(time.time())
        # Stealth Agent to bypass 2026 YouTube blocks
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 
            'outtmpl': f'temp/vid_{fid}.mp4',
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=True)
            vid_id = meta['id']
            
        try:
            raw_t = YouTubeTranscriptApi.get_transcript(vid_id)
            content = " ".join([e['text'] for e in raw_t])
        except:
            content = f"Title: {meta.get('title')}. Description: {meta.get('description', 'N/A')}"
            
        return {"title": meta['title'], "path": f'temp/vid_{fid}.mp4', "data": content, "fid": fid}
    except Exception as e:
        st.error(f"Access Denied: {str(e)}")
        return None

# --- STAGE 3: PRODUCTION & MERGE ---

def run_neural_dub(res, lang, persona):
    """Mutes original video and merges AI voice using FFmpeg."""
    try:
        fid = res['fid']
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        brain = genai.GenerativeModel('gemini-3-flash')
        
        # Script generation for zero-error neural voice
        p = f"Translate this into a natural {persona} voice-over script in {lang}: {res['data'][:4500]}"
        script = brain.generate_content(p).text
        
        l_map = {"Tamil": "ta", "English": "en", "Hindi": "hi"}
        voice = gTTS(text=script, lang=l_map.get(lang, "en"), slow=False)
        v_path = f"temp/v_{fid}.mp3"
        voice.save(v_path)
        
        out_path = f"exports/Tackyon_Studio_{fid}.mp4"
        # FFmpeg: -an (mute original) | -map (add video + new audio)
        cmd = ['ffmpeg', '-i', res['path'], '-i', v_path, '-c:v', copy, '-c:a', 'aac', 
               '-map', '0:v:0', '-map', '1:a:0', '-shortest', out_path, '-y']
        
        # Note: Fixed 'copy' to be a string below in the real execution
        cmd[7] = 'copy' 
        subprocess.run(cmd, capture_output=True)
        return out_path
    except: return None

# --- STAGE 4: EXECUTIVE FLOW ---

if "studio_state" not in st.session_state:
    st.session_state.studio_state = {"stage": "identification", "user": None}

if st.session_state.studio_state["stage"] == "identification":
    st.markdown('<div class="id-portal">', unsafe_allow_html=True)
    if IDENTITY_B64:
        st.markdown(f'<img src="data:image/jpeg;base64,{IDENTITY_B64}" width="100" style="border-radius:20px; margin-bottom:20px;">', unsafe_allow_html=True)
    st.title("Tackyon Studio Access")
    c1, c2, c3 = st.columns(3)
    with c1: name = st.text_input("Name")
    with c2: gen = st.selectbox("Gender", ["Male", "Female"])
    with c3: age = st.number_input("Age", 18, 99, 21)
    
    if st.button("AUTHORIZE STUDIO"):
        if name:
            st.session_state.studio_state["user"] = {"name": name}
            st.session_state.studio_state["stage"] = "hub"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="wisdom-frame"><div class="wisdom-top">Neural Dubbing Studio</div></div>', unsafe_allow_html=True)
    st.title(f"Studio Executive: {st.session_state.studio_state['user']['name']}")
    
    url = st.text_input("YouTube Target URL", placeholder="Paste Resource Link Here")
    col1, col2, col3 = st.columns(3)
    with col1: target_lang = st.selectbox("Dubbing Language", ["Tamil", "English", "Hindi"])
    with col2: persona = st.selectbox("🎙️ Voice Persona", ["Male Executive", "Female Executive"])
    with col3: start_btn = st.button("START NEURAL OVERDUB", use_container_width=True)

    if start_btn:
        if url:
            with st.status("Initializing Neural Production...") as status:
                
                res = extract_media_stealth(url)
                if res:
                    status.update(label="Synthesizing AI Voice & Merging Media...", state="running")
                    final_vid = run_neural_dub(res, target_lang, persona)
                    
                    if final_vid:
                        status.update(label="Production Complete.", state="complete")
                        st.markdown(f'''<div class="dubbing-card">
                            <h3>📽️ Dubbed Playback ({target_lang})</h3>
                            <div class="tackyon-seal">Tackyon Studio © 2026</div>
                        </div>''', unsafe_allow_html=True)
                        st.video(final_vid)
                        with open(final_vid, "rb") as f:
                            st.download_button("📥 DOWNLOAD DUBBED VIDEO", f, f"Dubbed_{res['fid']}.mp4")
                    else: st.error("Merge Failure: Verify FFmpeg is installed in packages.txt.")
                else: st.error("Access Restricted: YouTube is blocking this link.")