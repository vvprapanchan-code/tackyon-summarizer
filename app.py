import streamlit as st
import time
import base64
import os
import random

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

# --- 2. LOGO ENGINE (JPEG Focus) ---
def load_executive_logo():
    # Force search for logo.jpg as a JPEG
    if os.path.exists("logo.jpg"):
        with open("logo.jpg", "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = load_executive_logo()

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
        st.markdown(f'<div style="text-align: center; font-size: 30px; font-weight: bold;">T-CORE</div>', unsafe_allow_html=True)

# Strict 4-3 Word Format for Kural
KURALS = [
    {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"},
    {"top": "அகர முதல எழுத்தெல்லாம் ஆதி", "bottom": "பகவன் முதற்றே உலகு"},
    {"top": "அன்பிலார் எல்லாம் தமக்குரியர் அன்புடையார்", "bottom": "என்பும் உரியர் பிறர்க்கு"}
]

# --- 3. THE EXECUTIVE FLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = random.choice(KURALS)

# STAGE 1: LOGO ANIMATION (Every time app opens)
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="350px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: ONBOARDING (Kural on top)
elif st.session_state.flow_stage == "onboarding":
    # Show Kural in Box
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_t_logo(size="90px") # Logo present here
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
    render_t_logo(size="80px") # Logo present here
    st.subheader("Intelligence Gateway | Daily Reflection")
    st.info(f"Welcome, Executive {st.session_state.user['name']}. System ready.")
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB (Logo visible, NO Kural)
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    render_t_logo(size="140px") # Logo present here
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("YouTube Resource URL", placeholder="Paste Link")
        c1, c2, c3 = st.columns(3)
        with c1: st.selectbox("Language", ["Tamil", "English", "Hindi"])
        with c2: st.selectbox("Output Style", ["Summary", "Strategic Points"])
        with c3: st.selectbox("Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")