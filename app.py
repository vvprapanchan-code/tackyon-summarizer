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
    
    /* Remove top padding and empty boxes completely */
    .block-container {
        padding-top: 0px !important;
        margin-top: -50px !important;
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
        50% { transform: scale(1.1); filter: brightness(125%) drop-shadow(0 0 25px rgba(0,102,204,0.5)); }
        100% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
    }
    .pulse-logo { animation: metallic-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ULTIMATE LOGO FINDER (SEARCHES EVERY POSSIBILITY) ---
def load_logo_robustly():
    # This list covers every possible way your file might be named in the folder
    search_names = [
        "logo.jpg", "logo.jpeg", "logo.jpg.jpeg", "logo.jpeg.jpg",
        "tackyon logo.jpg", "tackyon logo.jpeg", "tackyon logo"
    ]
    for f in search_names:
        if os.path.exists(f):
            with open(f, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    return None

logo_b64 = load_logo_robustly()

def display_t_logo(size="100px", animate=False):
    if logo_b64:
        anim_class = "pulse-logo" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 20px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 12px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        # If no file is found, show a professional placeholder so the app stays clean
        st.markdown(f'<div style="font-size: {size}; text-align: center;">🎯</div>', unsafe_allow_html=True)
        st.error("⚠️ T-Core Logo Not Detected. Using default system icon.")

# --- 3. THE EXECUTIVE FLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# STAGE 1: THE 2-SECOND FULLSCREEN PULSE
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    display_t_logo(size="320px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE CREDENTIALING (Furnished Onboarding)
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    display_t_logo(size="90px")
    st.title("Executive Onboarding")
    st.markdown("<p style='color: #5D6D7E; font-size: 1.1em;'>Provide your credentials to initialize the Intelligence Hub.</p>", unsafe_allow_html=True)
    
    # 3-Column Furnished Layout
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

# STAGE 4: THE HUB (READY FOR STEP 5)
elif st.session_state.flow_stage == "hub":
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    display_t_logo(size="130px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link (Shorts/Vlogs/Long-form)")
        col_l, col_s, col_f = st.columns(3)
        with col_l: st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi"])
        with col_s: st.selectbox("Analysis Output", ["Summary", "Points"])
        with col_f: st.selectbox("Interface Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")