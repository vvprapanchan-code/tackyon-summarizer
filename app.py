import streamlit as st
import time
import base64
import os
import random

# --- 1. UI ARCHITECTURE (THE INSPIRATION BAR) ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* 1. UTILIZING THE TOP BOX FOR THE KURAL */
    header, [data-testid="stHeader"] {
        background-color: #F8F9FA;
        height: 120px !important;
        border-bottom: 2px solid #1B2631;
    }
    
    /* 2. LOGO PADDING FIX (NO HALF-SHOWING) */
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* 3. KURAL FORMATTING (4 WORDS TOP / 3 WORDS BOTTOM) */
    .kural-display {
        text-align: center;
        font-family: 'serif';
        color: #1B2631;
        margin-top: -10px;
    }
    .kural-line1 { font-size: 1.3em; font-weight: bold; margin-bottom: 5px; }
    .kural-line2 { font-size: 1.1em; color: #5D6D7E; }

    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 6px solid #1B2631;
        text-align: center; max-width: 800px; margin: auto;
    }
    
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%); }
        50% { transform: scale(1.05); filter: brightness(120%); }
        100% { transform: scale(1); filter: brightness(100%); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO & KURAL ENGINE ---
def load_logo():
    search_list = ["logo.jpg", "tackyon logo", "tackyon logo.jpeg"]
    for f in search_list:
        if os.path.exists(f):
            with open(f, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

logo_b64 = load_logo()

# Correct 4-3 Word Format Logic
THIRUKURAL_HUB = [
    {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"},
    {"top": "அகர முதல எழுத்தெல்லாம் ஆதி", "bottom": "பகவன் முதற்றே உலகு"},
    {"top": "எப்பொருள் யார்யார்வாய்க் கேட்பினும் அப்பொருள்", "bottom": "மெய்ப்பொருள் காண்ப தறிவு"}
]

def render_logo(size="100px", animate=False):
    if logo_b64:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 20px; padding-top: 10px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 12px;">'
            f'</div>', 
            unsafe_allow_html=True
        )

# --- 3. THE BRANDED FLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = random.choice(THIRUKURAL_HUB)

# STAGE 1: FULLSCREEN PULSE
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    render_logo(size="320px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# DISPLAY KURAL IN THE BOX (STAGES 2, 3, 4)
if st.session_state.flow_stage != "animation":
    st.markdown(f"""
        <div class="kural-display">
            <div class="kural-line1">{st.session_state.daily_kural['top']}</div>
            <div class="kural-line2">{st.session_state.daily_kural['bottom']}</div>
        </div>
    """, unsafe_allow_html=True)

# STAGE 2: EXECUTIVE ONBOARDING
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
        url = st.text_input("YouTube Resource URL", placeholder="Paste Link (Shorts/Vlogs/Long-form)")
        col_l, col_s, col_f = st.columns(3)
        with col_l: st.selectbox("Language", ["Tamil", "English", "Hindi"])
        with col_s: st.selectbox("Style", ["Summary", "Points"])
        with col_f: st.selectbox("Font", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")