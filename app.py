import streamlit as st
import time
import random
import uuid
import base64
from PIL import Image

# --- 1. LOGO EMBEDDING UTILITY ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_logo(file_path, width="100px"):
    try:
        bin_str = get_base64_of_bin_file(file_path)
        return f'<img src="data:image/png;base64,{bin_str}" style="width:{width};">'
    except:
        return "🎯" # Fallback if file not found

# --- 2. THEME & EXECUTIVE STYLING ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* Remove default Streamlit whitespace at the top */
    .block-container { padding-top: 1rem; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-top: 5px solid #1B2631;
        text-align: center; max-width: 900px; margin: auto;
    }
    
    /* Animation Pulse */
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    .t-logo-anim { animation: pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

LOGO_FILE = "17975.png" # YOUR METALLIC LOGO

# --- 4. THE EXECUTIVE FLOW ---

# STAGE 1: 2-SECOND FULLSCREEN ANIMATION
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 80vh;">', unsafe_allow_html=True)
    # Pulsing Metallic T-Logo
    logo_html = set_logo(LOGO_FILE, width="300px")
    st.markdown(f'<div class="t-logo-anim">{logo_html}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    # Smaller Logo for Header
    st.markdown(set_logo(LOGO_FILE, width="80px"), unsafe_allow_html=True)
    st.title("Executive Onboarding")
    st.info("Please provide your credentials to proceed to the Intelligence Hub.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Non-Binary"])
    with col3:
        age = st.number_input("Age", 18, 99, 19)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: THIRUKURAL GATEWAY
elif st.session_state.flow_stage == "gateway":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown(set_logo(LOGO_FILE, width="60px"), unsafe_allow_html=True)
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    # Built-in Kural to avoid JSON error
    st.markdown("""
        <div style="background: #FDFEFE; border: 2px solid #D5D8DC; padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h2 style="color: #1B2631;">கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.</h2>
            <hr>
            <p style="color: #5D6D7E; font-style: italic;">Learn thoroughly, then live according to that learning.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB
else:
    st.sidebar.markdown(f"<div style='text-align: center;'>{set_logo(LOGO_FILE, width='120px')}</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    st.markdown("### 📥 Primary Data Acquisition")
    url = st.text_input("YouTube Resource URL", placeholder="Paste Link (Shorts/Vlogs/Long-form)")
    
    col_l, col_s, col_f = st.columns(3)
    with col_l:
        st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi", "Malayalam"])
    with col_s:
        st.selectbox("Analysis Output", ["Executive Summary", "Strategic Points", "Twitter Thread"])
    with col_f:
        st.selectbox("Interface Typography", ["Inter", "Roboto", "Arima"])

    if st.button("Execute Deep Analysis", use_container_width=True):
        st.info("Initiating Tackyon Decryption Engine...")