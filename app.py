import streamlit as st
import time
import base64
import os

# --- 1. TOTAL UI REFINEMENT (THE "BOX KILLER") ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* Forcefully hide the top white box and Streamlit header */
    header, [data-testid="stHeader"], .stAppHeader {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Pull content to the very top to cover the gap */
    .block-container {
        padding-top: 0px !important;
        margin-top: -70px !important;
    }
    
    /* Executive Card Styling */
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 6px solid #1B2631;
        text-align: center; max-width: 800px; margin: auto;
    }

    /* Metallic T-Pulse Animation */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
        50% { transform: scale(1.08); filter: brightness(120%) drop-shadow(0 0 25px rgba(0,102,204,0.5)); }
        100% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE CUMULATIVE LOGO LOADER (TRIPLE-CHECK) ---
def load_logo_final():
    # Looking for 'tackyon logo' as seen in your folder
    names_to_check = ["tackyon logo", "tackyon logo.jpg", "tackyon logo.jpeg", "logo.jpg"]
    for name in names_to_check:
        if os.path.exists(name):
            try:
                with open(name, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except:
                continue
    return None

logo_b64 = load_logo_final()

def show_t_logo(size="100px", animate=False):
    if logo_b64:
        div_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{div_class}" style="text-align: center; margin-bottom: 20px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 15px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        # Professional fallback so the app stays clean if the file is moved
        st.markdown(f'<div style="font-size: {size}; text-align: center;">🎯</div>', unsafe_allow_html=True)

# --- 3. THE BRANDED FLOW (CUMULATIVE) ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# STAGE 1: 2-SECOND FULLSCREEN PULSE
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    show_t_logo(size="320px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING (CUMULATIVE)
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 12vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="90px")
    st.title("Executive Onboarding")
    st.markdown("<p style='color: #5D6D7E; font-size: 1.1em;'>Credentialing required to initialize the Hub.</p>", unsafe_allow_html=True)
    
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

# STAGE 3: GATEWAY & HUB (CUMULATIVE)
else:
    # Sidebar Identity
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    show_t_logo(size="130px")
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
            st.info("Initiating Tackyon Decryption Engine...")