import streamlit as st
import time
import random
import uuid
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- PHASE 1 & 2: EXECUTIVE DESIGN SYSTEM ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    header, [data-testid="stHeader"], .stAppHeader { display: none !important; }
    .stApp { background-color: #FDFDFD; }
    .block-container { max-width: 550px !important; padding-top: 2rem !important; }

    /* Metallic T Animation */
    .metallic-t { 
        font-size: 120px; font-weight: 900; color: #1B2631; text-align: center;
        animation: pulse 2s ease-in-out; margin-top: 20vh;
    }
    @keyframes pulse { 0% { opacity:0; transform:scale(0.8); } 50% { opacity:1; transform:scale(1.05); } 100% { opacity:1; transform:scale(1); } }

    /* 4-3 Thirukural Gateway */
    .kural-box { text-align: center; padding: 50px 20px; background: #1B2631; border-radius: 30px; margin-bottom: 20px; color: #D4AC0D; }
    .kural-l1 { font-size: 1.4em; font-weight: 800; margin-bottom: 12px; }
    .kural-l2 { font-size: 1.2em; font-weight: 500; opacity: 0.9; }

    /* Clean Card UI */
    .exec-card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); border: 1px solid #F0F0F0; margin-bottom: 25px; }
    .assistant-logo { width: 35px; height: 35px; background: #1B2631; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; margin-right: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- PHASE 1: BRAND ONBOARDING ---
if "flow" not in st.session_state: st.session_state.flow = "splash"

if st.session_state.flow == "splash":
    st.markdown('<div class="metallic-t">T</div><p style="text-align:center; letter-spacing:5px;">TACKYON CORE</p>', unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.flow = "onboarding"
    st.rerun()

elif st.session_state.flow == "onboarding":
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.title("Onboarding")
    u_name = st.text_input("Full Name")
    u_age = st.number_input("Age", 18, 99, 25)
    u_gen = st.selectbox("Gender", ["Male", "Female", "Executive"])
    if st.button("AUTHORIZE", use_container_width=True):
        if u_name:
            st.session_state.user = {"name": u_name, "id": uuid.uuid4().hex[:8].upper()}
            st.session_state.flow = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.flow == "gateway":
    # Thirukural 4-3 format
    kurals = [{"l1": "அகர முதல எழுத்தெல்லாம்", "l2": "ஆதி பகவன் முதற்றே உலகு"}]
    k = random.choice(kurals)
    st.markdown(f'<div class="kural-box"><div class="kural-l1">{k["l1"]}</div><div class="kural-l2">{k["l2"]}</div></div>', unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.flow = "workspace"
    st.rerun()

# --- PHASE 3 & 4: WORKSPACE & ASSISTANT ---
else:
    st.title("Tackyon AI")
    st.caption(f"Session: {st.session_state.user['name']} | ID: {st.session_state.user['id']}")

    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    url = st.text_input("YouTube URL")
    lang = st.selectbox("Language", ["Tamil", "English", "Hindi", "French", "German", "Spanish"])
    
    if st.button("GENERATE REPORT", use_container_width=True):
        if url:
            try:
                v_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
                raw = YouTubeTranscriptApi.get_transcript(v_id)
                context = " ".join([t['text'] for t in raw])
                
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-2.5-flash')
                report = model.generate_content(f"Summarize in {lang}: {context[:5000]}").text
                st.write(report)
            except Exception as e:
                st.error("Daily Quota Reached. Please try again tomorrow.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Tackyon Assistant
    st.markdown('<div class="exec-card"><div style="display:flex; align-items:center;"><div class="assistant-logo">T</div><b>Tackyon Assistant</b></div>', unsafe_allow_html=True)
    q = st.chat_input("Ask Tackyon...")
    if q: st.write(f"🎙️ Analysis in progress...")
    st.markdown('</div>', unsafe_allow_html=True)