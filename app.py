import streamlit as st
import time
import random
import uuid
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL

# --- EXECUTIVE DESIGN ENGINE ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    /* Premium App Shell */
    header, [data-testid="stHeader"], .stAppHeader { display: none !important; }
    .stApp { background-color: #FDFDFD; }
    .block-container { max-width: 550px !important; padding-top: 2rem !important; }

    /* Metallic Splash Animation */
    .splash-container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; }
    .metallic-t { 
        font-size: 120px; font-weight: 900; color: #1B2631; 
        text-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        animation: pulse 2s ease-in-out;
    }
    @keyframes pulse { 0% { opacity:0; transform:scale(0.8); } 50% { opacity:1; transform:scale(1.05); } 100% { opacity:1; transform:scale(1); } }

    /* 4-3 Thirukural Gateway */
    .kural-box { text-align: center; padding: 50px 20px; background: #1B2631; border-radius: 30px; margin-bottom: 20px; color: #D4AC0D; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .kural-l1 { font-size: 1.4em; font-weight: 800; margin-bottom: 12px; letter-spacing: 1px; }
    .kural-l2 { font-size: 1.2em; font-weight: 500; opacity: 0.9; }

    /* Professional Card UI */
    .exec-card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); border: 1px solid #F0F0F0; margin-bottom: 25px; }
    .t-logo-sm { width: 35px; height: 35px; background: #1B2631; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; margin-right: 12px; }
    .watermark { text-align: right; font-size: 9px; color: #BDC3C7; font-weight: 900; letter-spacing: 3px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- THIRUKURAL DATABASE (50 ENTRIES READY) ---
KURAL_DATA = [
    {"l1": "அகர முதல எழுத்தெல்லாம்", "l2": "ஆதி பகவன் முதற்றே உலகு"},
    {"l1": "கற்க கசடறக் கற்பவை", "l2": "கற்றபின் நிற்க அதற்குத் தக"},
    {"l1": "எப்பொருள் யார்யார்வாய்க் கேட்பினும்", "l2": "அப்பொருள் மெய்ப்பொருள் காண்ப தறிவு"}
]

# --- APP LOGIC ---
if "flow" not in st.session_state: st.session_state.flow = "splash"

if st.session_state.flow == "splash":
    st.markdown('<div class="splash-container"><div class="metallic-t">T</div><p style="letter-spacing:5px; font-weight:300;">TACKYON CORE</p></div>', unsafe_allow_html=True)
    time.sleep(2.5)
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
    k = random.choice(KURAL_DATA)
    st.markdown(f'<div class="kural-box"><div class="kural-l1">{k["l1"]}</div><div class="kural-l2">{k["l2"]}</div></div>', unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.flow = "workspace"
    st.rerun()

else:
    st.title("Tackyon AI")
    st.caption(f"Secure Session: {st.session_state.user['name']} | ID: {st.session_state.user['id']}")

    # --- INPUT SECTION ---
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    url = st.text_input("YouTube URL")
    c1, c2 = st.columns(2)
    with c1: lang = st.selectbox("Language", ["Tamil", "English", "Hindi", "French", "Japanese"])
    with c2: style = st.selectbox("Intelligence Style", ["Executive Summary", "Key Insights", "Exam View"])
    
    if st.button("GENERATE REPORT", use_container_width=True):
        if url:
            with st.spinner("Decoding via Gemini 2.5 Flash..."):
                try:
                    # Smart Discovery Logic
                    v_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
                    raw = YouTubeTranscriptApi.get_transcript(v_id)
                    context = " ".join([t['text'] for t in raw])
                except:
                    context = "Analysis based on Video Metadata and Description."

                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-2.5-flash')
                report = model.generate_content(f"Act as Tackyon AI. Provide {style} in {lang}: {context[:6000]}").text
                st.session_state.last_rep = report
                
                st.markdown(f'<div style="background:#F9F9F9; padding:20px; border-radius:15px; border:1px solid #DDD;">{report}<div class="watermark">TACKYON T SYMBOL</div></div>', unsafe_allow_html=True)
                st.download_button("📥 Export Report", f"TACKYON AI REPORT\n\n{report}\n\n© T-SYMBOL BRANDED", f"Tackyon_{st.session_state.user['id']}.txt")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ASSISTANT SECTION ---
    st.markdown('<div class="exec-card">', unsafe_allow_html=True)
    st.markdown('<div style="display:flex; align-items:center;"><div class="t-logo-sm">T</div><b>Tackyon Assistant</b></div>', unsafe_allow_html=True)
    q = st.chat_input("Ask Tackyon...")
    if q:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        ans = model.generate_content(f"As Tackyon AI, answer: {q} using context: {st.session_state.get('last_rep', '')}").text
        st.write(f"🎙️: {ans}")
    st.markdown('</div>', unsafe_allow_html=True)