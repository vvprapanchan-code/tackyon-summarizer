import streamlit as st
import time
import base64
import os
import random
import json

# --- 1. THEME & DYNAMIC HEADER ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* Hide default headers but keep space for our custom Kural bar */
    header, [data-testid="stHeader"], .stAppHeader {
        display: none !important;
        visibility: hidden !important;
    }
    
    .block-container {
        padding-top: 0px !important;
        margin-top: -30px !important;
    }

    /* Kural Box - Fixed at top */
    .kural-box {
        background-color: #FDFEFE;
        border-bottom: 2px solid #D4AC0D;
        padding: 15px;
        text-align: center;
        width: 100%;
        margin-bottom: 30px;
    }
    .kural-line1 { font-size: 1.4em; font-weight: bold; color: #1B2631; margin-bottom: 5px; }
    .kural-line2 { font-size: 1.2em; color: #5D6D7E; }

    /* Executive Card Styling */
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 6px solid #1B2631;
        text-align: center; max-width: 850px; margin: auto;
    }

    /* Metallic T-Pulse Animation */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%); }
        50% { transform: scale(1.05); filter: brightness(125%); }
        100% { transform: scale(1); filter: brightness(100%); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PROVEN LOGO ENGINE ---
def load_logo_proven():
    """
    Scans the folder for logo.jpg or any image file. 
    Matches your folder structure: logo.jpg.
    """
    try:
        search_list = ["logo.jpg", "tackyon logo", "logo.jpeg", "tackyon logo jpeg"]
        for f in search_list:
            if os.path.exists(f):
                with open(f, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        
        for file in os.listdir("."):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                with open(file, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
    except:
        return None
    return None

logo_b64 = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    if logo_b64:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 20px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 15px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(f'<div style="text-align: center; font-size: 30px; font-weight: bold; color: #1B2631;">TACKYON AI</div>', unsafe_allow_html=True)

# --- 3. DATABASE ENGINE (ACCESSING YOUR UPLOADED JSON) ---
def get_random_kural():
    """Loads a random Kural from the thirukural.json you uploaded."""
    try:
        # Check if the file exists in your main folder
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except Exception as e:
        pass
    # Safety Backup
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 4. THE EXECUTIVE FLOW (CUMULATIVE & UNCHANGED) ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = get_random_kural()

# STAGE 1: LOGO ANIMATION
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="350px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: ONBOARDING (Kural in top box + Logo)
elif st.session_state.flow_stage == "onboarding":
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="90px") 
    st.title("Executive Onboarding")
    col1, col2, col3 = st.columns(3)
    with col1: name = st.text_input("Full Legal Name", placeholder="e.g. Prapanchan V V")
    with col2: gender = st.selectbox("Gender Identity", ["Male", "Female", "Executive"])
    with col3: age = st.number_input("Age Group", 18, 99, 19)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: GATEWAY (Same Kural + Logo)
elif st.session_state.flow_stage == "gateway":
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="80px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    st.info(f"Welcome, Executive {st.session_state.user['name']}. System ready.")
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB (Logo in sidebar, NO Kural)
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    render_t_logo(size="140px") 
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
        c1, c2, c3 = st.columns(3)
        with c1: 
            st.selectbox("Intelligence Language", [
                "Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada", 
                "French", "German", "Spanish", "Japanese", "Chinese", "Russian", 
                "Arabic", "Portuguese", "Italian", "Korean", "Turkish", "Dutch"
            ])
        with c2: 
            st.selectbox("Output Style", [
                "Executive Summary", "Strategic Points", "Exam Point of View", 
                "Twitter (X) Thread", "Threads Post", "Actionable Steps", "Detailed Notes"
            ])
        with c3: st.selectbox("Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("Initiating Tackyon Decryption Engine...")