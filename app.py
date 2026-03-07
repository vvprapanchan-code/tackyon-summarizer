# ==============================================================================
# TACKYON AI: NEURAL INTERPRETER (AUDIO-ONLY EDITION)
# CORE MODEL: GEMINI 3 FLASH
# STRATEGY: HIGHSPEED TRANSCRIPTION & NEURAL VOICE SYNTHESIS
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
from datetime import datetime

# --- STAGE 0: PYTHON 3.13 AUDIO ENGINE PATCH ---
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
        import sys
        sys.modules['audioop'] = audioop 
    except ImportError:
        st.error("Protocol Alert: 'audioop-lts' is required for voice synthesis.")

# --- STAGE 1: EXECUTIVE INTERFACE & BRANDING ---
st.set_page_config(page_title="Tackyon Interpreter", page_icon="🎙️", layout="wide")

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

    .interpreter-card {
        background: #FFFFFF; padding: 40px; border-radius: 25px;
        border-left: 15px solid #1B2631; position: relative;
        box-shadow: 0 15px 45px rgba(0,0,0,0.06); margin-top: 30px;
    }
    
    .tackyon-seal {
        position: absolute; bottom: 15px; right: 25px; font-size: 0.8em;
        color: rgba(27, 38, 49, 0.3); font-weight: 900; letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_directories():
    """Ensures temp storage exists to prevent FileNotFoundError."""
    for folder in ['temp', 'voice_exports']:
        if not os.path.exists(folder):
            os.makedirs(folder)

def load_identity():
    """Retrieves official Tackyon band image."""
    for f in ["logo.jpg", "logo.png", "t_symbol.jpg", "logo.jpeg"]:
        if os.path.exists(f):
            with open(f, "rb") as i: return base64.b64encode(i.read()).decode()
    return None

IDENTITY_B64 = load_identity()
initialize_directories()

# --- STAGE 2: STEALTH INTELLIGENCE EXTRACTION ---

def extract_intelligence(url):
    """Bypasses YouTube blocks to get speech data for translation."""
    try:
        # Use stealth headers to avoid 403 Forbidden
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36'
        }
        with YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            video_id = meta['id']
            video_title = meta['title']
        
        # Priority 1: Direct Transcript
        try:
            raw_t = YouTubeTranscriptApi.get_transcript(video_id)
            content = " ".join([e['text'] for e in raw_t])
            mode = "Deep Neural Sync"
        except:
            # Priority 2: Description Fallback
            content = f"Title: {video_title}. Context: {meta.get('description', 'N/A')}"
            mode = "Contextual Inference"
            
        return {"title": video_title, "content": content, "mode": mode, "id": video_id}
    except Exception as e:
        st.error(f"Access Error: {str(e)}")
        return None

# --- STAGE 3: NEURAL VOICE PRODUCTION ---

def generate_dub_audio(intel_data, lang, persona):
    """Converts video data into a high-quality neural voice."""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Using Gemini 3 Flash for the 2026 Sovereign Engine
        brain = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create a professional script for the voice
        script_prompt = f"Convert this text into a flowing, professional {persona} dubbing script in {lang}. Return ONLY the script: {intel_data['content'][:5000]}"
        script = brain.generate_content(script_prompt).text
        
        l_map = {"Tamil": "ta", "English": "en", "Hindi": "hi", "French": "fr"}
        tts = gTTS(text=script, lang=l_map.get(lang, "ta"), slow=False)
        
        audio_filename = f"temp/dub_{intel_data['id']}.mp3"
        tts.save(audio_filename)
        return audio_filename
    except Exception as e:
        st.error(f"Voice Synthesis Error: {str(e)}")
        return None

# --- STAGE 4: EXECUTIVE FLOW ---

if "interpreter_state" not in st.session_state:
    st.session_state.interpreter_state = {"stage": "identification", "user": None}

if st.session_state.interpreter_state["stage"] == "identification":
    st.markdown('<div class="id-portal" style="background:white; padding:50px; border-radius:30px; text-align:center; box-shadow:0 20px 60px rgba(0,0,0,0.1); border-top:10px solid #1B2631; max-width:800px; margin: 50px auto;">', unsafe_allow_html=True)
    if IDENTITY_B64:
        st.markdown(f'<img src="data:image/jpeg;base64,{IDENTITY_B64}" width="100" style="border-radius:20px; margin-bottom:20px;">', unsafe_allow_html=True)
    st.title("Tackyon Interpreter Access")
    name = st.text_input("Executive Name")
    if st.button("AUTHORIZE SYSTEM", use_container_width=True):
        if name:
            st.session_state.interpreter_state["user"] = name
            st.session_state.interpreter_state["stage"] = "hub"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="wisdom-frame"><div class="wisdom-top">Tackyon Neural Interpreter</div></div>', unsafe_allow_html=True)
    st.title(f"Active Session: {st.session_state.interpreter_state['user']}")
    
    
    
    url = st.text_input("Enter YouTube Link to Interpret", placeholder="Paste Video Link Here")
    
    c1, c2 = st.columns(2)
    with c1: target_lang = st.selectbox("Target Dubbing Language", ["Tamil", "English", "Hindi", "French"])
    with c2: persona = st.selectbox("🎙️ Voice Persona", ["Male Executive", "Female Executive"])
    
    if st.button("START NEURAL INTERPRETATION", use_container_width=True):
        if url:
            with st.status("Extracting Intelligence...") as status:
                intel = extract_intelligence(url)
                if intel:
                    status.update(label=f"Synthesizing {target_lang} Voice ({intel['mode']})...", state="running")
                    audio_path = generate_dub_audio(intel, target_lang, persona)
                    
                    if audio_path:
                        status.update(label="Interpretation Ready.", state="complete")
                        st.markdown(f'''<div class="interpreter-card">
                            <h3>🎙️ {target_lang} Neural Dub ({persona})</h3>
                            <p><b>Video:</b> {intel['title']}</p>
                            <div class="tackyon-seal">Tackyon Interpreter © 2026</div>
                        </div>''', unsafe_allow_html=True)
                        
                        st.audio(audio_path)
                        st.success("You can now play this audio while watching the original video.")
                        
                        with open(audio_path, "rb") as f:
                            st.download_button("📥 DOWNLOAD DUBBED AUDIO (MP3)", f, f"Dub_{intel['id']}.mp3")
                else:
                    st.error("Access Restricted: YouTube is blocking the server IP.")