import streamlit as st
import time
import base64
import os
import random

# --- 1. EXECUTIVE UI ARCHITECTURE ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* Forcefully hide the empty white box at the top */
    header, [data-testid="stHeader"] { visibility: hidden; height: 0px !important; }
    .block-container { padding-top: 0px !important; margin-top: -30px !important; }

    /* Executive Card & Kural Styling */
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 6px solid #1B2631;
        text-align: center; max-width: 850px; margin: auto;
    }
    .kural-container {
        background: #FDFEFE; border: 1.5px solid #D4AC0D; /* Gold Accent */
        padding: 20px; border-radius: 15px; margin: 20px 0;
    }
    .kural-line1 { font-size: 1.4em; font-weight: bold; color: #1B2631; margin-bottom: 8px; }
    .kural-line2 { font-size: 1.2em; color: #5D6D7E; }

    /* Metallic Pulse Animation */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%); }
        50% { transform: scale(1.05); filter: brightness(120%); }
        100% { transform: scale(1); filter: brightness(100%); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE CUMULATIVE ENGINES ---
def find_logo_robustly():
    """Scans for logo.jpg or tackyon logo in the folder."""
    search_names = ["logo.jpg", "tackyon logo", "logo.jpeg", "tackyon logo.jpeg"]
    for f in search_names:
        if os.path.exists(f):
            with open(f, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

logo_data = find_logo_robustly()

# Strict 4-3 Grammar Format
THIRUKURAL_DATA = [
    {"line1": "கற்க கசடறக் கற்பவை கற்றபின்", "line2": "நிற்க அதற்குத் தக"},
    {"line1": "அகர முதல எழுத்தெல்லாம் ஆதி", "line2": "பகவன் முதற்றே உலகு"},
    {"line1": "அன்பிலார் எல்லாம் தமக்குரியர் அன்புடையார்", "line2": "என்பும் உரியர் பிறர்க்கு"}
]

def show_logo(size="100px", animate=False):
    if logo_data:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 20px;">'
            f'<img src="data:image/jpeg;base64,{logo_data}" style="width:{size}; border-radius: 15px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(f'<div style="text-align: center; font-size: 30px; font-weight: bold;">T-CORE</div>', unsafe_allow_html=True)

# --- 3. BRANDED FLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.kural = random.choice(THIRUKURAL_DATA)

# STAGE 1: 2-SECOND FULLSCREEN PULSE
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    show_logo(size="350px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_logo(size="100px")
    st.title("Executive Onboarding")
    
    # 3-Column Furnished Layout
    c1, c2, c3 = st.columns(3)
    with c1: name = st.text_input("Full Legal Name", placeholder="e.g. Prapanchan V V")
    with c2: gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with c3: age = st.number_input("Age", 18, 99, 19)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: THIRUKURAL GATEWAY (Fixed 4-3 Format)
elif st.session_state.flow_stage == "gateway":
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_logo(size="80px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    # Displaying Kural in the Gold-Bordered Card
    st.markdown(f"""
        <div class="kural-container">
            <div class="kural-line1">{st.session_state.kural['line1']}</div>
            <div class="kural-line2">{st.session_state.kural['line2']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    show_logo(size="130px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
        col_l, col_s, col_f = st.columns(3)
        with col_l: st.selectbox("Language", ["Tamil", "English", "Hindi"])
        with col_s: st.selectbox("Style", ["Summary", "Points"])
        with col_f: st.selectbox("Font", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")