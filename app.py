import streamlit as st
import time
import base64
import os

# --- 1. TOTAL UI ARCHITECTURE (THE "BOX KILLER") ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* FORCE-HIDE THE TOP WHITE BOX AND ALL HEADERS */
    header, [data-testid="stHeader"], .stAppHeader {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* PULL CONTENT TO THE ABSOLUTE TOP TO COVER THE GAP */
    .block-container {
        padding-top: 0px !important;
        margin-top: -100px !important;
    }
    
    /* EXECUTIVE CARD DESIGN */
    .executive-card {
        background: white; padding: 50px; border-radius: 25px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.1); border-top: 8px solid #1B2631;
        text-align: center; max-width: 850px; margin: auto;
    }

    /* METALLIC LOGO PULSE ANIMATION */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
        50% { transform: scale(1.08); filter: brightness(130%) drop-shadow(0 0 30px rgba(0,102,204,0.6)); }
        100% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ULTIMATE LOGO SCANNER (CUMULATIVE FIX) ---
def load_logo_master():
    """
    Scans the folder for anything starting with 'logo' or 'tackyon' 
    to ensure the Metallic T always appears.
    """
    try:
        files = os.listdir(".")
        # Triple-check for the names seen in your screenshots
        for file in files:
            clean_name = file.lower().replace(" ", "")
            if ("logo" in clean_name or "tackyon" in clean_name) and file.lower().endswith(('.png', '.jpg', '.jpeg')):
                with open(file, "rb") as f:
                    return base64.b64encode(f.read()).decode()
    except:
        return None
    return None

logo_b64 = load_logo_master()

def show_t_logo(size="100px", animate=False):
    if logo_b64:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 25px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 15px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        # High-end text fallback if file is missing
        st.markdown(f'<div style="font-size: 35px; font-weight: bold; text-align: center; color: #1B2631;">TACKYON AI</div>', unsafe_allow_html=True)

# --- 3. THE BRANDED FLOW (CUMULATIVE) ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# STAGE 1: 2-SECOND METALLIC PULSE
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 35vh;"></div>', unsafe_allow_html=True)
    show_t_logo(size="350px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="100px")
    st.title("Executive Onboarding")
    st.markdown("<p style='color: #5D6D7E; font-size: 1.1em;'>Identify your credentials to initialize the Hub.</p>", unsafe_allow_html=True)
    
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

# STAGE 3: GATEWAY & HUB
elif st.session_state.flow_stage == "gateway":
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="80px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    st.markdown("""
        <div style="background: #F4F6F7; border-left: 8px solid #1B2631; padding: 30px; border-radius: 0 15px 15px 0; margin: 25px 0; text-align: left;">
            <h2 style="color: #1B2631;">கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.</h2>
            <hr>
            <p style="color: #5D6D7E; font-size: 1.1em; font-style: italic;">"Learn thoroughly, then live according to that learning."</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    show_t_logo(size="130px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
        c1, c2, c3 = st.columns(3)
        with c1: st.selectbox("Language", ["Tamil", "English", "Hindi"])
        with c2: st.selectbox("Style", ["Executive Summary", "Strategic Points"])
        with c3: st.selectbox("Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")