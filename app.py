import streamlit as st
import time
import base64
import os

# --- 1. THEME & HEADER CLEANUP ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

# This CSS removes the empty white box at the top and centers everything
st.markdown("""
    <style>
    /* Remove default Streamlit header and padding */
    [data-testid="stHeader"] { visibility: hidden; height: 0%; }
    .block-container { padding-top: 0rem; padding-bottom: 0rem; }
    
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-top: 5px solid #1B2631;
        text-align: center; max-width: 800px; margin: auto;
    }

    /* Professional Pulse Animation */
    @keyframes pulse-tcore {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    .logo-container { animation: pulse-tcore 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO HANDLER (Base64 for Stability) ---
def get_image_base64(file_name):
    """Encodes the image so it works even on the web."""
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Use the exact name from your desktop screenshot
LOGO_FILE = "tackyon logo.jpg" 
img_b64 = get_image_base64(LOGO_FILE)

def display_logo(width="100px", anim=False):
    if img_b64:
        class_name = "logo-container" if anim else ""
        st.markdown(
            f'<div class="{class_name}" style="text-align: center;">'
            f'<img src="data:image/jpeg;base64,{img_b64}" style="width:{width}; border-radius: 10px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.error(f"Missing File: Please rename your logo to '{LOGO_FILE}' in the folder.")

# --- 3. EXECUTIVE FLOW LOGIC ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# STAGE 1: 2-SECOND METALLIC ANIMATION
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 20vh;"></div>', unsafe_allow_html=True) # Professional spacing
    display_logo(width="300px", anim=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE CREDENTIALING (Tabular UI)
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 5vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    display_logo(width="80px")
    st.title("Executive Onboarding")
    st.markdown("Please provide your credentials to proceed.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
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
    st.markdown('<div style="height: 5vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    display_logo(width="60px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    st.markdown("""
        <div style="background: #FDFEFE; border: 2px solid #D5D8DC; padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h2 style="color: #1B2631; font-family: 'serif';">கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.</h2>
            <hr>
            <p style="color: #5D6D7E; font-style: italic;">"Learn thoroughly, then live according to that learning."</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    display_logo(width="100px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    
    # Professional Tabular Acquisition
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
        c1, c2, c3 = st.columns(3)
        with c1: st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi"])
        with c2: st.selectbox("Analysis Output", ["Executive Summary", "Points"])
        with c3: st.selectbox("Interface Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")