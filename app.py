import streamlit as st
import time
import base64
import os

# --- 1. THEME & TOTAL HEADER HIDER ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

# This CSS strictly removes the white box and centers the pulse animation
st.markdown("""
    <style>
    /* Forcefully hide the empty white box and Streamlit header */
    [data-testid="stHeader"], header { visibility: hidden; height: 0px !important; }
    .block-container { padding-top: 0rem !important; }
    
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); border-top: 5px solid #1B2631;
        text-align: center; max-width: 800px; margin: auto;
    }

    /* Metallic T-Pulse Animation */
    @keyframes t-pulse {
        0% { transform: scale(1); opacity: 0.85; filter: drop-shadow(0 0 5px rgba(255,255,255,0.2)); }
        50% { transform: scale(1.1); opacity: 1; filter: drop-shadow(0 0 20px rgba(0,100,255,0.4)); }
        100% { transform: scale(1); opacity: 0.85; filter: drop-shadow(0 0 5px rgba(255,255,255,0.2)); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGO LOADER ---
def get_executive_logo(file_name):
    """Automatically finds and encodes the metallic logo."""
    # Check for common extensions just in case
    possible_names = [file_name, file_name + ".jpg", file_name + ".jpeg", "tackyon logo.jpg"]
    for name in possible_names:
        if os.path.exists(name):
            with open(name, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

# From your desktop screenshot: 'tackyon logo'
img_b64 = get_executive_logo("tackyon logo")

def show_t_logo(size="100px", animate=False):
    if img_b64:
        div_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{div_class}" style="text-align: center; margin-top: 20px;">'
            f'<img src="data:image/jpeg;base64,{img_b64}" style="width:{size}; border-radius: 15px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Logo File Sync Error: Ensure 'tackyon logo.jpg' is in the folder.")

# --- 3. THE BRANDED FLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# STAGE 1: FULLSCREEN PULSE (2 SECONDS)
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    show_t_logo(size="350px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING (Tabular & Furnished)
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="90px")
    st.title("Executive Onboarding")
    st.markdown("<p style='color: #5D6D7E;'>Secure your profile to initialize the Hub.</p>", unsafe_allow_html=True)
    
    # 3-Column Tabular Furnishing
    c1, c2, c3 = st.columns(3)
    with c1: name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with c2: gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with c3: age = st.number_input("Age", 18, 99, 19)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: THIRUKURAL GATEWAY
elif st.session_state.flow_stage == "gateway":
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="70px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    st.markdown("""
        <div style="background: #F4F6F7; border-left: 5px solid #1B2631; padding: 25px; border-radius: 0 15px 15px 0; margin: 20px 0;">
            <h2 style="color: #1B2631;">கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.</h2>
            <hr style="border: 0.5px solid #D5D8DC;">
            <p style="color: #5D6D7E; font-style: italic;">"Learn thoroughly, then live according to that learning."</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB (Professional Furnishing)
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    show_t_logo(size="130px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link (Shorts/Vlogs/Long-form)")
        
        # Professional Columns
        col_l, col_s, col_f = st.columns(3)
        with col_l: st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi"])
        with col_s: st.selectbox("Analysis Output", ["Executive Summary", "Key Strategic Points"])
        with col_f: st.selectbox("Interface Typography", ["Inter", "Arima", "Roboto"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")