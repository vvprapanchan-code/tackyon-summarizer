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

# --- 0. CRITICAL PYTHON 3.13 FIX ---
# Restores the removed audio engine required for media processing
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
    except ImportError:
        st.error("Protocol Alert: 'audioop-lts' missing in requirements.txt.")

from pydub import AudioSegment

# --- 1. EXECUTIVE THEME ARCHITECTURE ---
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

# --- 2. BRANDING & DATA ENGINES ---
def load_logo_proven():
    try:
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
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 3. STEALTH MEDIA PIPELINE ---
def get_video_data_pro(url):
    try:
        if not os.path.exists("temp"): os.makedirs("temp")
        file_id = int(time.time())
        
        # Optimized for 2026 YouTube algorithms to prevent "Access Denied" errors
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', 
            'outtmpl': f'temp/video_{file_id}.mp4',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            metadata = {
                "title": info.get('title', 'Tackyon Executive Dub'),
                "id": info['id'],
                "desc": info.get('description', 'No description available.')
            }
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(info['id'])
            content = " ".join([t['text'] for t in transcript_list])
            mode = "full_transcript"
        except: 
            content = f"Title: {metadata['title']}. Desc: {metadata['desc']}"
            mode = "metadata_fallback"
            
        return metadata, content, f'temp/video_{file_id}.mp4', file_id, mode
    except Exception as e:
        return None, None, None, None, f"error: {str(e)}"

# --- 4. NEURAL BRAIN (GEMINI 3 FLASH) ---
def generate_ai_executive(prompt_text):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # Using the flagship Gemini 3 Flash engine
        model = genai.GenerativeModel('gemini-3-flash')
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"AI Engine Exception: {str(e)}"

# --- 5. THE PRODUCTION STUDIO (DUBBING & MERGE) ---
def create_executive_dub(video_path, content, lang_code, file_id, voice_type):
    try:
        # Create professional script
        script_prompt = f"Convert this transcript into a clear, executive speech in {lang_code}. Ensure the script length matches the original video pace: {content[:4500]}"
        script = generate_ai_executive(script_prompt)
        
        # Neural Voice Synthesis
        tts = gTTS(text=script, lang=lang_code, slow=False)
        audio_path = f"temp/audio_{file_id}.mp3"
        tts.save(audio_path)
        
        # FFmpeg Executive Multiplexer: Mute original and merge with AI Voice
        output_path = f"temp/Tackyon_Dub_{file_id}.mp4"
        # -an mutes original; -map combines video and new audio
        cmd = [
            'ffmpeg', '-i', video_path, '-i', audio_path,
            '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v:0', '-map', '1:a:0',
            '-shortest', output_path, '-y'
        ]
        subprocess.run(cmd, capture_output=True)
        return output_path
    except:
        return None

# --- 6. SYSTEM WORKFLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.update({
        "flow_stage": "animation", 
        "history": [], 
        "daily_kural": get_random_kural(),
        "user_profile": None
    })

if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 22vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="400px", animate=True)
    pb = st.progress(0)
    for p in range(100):
        time.sleep(0.015)
        pb.progress(p + 1)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

elif st.session_state.flow_stage == "onboarding":
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="110px") 
    st.title("System Access: Identification")
    c1, c2, c3 = st.columns(3)
    with c1: f_name = st.text_input("First Name", placeholder="e.g. Prapanchan")
    with c2: gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with c3: age = st.number_input("Age", 18, 99, 21)
    
    if st.button("Initialize Deep Intelligence", use_container_width=True):
        if f_name:
            st.session_state.user_profile = {"name": f_name, "gender": gender, "age": age}
            st.session_state.flow_stage = "hub"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    with st.sidebar:
        render_t_logo(size="140px") 
        st.markdown(f"### Executive: {st.session_state.user_profile['name']}")
        st.divider()
        st.markdown("### 🕒 Intelligence Archive")
        if not st.session_state.history: st.write("No session records found.")
        for item in reversed(st.session_state.history):
            st.markdown(f'<div class="history-card"><b>{item["title"][:28]}...</b></div>', unsafe_allow_html=True)

    st.title("Executive Intelligence Hub")
    st.markdown(f'<div class="kural-box"><div class="kural-line1">{st.session_state.daily_kural["top"]}</div><div class="kural-line2">{st.session_state.daily_kural["bottom"]}</div></div>', unsafe_allow_html=True)

    with st.expander("📥 Resource Configuration", expanded=True):
        url = st.text_input("YouTube URL", placeholder="Paste Link Here")
        col1, col2, col3, col4 = st.columns(4)
        with col1: analysis_lang = st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi", "French"])
        with col2: style = st.selectbox("Summary Architecture", ["Comprehensive Long Summary", "Strategic Points"])
        with col3: persona = st.selectbox("🎙️ Voice Persona", ["Male Executive", "Female Executive"])
        with col4: dub_lang = st.selectbox("🎙️ Universal Dubbing", ["No Dubbing", "Tamil", "English", "Hindi"])

    if st.button("EXECUTE TOTAL SYSTEM ANALYSIS", use_container_width=True):
        if url:
            with st.spinner("Initializing Neural Production... (Decrypted Access to YouTube)"):
                
                m, content, video_path, f_id, mode = get_video_data_pro(url)
                
                if m:
                    st.subheader(f"📑 Intelligence Report: {m['title']}")
                    # 1. GENERATE DEEP ANALYSIS
                    prompt = f"Provide an exhaustive analysis in {analysis_lang} for this content: {content[:6000]}. Style: {style}."
                    analysis = generate_ai_executive(prompt)
                    
                    if not any(h['title'] == m['title'] for h in st.session_state.history):
                        st.session_state.history.append({"title": m['title']})
                    
                    st.markdown(f'''
                        <div class="analysis-result">
                            <b>Executive Analysis ({analysis_lang}):</b><br><br>{analysis}
                            <div class="watermark-text">tackyon t symbol © 2026</div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # 2. GENERATE DUBBED VIDEO
                    if dub_lang != "No Dubbing":
                        with st.spinner(f"Synthesizing {persona} Neural Voice... Merging with Video."):
                            l_map = {"Tamil": "ta", "English": "en", "Hindi": "hi"}
                            final_video = create_executive_dub(video_path, content, l_map[dub_lang], f_id, persona)
                            
                            if final_video:
                                st.divider()
                                st.subheader(f"📽️ Neural Dubbed Playback ({dub_lang})")
                                st.video(final_video)
                                st.success(f"Production Complete: Original audio replaced with {persona} AI Voice.")
                                
                                with open(final_video, "rb") as file:
                                    st.download_button(label="📥 Download Dubbed Video", data=file, file_name=f"Tackyon_{dub_lang}.mp4", mime="video/mp4")
                else: st.error(f"Critical System Failure: {mode}")