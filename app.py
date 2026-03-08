# ==============================================================================
# TACKYON AI: SOVEREIGN EXECUTIVE WORKSPACE (BUILD 2026.03.08)
# ARCHITECT: PRAPANCHAN | CORE ENGINE: GEMINI 2.5 FLASH
# FEATURES: PHASE 1-4 (EXCLUDING DUBBING/ADS)
# ==============================================================================

import streamlit as st
import time
import base64
import os
import random
import json
import uuid
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
from datetime import datetime

# --- STAGE 0: THE SOVEREIGN STYLE ENGINE ---
st.set_page_config(page_title="Tackyon AI", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Executive UI Overrides */
    header, [data-testid="stHeader"], .stAppHeader { display: none !important; }
    .block-container { padding-top: 0px !important; margin-top: -20px !important; }
    
    /* Font Hub (Phase 2) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Playfair+Display:ital,wght@0,400;0,900;1,400&display=swap');
    
    .main { background-color: #FDFDFD; }
    
    /* Card Interface (Phase 2) */
    .executive-card {
        background: #FFFFFF; padding: 40px; border-radius: 25px;
        border-left: 12px solid #1B2631; margin-bottom: 30px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.04); position: relative;
    }
    
    .t-watermark {
        position: absolute; bottom: 15px; right: 25px; font-size: 0.75em;
        color: rgba(27, 38, 49, 0.25); font-weight: 900; letter-spacing: 3px;
    }

    /* Metallic Animation (Phase 1) */
    .metallic-t {
        font-family: 'Inter', sans-serif; font-weight: 900; font-size: 120px;
        background: linear-gradient(135deg, #1B2631 0%, #5D6D7E 50%, #1B2631 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shine 2s ease-in-out; text-align: center;
    }
    
    @keyframes shine {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }

    .wisdom-frame {
        text-align: center; padding: 40px; border-bottom: 3px solid #D4AC0D;
        margin-bottom: 40px; background: white; border-radius: 0 0 40px 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STAGE 1: ASSETS & IDENTITY (PHASE 1) ---

def get_tackyon_id():
    """Generates a hardware-style token for Device-Locked Identity."""
    if 'tackyon_token' not in st.session_state:
        # In a real app, this would query hardware UUID; here we simulate it locally
        st.session_state.tackyon_token = str(uuid.uuid4())[:13].upper()
    return st.session_state.tackyon_token

def load_kurals():
    """Phase 1: The Thirukural Gateway (Random 1 of 50)."""
    return [
        {"ta": "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு.", "en": "A, as its first of letters, every speech maintains; The Primal Deity is first through all the world's domains."},
        {"ta": "கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.", "en": "So learn that you may faultless learn, and having learnt, remain obedient to the lessons you have learnt."},
        {"ta": "எப்பொருள் யார்யார்வாய்க் கேட்பினும் அப்பொருள் மெய்ப்பொருள் காண்ப தறிவு.", "en": "To discern the truth in everything, by whomsoever spoken, is wisdom."},
        # ... (Extended list of 50 Kurals)
    ]

# --- STAGE 2: INTELLIGENCE HUB (PHASE 3) ---

def extract_transcript(url):
    """Deep Intelligence Engine: yt_dlp & Transcript fallback."""
    v_id = ""
    try:
        if "v=" in url: v_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url: v_id = url.split("youtu.be/")[1].split("?")[0]
        
        raw_t = YouTubeTranscriptApi.get_transcript(v_id)
        return " ".join([t['text'] for t in raw_t]), "Full Transcript"
    except:
        # Smart Discovery Fallback (Phase 3)
        try:
            with YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return f"Title: {info['title']}. Channel: {info['uploader']}. Description: {info['description']}", "Metadata Fallback"
        except:
            return None, None

def generate_intelligence(content, style, lang, mode):
    """Tackyon Brain Execution via Gemini 2.5 Flash."""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        Role: You are Tackyon AI, an elite Executive Intelligence Officer. 
        Creator: Prapanchan (Only mention if explicitly asked).
        Task: Analyze the following content and provide a {style} in {lang}. 
        Format: Use {mode} (Paragraphs/Bullets).
        
        Content: {content[:8000]}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Intelligence Error: {str(e)}"

# --- STAGE 3: EXECUTIVE WORKFLOW ---

if "auth_stage" not in st.session_state:
    st.session_state.auth_stage = "splash"

# 1. SPLASH SCREEN (PHASE 1)
if st.session_state.auth_stage == "splash":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="metallic-t">T</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-weight:300; letter-spacing:5px;">TACKYON CORE</p>', unsafe_allow_html=True)
    time.sleep(2) # 2-second animation signal
    st.session_state.auth_stage = "identity"
    st.rerun()

# 2. IDENTITY PORTAL (PHASE 1)
elif st.session_state.auth_stage == "identity":
    st.markdown('<div class="executive-card" style="max-width:600px; margin: 100px auto;">', unsafe_allow_html=True)
    st.title("Executive Onboarding")
    name = st.text_input("Full Name")
    c1, c2 = st.columns(2)
    with c1: gender = st.selectbox("Gender", ["Male", "Female", "Non-Binary"])
    with c2: age = st.number_input("Age", 18, 99, 30)
    
    if st.button("AUTHORIZE DEVICE", use_container_width=True):
        if name:
            st.session_state.user_data = {"name": name, "gender": gender, "age": age, "id": get_tackyon_id()}
            st.session_state.auth_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 3. THIRUKURAL GATEWAY (PHASE 1)
elif st.session_state.auth_stage == "gateway":
    kural = random.choice(load_kurals())
    st.markdown(f"""
        <div class="wisdom-frame">
            <h1 style="color:#1B2631; font-family:'Playfair Display';">{kural['ta']}</h1>
            <p style="font-style:italic; color:#5D6D7E;">"{kural['en']}"</p>
            <br>
            <p style="font-size:0.8em; letter-spacing:2px;">TACKYON GATEWAY OPENING...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.auth_stage = "workspace"
    st.rerun()

# 4. PROFESSIONAL WORKSPACE (PHASE 2-4)
else:
    # Sidebar Command Center (Phase 2)
    with st.sidebar:
        st.markdown(f"### ID: {st.session_state.user_data['id']}")
        st.markdown("---")
        st.subheader("Typography Hub")
        font_style = st.radio("Executive Font", ["Inter (Modern)", "Playfair (Classic)"])
        st.subheader("Theme Customization")
        theme_color = st.color_picker("Accent Color", "#1B2631")
        st.markdown("---")
        st.caption("Tackyon AI v2.5.S")

    # Main Workspace
    st.title(f"Sovereign Workspace: {st.session_state.user_data['name']}")
    
    
    
    # Universal Input (Phase 3)
    url = st.text_input("Universal Intelligence Input (YouTube URL)", placeholder="Paste URL here...")
    
    tab1, tab2, tab3 = st.tabs(["Deep Summary", "Executive Insights", "Assistant"])
    
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1: target_lang = st.selectbox("Language", ["Tamil", "English", "French", "German", "Hindi", "Japanese", "Spanish"])
        with c2: style = st.selectbox("Style", ["Executive Summary", "Twitter Thread", "Exam Point of View"])
        with c3: mode = st.selectbox("Format", ["Point-wise Bullets", "Clean Paragraphs"])
        
        if st.button("EXECUTE BRAIN ANALYSIS", use_container_width=True):
            if url:
                with st.status("Tackyon Brain Executing...") as s:
                    content, source = extract_transcript(url)
                    if content:
                        s.update(label=f"Decoding via Gemini 2.5 Flash ({source})...", state="running")
                        report = generate_intelligence(content, style, target_lang, mode)
                        
                        st.markdown(f"""
                            <div class="executive-card">
                                <h3 style="color:{theme_color};">Intelligence Report</h3>
                                <p style="font-family:'{font_style.split()[0]}'; white-space: pre-wrap;">{report}</p>
                                <div class="t-watermark">TACKYON T SYMBOL</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Branded Export (Phase 4)
                        export_text = f"TACKYON AI REPORT\nUser: {st.session_state.user_data['name']}\nDate: {datetime.now()}\n\n{report}\n\n© TACKYON AI - PRAPANCHAN CREATION"
                        st.download_button("📥 DOWNLOAD BRANDED REPORT (.TXT)", export_text, f"Tackyon_Report_{st.session_state.user_data['id']}.txt")
                    else:
                        st.error("Access Denied: Could not retrieve video data.")

    with tab2:
        st.info("Insights Engine: Historical patterns and creator metadata are analyzed here.")

    with tab3:
        # The Discrete Assistant (Phase 4)
        st.subheader("Tackyon Discrete Assistant")
        if "chat_log" not in st.session_state: st.session_state.chat_log = []
        
        for msg in st.session_state.chat_log:
            with st.chat_message(msg["role"]): st.write(msg["content"])
            
        if prompt := st.chat_input("Ask Tackyon about the video..."):
            st.session_state.chat_log.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            
            with st.chat_message("assistant"):
                # Real-time assistant call
                response = generate_intelligence(prompt, "Discrete Answer", "English", "Paragraph")
                st.write(response)
                st.session_state.chat_log.append({"role": "assistant", "content": response})