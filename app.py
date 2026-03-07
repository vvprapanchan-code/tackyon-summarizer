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
        padding: 25px;
        text-align: center;
        width: 100%;
        margin-bottom: 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .kural-line1 { font-size: 1.7em; font-weight: bold; color: #1B2631; margin-bottom: 10px; }
    .kural-line2 { font-size: 1.4em; color: #5D6D7E; font-style: italic; }

    .executive-card {
        background: white; 
        padding: 50px; 
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15); 
        border-top: 10px solid #1B2631;
        text-align: center; 
        max-width: 1000px; 
        margin: auto;
    }

    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%); }
        50% { transform: scale(1.08); filter: brightness(140%); }
        100% { transform: scale(1); filter: brightness(100%); }
    }
    .pulse-layer { animation: t-pulse 3s infinite ease-in-out; }

    .analysis-result {
        background: #F4F6F7; 
        padding: 40px; 
        border-radius: 20px;
        border-left: 12px solid #1B2631; 
        text-align: left;
        margin-top: 30px; 
        color: #1C2833; 
        line-height: 2.0;
        position: relative;
    }

    .watermark-text {
        position: absolute;
        bottom: 10px;
        right: 15px;
        font-size: 0.7em;
        color: rgba(27, 38, 49, 0.4);
        font-weight: bold;
    }
    
    .history-card {
        background: #EBEDEF;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #D4AC0D;
        transition: 0.3s;
    }
    .history-card:hover { background: #D5DBDB; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO & BRANDING ENGINES ---
def load_logo_proven():
    try:
        # Search for the "tackyon t symbol" band image
        search_list = ["logo.jpg", "logo.png", "t_symbol.jpg", "logo.jpeg"]
        for f in search_list:
            if os.path.exists(f):
                with open(f, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    except: return None
    return None

logo_data_b64 = load_logo_proven()

def render_t_logo(size="120px", animate=False):
    if logo_data_b64:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(f'<div class="{anim_class}" style="text-align: center; margin-bottom: 30px;"><img src="data:image/jpeg;base64,{logo_data_b64}" style="width:{size}; border-radius: 25px;"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: center; font-size: 40px; font-weight: bold; color: #1B2631;">TACKYON</div>', unsafe_allow_html=True)

def get_random_kural():
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except: pass
    # Default 4-3 format kural
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 3. THE STEALTH MEDIA ENGINE (FFMPEG + YT-DLP) ---
def get_video_data_pro(url):
    try:
        if not os.path.exists("temp"): os.makedirs("temp")
        file_id = int(time.time())
        
        # Stealth options for 2026 YouTube algorithms
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 
            'outtmpl': f'temp/video_{file_id}.mp4',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'Tackyon Executive Dub')
            video_id = info['id']
            metadata = {
                "title": video_title,
                "id": video_id,
                "desc": info.get('description', 'No description available.'),
                "thumb": info.get('thumbnail', '')
            }
        
        # Transcript retrieval with fallback to metadata
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            content = " ".join([t['text'] for t in transcript_list])
            mode = "full_transcript"
        except: 
            content = f"Resource Title: {video_title}. Context: {metadata['desc']}"
            mode = "metadata_fallback"
            
        return metadata, content, f'temp/video_{file_id}.mp4', file_id, mode
            
    except Exception as e:
        return None, None, None, None, f"error: {str(e)}"

# --- 4. THE AI BRAIN (GEMINI 3 FLASH) ---
def generate_ai_executive(prompt_text):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # Using the advanced Gemini 3 Flash model
        model = genai.GenerativeModel('gemini-3-flash')
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"AI Engine Exception: {str(e)}"

# --- 5. NEURAL DUBBING & MEDIA MERGE ---
def create_executive_dub(video_path, content, lang_code, file_id, voice_type):
    try:
        # Create professional script
        script_prompt = f"Rewrite this content into a professional, executive-level speech for a {voice_type} voice in {lang_code}. Focus on clear articulation: {content[:5000]}"
        script = generate_ai_executive(script_prompt)
        
        # Neural Voice Synthesis
        tts = gTTS(text=script, lang=lang_code, slow=False)
        audio_path = f"temp/audio_{file_id}.mp3"
        tts.save(audio_path)
        
        # Executive FFmpeg Merge (Mute original + Replace with Tackyon AI Voice)
        output_path = f"temp/Tackyon_Final_{file_id}.mp4"
        # -an removes original; -shortest ensures it matches duration
        cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest {output_path} -y"
        subprocess.run(cmd, shell=True)
        
        return output_path
    except:
        return None

# --- 6. THE EXECUTIVE WORKFLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.update({
        "flow_stage": "animation", 
        "history": [], 
        "daily_kural": get_random_kural(),
        "user_profile": None
    })

# STAGE 1: METALLIC LOGO PULSE
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 22vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="400px", animate=True)
    pb = st.progress(0)
    for p in range(100):
        time.sleep(0.015)
        pb.progress(p + 1)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING
elif st.session_state.flow_stage == "onboarding":
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="110px") 
    st.title("System Access: Identification")
    # Collect mandatory executive data
    c1, c2, c3 = st.columns(3)
    with c1: f_name = st.text_input("First Name", placeholder="Executive Name")
    with c2: gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with c3: age = st.number_input("Age", 18, 99, 21)
    
    if st.button("Initialize Deep Intelligence", use_container_width=True):
        if f_name:
            st.session_state.user_profile = {"name": f_name, "gender": gender, "age": age}
            st.session_state.flow_stage = "hub"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: THE INTELLIGENCE HUB
else:
    # --- Sidebar Configuration ---
    with st.sidebar:
        render_t_logo(size="140px") 
        st.markdown(f"### Executive: {st.session_state.user_profile['name']}")
        st.info(f"Identity: {st.session_state.user_profile['gender']} | Age: {st.session_state.user_profile['age']}")
        st.divider()
        st.markdown("### 🕒 Intelligence Archive")
        if not st.session_state.history: st.write("No session records found.")
        for item in reversed(st.session_state.history):
            st.markdown(f'<div class="history-card"><b>{item["title"][:28]}...</b><br><small>{item["time"]}</small></div>', unsafe_allow_html=True)
        if st.button("Purge Archive"):
            st.session_state.history = []
            st.rerun()

    st.title("Executive Intelligence Hub")
    # Display 4-3 Thirukural
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)

    with st.expander("📥 Resource Configuration", expanded=True):
        url = st.text_input("YouTube Resource URL", placeholder="Enter URL to begin decryption...")
        
        # Master Row Configuration
        col1, col2, col3, col4 = st.columns(4)
        with col1: analysis_lang = st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi", "French"])
        with col2: style = st.selectbox("Summary Architecture", ["Comprehensive Long Summary", "Strategic Points", "Actionable Deep Dive"])
        with col3: persona = st.selectbox("🎙️ Voice Persona", ["Male Executive", "Female Executive"])
        with col4: dub_lang = st.selectbox("🎙️ Universal Dubbing", ["No Dubbing", "Tamil", "English", "Hindi"])

    if st.button("EXECUTE TOTAL SYSTEM ANALYSIS", use_container_width=True):
        if url:
            with st.spinner("Initializing Neural Production... (Decrypted Access to YouTube)"):
                # Stealth Data Retrieval
                m, content, video_path, f_id, mode = get_video_data_pro(url)
                
                if m:
                    st.subheader(f"📑 Intelligence Report: {m['title']}")
                    if mode == "metadata_fallback": 
                        st.warning("Encryption Notice: Direct transcript access restricted. Utilizing metadata fallback engine.")
                    
                    # 1. GENERATE EXHAUSTIVE ANALYSIS
                    analysis_prompt = f"Act as an Elite Consultant. Provide an extremely long, exhaustive, 10-paragraph analysis in {analysis_lang} for this content: {content[:6000]}. Style: {style}."
                    analysis_output = generate_ai_executive(analysis_prompt)
                    
                    # Update History Archive
                    if not any(h['title'] == m['title'] for h in st.session_state.history):
                        st.session_state.history.append({"title": m['title'], "time": datetime.now().strftime("%H:%M")})
                    
                    # Display Result with Tackyon T-Symbol Watermark
                    st.markdown(f'''
                        <div class="analysis-result">
                            <b>Executive Analysis ({analysis_lang}):</b><br><br>{analysis_output}
                            <div class="watermark-text">tackyon t symbol © 2026</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # 2. GENERATE DUBBED VIDEO
                    if dub_lang != "No Dubbing":
                        with st.spinner(f"Synthesizing {persona} Neural Voice ({dub_lang})..."):
                            
                            l_map = {"Tamil": "ta", "English": "en", "Hindi": "hi"}
                            # Execute FFmpeg Merge
                            final_video = create_executive_dub(video_path, content, l_map[dub_lang], f_id, persona)
                            
                            if final_video:
                                st.divider()
                                st.subheader(f"📽️ Neural Dubbed Playback ({dub_lang})")
                                st.video(final_video)
                                st.success(f"Production Complete: Original audio replaced with {persona} AI Voice.")
                                
                                # Download Capability
                                with open(final_video, "rb") as file:
                                    st.download_button(
                                        label=f"📥 Download Tackyon_{dub_lang}_Dub.mp4", 
                                        data=file, 
                                        file_name=f"Tackyon_{dub_lang}_Executive.mp4", 
                                        mime="video/mp4"
                                    )
                            else: st.error("Neural Dubbing Engine failed at the media-merge stage.")
                else: st.error(f"Critical System Failure: {mode}")
        else: st.warning("Protocol Error: Please provide a valid Resource URL.")