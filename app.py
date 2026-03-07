# ==============================================================================
# TACKYON AI: ULTIMATE EXECUTIVE PRODUCER SUITE (BUILD 2026.03)
# CORE MODEL: GEMINI 3 FLASH
# FEATURES: NEURAL DUBBING, FFMPEG MERGE, THIRUKURAL DB, BRAND WATERMARK
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
import shutil

# --- STAGE 0: PYTHON 3.13 LEGACY AUDIO PATCH ---
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
    except ImportError:
        st.error("CRITICAL: audioop-lts missing from requirements.txt. Audio features may fail.")

from pydub import AudioSegment

# --- STAGE 1: GLOBAL CONFIGURATION & EXECUTIVE BRANDING ---
st.set_page_config(
    page_title="Tackyon AI | Sovereign Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED EXECUTIVE STYLING (CSS) ---
st.markdown("""
    <style>
    /* Hide Default Elements */
    header, [data-testid="stHeader"], .stAppHeader { display: none !important; visibility: hidden !important; }
    .block-container { padding-top: 0px !important; margin-top: -20px !important; }
    footer { visibility: hidden; }

    /* Executive Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8F9F9; }

    /* The Kural Wisdom Box (4-3 Format) */
    .kural-container {
        background: linear-gradient(135deg, #FFFFFF 0%, #F4F6F7 100%);
        border-bottom: 4px solid #D4AC0D;
        padding: 40px;
        text-align: center;
        width: 100%;
        margin-bottom: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border-radius: 0 0 40px 40px;
    }
    .kural-top { font-size: 1.8em; font-weight: 800; color: #1B2631; letter-spacing: -0.5px; margin-bottom: 12px; }
    .kural-bottom { font-size: 1.4em; color: #5D6D7E; font-style: italic; font-weight: 400; }

    /* Executive Identification Cards */
    .id-card {
        background: white; 
        padding: 60px; 
        border-radius: 35px;
        box-shadow: 0 25px 70px rgba(0,0,0,0.1); 
        border-top: 12px solid #1B2631;
        text-align: center; 
        max-width: 1100px; 
        margin: 50px auto;
    }

    /* Metallic T-Pulse Animation */
    @keyframes metallic-pulse {
        0% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(212, 172, 13, 0)); }
        50% { transform: scale(1.05); filter: drop-shadow(0 0 25px rgba(212, 172, 13, 0.4)); }
        100% { transform: scale(1); filter: drop-shadow(0 0 0px rgba(212, 172, 13, 0)); }
    }
    .brand-pulse { animation: metallic-pulse 3s infinite ease-in-out; }

    /* Intelligence Report Containers */
    .report-frame {
        background: #FFFFFF; 
        padding: 50px; 
        border-radius: 25px;
        border-left: 15px solid #1B2631; 
        text-align: left;
        margin-top: 40px; 
        color: #1C2833; 
        line-height: 2.2;
        position: relative;
        box-shadow: 0 15px 45px rgba(0,0,0,0.05);
    }
    
    /* The Official T-Symbol Watermark */
    .tackyon-watermark {
        position: absolute;
        bottom: 20px;
        right: 30px;
        font-size: 0.85em;
        color: rgba(27, 38, 49, 0.3);
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* History Sidebar Modules */
    .sidebar-history-item {
        background: #F2F4F4;
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-right: 5px solid #D4AC0D;
        transition: all 0.4s ease;
        cursor: pointer;
    }
    .sidebar-history-item:hover { background: #E5E8E8; transform: translateX(5px); }

    /* System Status Badges */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: bold;
        text-transform: uppercase;
        background: #D5F5E3;
        color: #1D8348;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STAGE 2: SYSTEM KERNEL (UTILITIES) ---

def initialize_directories():
    """Ensures environment is ready for media processing."""
    dirs = ['temp', 'exports', 'database', 'logs']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def log_system_event(event):
    """Internal auditing of executive actions."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/system.log", "a") as f:
        f.write(f"[{timestamp}] {event}\n")

def load_brand_asset():
    """Retrieves the official Tackyon T-Symbol Band Image."""
    try:
        potential_files = ["logo.jpg", "logo.png", "t_symbol.jpg", "brand.jpeg"]
        for f in potential_files:
            if os.path.exists(f):
                with open(f, "rb") as img:
                    return base64.b64encode(img.read()).decode()
    except Exception as e:
        log_system_event(f"Asset Load Error: {str(e)}")
    return None

BRAND_LOGO_B64 = load_brand_asset()

def display_brand_identity(size="120px", pulse=True):
    """Renders the executive pulsing logo."""
    if BRAND_LOGO_B64:
        css_class = "brand-pulse" if pulse else ""
        st.markdown(f'''
            <div class="{css_class}" style="text-align: center; margin-bottom: 40px;">
                <img src="data:image/jpeg;base64,{BRAND_LOGO_B64}" 
                     style="width:{size}; border-radius: 30px; border: 2px solid #D4AC0D;">
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: center; font-size: 45px; font-weight: 900; color: #1B2631; letter-spacing: 5px;">TACKYON</div>', unsafe_allow_html=True)

def fetch_wisdom_module():
    """Retrieves formatted wisdom from Thirukural DB."""
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                verse = random.choice(db)
                return verse
    except Exception as e:
        log_system_event(f"DB Error: {str(e)}")
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- STAGE 3: STEALTH MEDIA EXTRACTION ---

def decrypt_resource(url):
    """High-security extraction of video and audio streams."""
    try:
        file_id = int(time.time())
        initialize_directories()
        
        # High-level headers to bypass 2026 platform filters
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 
            'outtmpl': f'temp/raw_source_{file_id}.mp4',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=True)
            video_id = meta['id']
            
        # Transcript Engine with Multi-Layer Fallback
        try:
            raw_t = YouTubeTranscriptApi.get_transcript(video_id)
            clean_t = " ".join([entry['text'] for entry in raw_t])
            source_mode = "Direct Neural Extraction"
        except:
            clean_t = f"Title: {meta.get('title')}. Description: {meta.get('description', 'N/A')}"
            source_mode = "Description Fallback"
            
        return {
            "title": meta.get('title', 'Tackyon Resource'),
            "id": video_id,
            "path": f'temp/raw_source_{file_id}.mp4',
            "transcript": clean_t,
            "fid": file_id,
            "mode": source_mode,
            "uploader": meta.get('uploader', 'Independent')
        }
    except Exception as e:
        log_system_event(f"Extraction Failure: {str(e)}")
        return None

# --- STAGE 4: PRODUCTION STUDIO (DUBBING & MERGE) ---

def process_neural_dub(resource_data, target_lang, persona):
    """Mutes original audio and overlays Neural AI Voice."""
    try:
        fid = resource_data['fid']
        # 1. Script Generation via Gemini 3 Flash
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        brain = genai.GenerativeModel('gemini-3-flash')
        
        script_prompt = f"""
        Role: Executive Scriptwriter.
        Task: Create a professional, perfectly timed dubbing script in {target_lang}.
        Persona: {persona}.
        Source: {resource_data['transcript'][:5000]}
        Return ONLY the translated script text.
        """
        script_res = brain.generate_content(script_prompt).text
        
        # 2. TTS Generation
        lang_map = {"Tamil": "ta", "English": "en", "Hindi": "hi", "French": "fr", "German": "de"}
        voice = gTTS(text=script_res, lang=lang_map.get(target_lang, "en"), slow=False)
        voice_path = f"temp/neural_voice_{fid}.mp3"
        voice.save(voice_path)
        
        # 3. FFmpeg Master Merge
        final_path = f"exports/Tackyon_Dub_{fid}.mp4"
        # Command logic: -an (mute source) | -map (combine video + new audio)
        merge_cmd = [
            'ffmpeg', '-i', resource_data['path'], '-i', voice_path,
            '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0',
            '-shortest', final_path, '-y'
        ]
        subprocess.run(merge_cmd, capture_output=True)
        
        return final_path
    except Exception as e:
        log_system_event(f"Dubbing Failure: {str(e)}")
        return None

# --- STAGE 5: EXECUTIVE FLOW MANAGEMENT ---

if "system_state" not in st.session_state:
    st.session_state.system_state = {
        "stage": "boot",
        "user": None,
        "history": [],
        "wisdom": fetch_wisdom_module(),
        "start_time": time.time()
    }

# BOOT ANIMATION
if st.session_state.system_state["stage"] == "boot":
    st.markdown('<div style="height: 20vh;"></div>', unsafe_allow_html=True)
    display_brand_identity(size="350px", pulse=True)
    
    boot_progress = st.progress(0)
    status_text = st.empty()
    
    boot_steps = ["Initializing Kernel...", "Loading Brand Assets...", "Syncing Thirukural DB...", "Calibrating Gemini 3 Flash...", "System Ready."]
    for i, step in enumerate(boot_steps):
        status_text.markdown(f"<p style='text-align:center;'>{step}</p>", unsafe_allow_html=True)
        boot_progress.progress((i + 1) * 20)
        time.sleep(0.4)
    
    st.session_state.system_state["stage"] = "onboarding"
    st.rerun()

# EXECUTIVE ONBOARDING
elif st.session_state.system_state["stage"] == "onboarding":
    w = st.session_state.system_state["wisdom"]
    st.markdown(f'''
        <div class="kural-container">
            <div class="kural-top">{w["top"]}</div>
            <div class="kural-bottom">{w["bottom"]}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="id-card">', unsafe_allow_html=True)
    display_brand_identity(size="100px")
    st.title("Executive Identification Protocol")
    
    # Collect Personal Metadata
    col1, col2, col3 = st.columns(3)
    with col1: first_name = st.text_input("Sovereign Name", placeholder="e.g. Prapanchan")
    with col2: gender = st.selectbox("Gender Identity", ["Male", "Female", "Non-Binary", "Executive"])
    with col3: age = st.number_input("System Age", 18, 99, 21)
    
    if st.button("AUTHORIZE ACCESS", use_container_width=True):
        if first_name:
            st.session_state.system_state["user"] = {"name": first_name, "gender": gender, "age": age}
            st.session_state.system_state["stage"] = "hub"
            log_system_event(f"User {first_name} Authorized.")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# THE INTELLIGENCE HUB
else:
    user = st.session_state.system_state["user"]
    wisdom = st.session_state.system_state["wisdom"]
    
    # --- SIDEBAR: ARCHIVE & STATUS ---
    with st.sidebar:
        display_brand_identity(size="130px")
        st.markdown(f"### <span class='status-badge'>Online</span> Executive: {user['name']}")
        st.divider()
        
        st.markdown("### 🕒 Intelligence Archive")
        if not st.session_state.system_state["history"]:
            st.write("No session records found.")
        for item in reversed(st.session_state.system_state["history"]):
            st.markdown(f'''
                <div class="sidebar-history-item">
                    <b>{item['title'][:30]}...</b><br>
                    <small>{item['time']} | {item['lang']}</small>
                </div>
            ''', unsafe_allow_html=True)
        
        st.divider()
        if st.button("PURGE ALL DATA"):
            st.session_state.system_state["history"] = []
            st.rerun()

    # --- MAIN HUB INTERFACE ---
    st.markdown(f'''
        <div class="kural-container">
            <div class="kural-top">{wisdom["top"]}</div>
            <div class="kural-bottom">{wisdom["bottom"]}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.title("Sovereign Intelligence Hub")
    
    # Advanced Parameter Grid
    with st.container():
        source_url = st.text_input("YouTube Target URL", placeholder="https://youtube.com/...")
        
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        with p_col1: 
            target_lang = st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi", "French", "German"])
        with p_col2: 
            summary_style = st.selectbox("Summary Architecture", ["Comprehensive Long Summary", "Strategic Points", "Actionable Deep Dive", "Exam Prep"])
        with p_col3: 
            voice_persona = st.selectbox("🎙️ Neural Persona", ["Male Executive", "Female Executive", "Deep Narrator"])
        with p_col4: 
            dubbing_toggle = st.selectbox("🎙️ Universal Dubbing", ["Inactive", "Execute Neural Overdub"])

    # EXECUTION BUTTON
    if st.button("START INTELLIGENCE EXTRACTION", use_container_width=True):
        if source_url:
            with st.status("Decrypting Media Streams...") as status:
                st.write("Fetching Resource Metadata...")
                res = decrypt_resource(source_url)
                
                if res:
                    st.write(f"Source Verified: {res['mode']}")
                    status.update(label="Analyzing Content...", state="running")
                    
                    # 1. GENERATE DEEP ANALYSIS
                    api_key = st.secrets["GEMINI_API_KEY"]
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-3-flash')
                    
                    prompt = f"""
                    Role: Elite Global Intelligence Analyst.
                    Objective: Provide an EXHAUSTIVE, 10-paragraph analysis.
                    Style: {summary_style}.
                    Language: {target_lang}.
                    Context: {res['transcript'][:7000]}
                    Ensure high-level vocabulary and strategic insights.
                    """
                    
                    intelligence_report = model.generate_content(prompt).text
                    
                    # Save to History
                    st.session_state.system_state["history"].append({
                        "title": res['title'],
                        "time": datetime.now().strftime("%H:%M"),
                        "lang": target_lang
                    })
                    
                    status.update(label="Intelligence Gathered.", state="complete")
                    
                    # RENDER REPORT WITH T-SYMBOL WATERMARK
                    st.markdown(f'''
                        <div class="report-frame">
                            <h2 style="color:#1B2631; margin-top:0;">📑 Report: {res['title']}</h2>
                            <p style="font-size:1.1em; color:#1C2833;">{intelligence_report}</p>
                            <div class="tackyon-watermark">Tackyon T Symbol © 2026</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # 2. HANDLE NEURAL DUBBING
                    if dubbing_toggle == "Execute Neural Overdub":
                        with st.spinner(f"Synthesizing {voice_persona} Voice... Merging Frames."):
                            
                            final_video = process_neural_dub(res, target_lang, voice_persona)
                            
                            if final_video:
                                st.divider()
                                st.subheader(f"📽️ Neural Dubbed Playback ({target_lang})")
                                st.video(final_video)
                                st.success(f"Production Complete: Original audio replaced with Neural AI Voice.")
                                
                                # Download Module
                                with open(final_video, "rb") as f:
                                    st.download_button(
                                        label="📥 DOWNLOAD DUBBED EXECUTIVE MEDIA",
                                        data=f,
                                        file_name=f"Tackyon_{res['fid']}.mp4",
                                        mime="video/mp4"
                                    )
                            else:
                                st.error("Neural Dubbing Engine failed at the Merge stage.")
                else:
                    st.error("Protocol Error: YouTube access restricted or private link.")
        else:
            st.warning("Input Required: Please enter a valid YouTube URL.")

# ==============================================================================
# END OF TACKYON SOVEREIGN CORE BUILD
# ==============================================================================