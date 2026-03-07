# ==============================================================================
# TACKYON AI: ULTIMATE SOVEREIGN SUITE (BUILD 2026.03.07)
# FIXES: AUDIO ENGINE, YOUTUBE ACCESS, & DIRECTORY ERRORS
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

# --- STAGE 0: THE AUDIO BRIDGE (FIXES PYAUDIOOP ERROR) ---
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
        # This line is the "Bridge" that pydub needs
        import sys
        sys.modules['audioop'] = audioop 
    except ImportError:
        st.error("Protocol Error: audioop-lts not found in environment.")

from pydub import AudioSegment

# --- STAGE 1: AUTO-INITIALIZATION (FIXES FILENOTFOUND) ---
def initialize_system():
    # Automatically creates these folders so the app never crashes
    for folder in ['temp', 'exports', 'logs', 'assets']:
        if not os.path.exists(folder):
            os.makedirs(folder)

initialize_system()

# --- STAGE 2: EXECUTIVE STYLING ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    header, [data-testid="stHeader"], .stAppHeader { display: none !important; }
    .block-container { padding-top: 0px !important; margin-top: -20px !important; }
    .wisdom-frame { background: white; border-bottom: 5px solid #D4AC0D; padding: 40px; text-align: center; border-radius: 0 0 40px 40px; }
    .wisdom-top { font-size: 1.8em; font-weight: 900; color: #1B2631; }
    .report-frame { background: #FFFFFF; padding: 50px; border-radius: 30px; border-left: 15px solid #1B2631; box-shadow: 0 15px 45px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- STAGE 3: STEALTH DOWNLOAD ENGINE (FIXES 403 ERROR) ---
def decrypt_resource(url):
    try:
        fid = int(time.time())
        # Stealth Headers: Tells YouTube we are a human on Chrome
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 
            'outtmpl': f'temp/raw_{fid}.mp4',
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/'
        }
        with YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=True)
            vid = meta['id']
            
        try:
            raw_t = YouTubeTranscriptApi.get_transcript(vid)
            content = " ".join([e['text'] for e in raw_t])
        except:
            content = f"Title: {meta.get('title')}. Description: {meta.get('description', 'N/A')}"
            
        return {"title": meta['title'], "path": f'temp/raw_{fid}.mp4', "data": content, "fid": fid}
    except Exception as e:
        st.error(f"Access Denied (403): YouTube is blocking Streamlit. {str(e)}")
        return None

# --- STAGE 4: PRODUCTION STUDIO ---
def execute_dub(res, lang, persona):
    try:
        fid = res['fid']
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-3-flash')
        
        # Script preparation
        script = model.generate_content(f"Create a natural dubbing script in {lang}: {res['data'][:4000]}").text
        
        l_map = {"Tamil": "ta", "English": "en", "Hindi": "hi"}
        voice = gTTS(text=script, lang=l_map.get(lang, "en"), slow=False)
        v_path = f"temp/v_{fid}.mp3"
        voice.save(v_path)
        
        out = f"exports/Tackyon_{fid}.mp4"
        # Mute original and merge AI voice
        cmd = ['ffmpeg', '-i', res['path'], '-i', v_path, '-c:v', 'copy', '-c:a', 'aac', 
               '-map', '0:v:0', '-map', '1:a:0', '-shortest', out, '-y']
        subprocess.run(cmd, capture_output=True)
        return out
    except: return None

# --- STAGE 5: WORKFLOW ---
if "kernel" not in st.session_state:
    st.session_state.kernel = {"stage": "boot", "user": None}

if st.session_state.kernel["stage"] == "boot":
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    st.title("TACKYON AI")
    p = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        p.progress(i + 1)
    st.session_state.kernel["stage"] = "hub"
    st.rerun()

else:
    st.markdown('<div class="wisdom-frame"><div class="wisdom-top">Sovereign Intelligence Suite</div></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔍 Intelligence Summary", "🎙️ Universal Dubbing Studio"])
    
    with tab1:
        st.subheader("Deep Intelligence Extraction")
        url_s = st.text_input("Enter Video URL")
        l_s = st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi"])
        if st.button("Execute Deep Analysis"):
            res = decrypt_resource(url_s)
            if res:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-3-flash')
                analysis = model.generate_content(f"Exhaustive analysis in {l_s} for: {res['data'][:6000]}").text
                st.markdown(f'<div class="report-frame"><h2>{res["title"]}</h2><p>{analysis}</p></div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("Neural Production Studio")
        url_d = st.text_input("Enter URL to Dub")
        l_d = st.selectbox("Target Dub Language", ["Tamil", "English", "Hindi"])
        if st.button("Start Neural Overdub"):
            res = decrypt_resource(url_d)
            if res:
                with st.spinner("Processing..."):
                    dub_file = execute_dub(res, l_d, "Executive")
                    if dub_file:
                        st.video(dub_file)
                        with open(dub_file, "rb") as f:
                            st.download_button("📥 DOWNLOAD", f, f"Dubbed_{res['fid']}.mp4")