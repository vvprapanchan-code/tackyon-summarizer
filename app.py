import streamlit as st
import time
import base64
import os

# --- 1. THE "BOX KILLER" & EXECUTIVE THEME ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* 1. FORCE-HIDE THE TOP WHITE BOX & ALL STREAMLIT HEADERS */
    header, [data-testid="stHeader"], .stAppHeader {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Pull content to the very top to cover any remaining gap */
    .block-container {
        padding-top: 0px !important;
        margin-top: -80px !important;
    }
    
    /* 2. EXECUTIVE CARD DESIGN */
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 6px solid #1B2631;
        text-align: center; max-width: 800px; margin: auto;
    }

    /* 3. METALLIC LOGO PULSE ANIMATION */
    @keyframes metallic-pulse {
        0% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
        50% { transform: scale(1.08); filter: brightness(125%) drop-shadow(0 0 20px rgba(0,102,204,0.5)); }
        100% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
    }
    .pulse-logo { animation: metallic-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ULTIMATE LOGO FINDER (CUMULATIVE FIX) ---
def load_executive_logo():
    # Searching specifically for your file name from the photo
    search_list = ["tackyon logo", "tackyon logo.jpg", "tackyon logo.jpeg", "logo.jpg"]
    for f in search_list:
        if os.path.exists(f):
            with open(f, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

logo_b64 = load_executive_logo()

def show_t_logo(size="100px", animate=False):
    if logo_b64:
        anim_class = "pulse-logo" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 20px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 15px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        # Fallback to the rocket if the file is truly missing
        st.markdown(f'<div style="font-size: {size}; text-align: center;">🚀</div>', unsafe_allow_html=True)

# --- 3. THE BRANDED FLOW (CUMULATIVE) ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# STAGE 1: FULLSCREEN PULSE (2 SECONDS)
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 35vh;"></div>', unsafe_allow_html=True)
    show_t_logo(size="320px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING (CUMULATIVE)
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="90px")
    st.title("Executive Onboarding")
    st.markdown("<p style='color: #5D6D7E; font-size: 1.1em;'>Please provide your credentials to proceed.</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: name = st.text_input("Full Legal Name", placeholder="e.g. Prapanchan V V")
    with c2: gender = st.selectbox("Gender Identity", ["Male", "Female", "Executive"])
    with c3: age = st.number_input("Age Group", 18, 99, 19)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: THE GATEWAY (CUMULATIVE)
elif st.session_state.flow_stage == "gateway":
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="70px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    st.markdown("""
        <div style="background: #F4F6F7; border-left: 6px solid #1B2631; padding: 25px; border-radius: 0 15px 15px 0; margin: 20px 0; text-align: left;">
            <h2 style="color: #1B2631; font-family: 'serif';">கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.</h2>
            <hr>
            <p style="color: #5D6D7E; font-size: 1.1em; font-style: italic;">"Learn thoroughly, then live according to that learning."</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN HUB (CUMULATIVE)
else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    show_t_logo(size="130px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
        col_l, col_s, col_f = st.columns(3)
        with col_l: st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi"])
        with col_s: st.selectbox("Analysis Output", ["Summary", "Strategic Points"])
        with col_f: st.selectbox("Interface Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")