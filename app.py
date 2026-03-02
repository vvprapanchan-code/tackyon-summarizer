import streamlit as st
import time
import base64
import os
import random

# --- 1. UI ARCHITECTURE (THE "KURAL-IN-A-BOX" FIX) ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* 1. UTILIZE THE TOP WHITE BOX FOR THE KURAL */
    header, [data-testid="stHeader"], .stAppHeader {
        background-color: #F8F9FA !important;
        height: 100px !important;
        border-bottom: 2px solid #1B2631;
        display: block !important;
        visibility: visible !important;
    }
    
    /* 2. PADDING TO PREVENT LOGO CUT-OFF */
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* 3. KURAL FORMATTING (STRICT 4-3 WORD RULE) */
    .kural-box {
        text-align: center;
        width: 100%;
        position: fixed;
        top: 15px;
        z-index: 999;
    }
    .kural-top { font-size: 1.2em; font-weight: bold; color: #1B2631; }
    .kural-bottom { font-size: 1.0em; color: #5D6D7E; }

    /* EXECUTIVE CARD DESIGN */
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 6px solid #1B2631;
        text-align: center; max-width: 800px; margin: auto;
    }

    /* PULSE ANIMATION */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%); }
        50% { transform: scale(1.05); filter: brightness(120%); }
        100% { transform: scale(1); filter: brightness(100%); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE TRIPLE-LAYER LOGO SCANNER ---
def load_logo_robustly():
    """Searches for the logo using every possible name and extension."""
    search_list = ["logo.jpg", "tackyon logo", "logo.jpeg", "tackyon logo.jpeg", "17975.png"]
    for f in search_list:
        if os.path.exists(f):
            with open(f, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

logo_b64 = load_logo_robustly()

# Strict 4-3 Format Data
KURALS = [
    {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"},
    {"top": "அகர முதல எழுத்தெல்லாம் ஆதி", "bottom": "பகவன் முதற்றே உலகு"},
    {"top": "அன்பிலார் எல்லாம் தமக்குரியர் அன்புடையார்", "bottom": "என்பும் உரியர் பிறர்க்கு"}
]

def render_logo(size="100px", animate=False):
    if logo_b64:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 20px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 15px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        # If it fails, show high-end text instead of emoji
        st.markdown(f'<div style="text-align: center; font-size: 30px; font-weight: bold; color: #1B2631;">T-CORE AI</div>', unsafe_allow_html=True)

# --- 3. THE BRANDED FLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = random.choice(KURALS)

# STAGE 1: 2-SECOND FULLSCREEN PULSE
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    render_logo(size="350px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# DISPLAY KURAL AT THE TOP (EXCEPT DURING SPLASH)
if st.session_state.flow_stage != "animation":
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-top">{st.session_state.daily_kural['top']}</div>
            <div class="kural-bottom">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True) # Space for Kural

# STAGE 2: ONBOARDING
if st.session_state.flow_stage == "onboarding":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    render_logo(size="90px")
    st.title("Executive Onboarding")
    col1, col2, col3 = st.columns(3)
    with col1: name = st.text_input("Full Legal Name", placeholder="e.g. Prapanchan V V")
    with col2: gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with col3: age = st.number_input("Age", 18, 99, 19)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "hub"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: THE HUB
elif st.session_state.flow_stage == "hub":
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    render_logo(size="130px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
        c1, c2, c3 = st.columns(3)
        with c1: st.selectbox("Language", ["Tamil", "English", "Hindi"])
        with c2: st.selectbox("Style", ["Summary", "Key Points"])
        with c3: st.selectbox("Font", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")