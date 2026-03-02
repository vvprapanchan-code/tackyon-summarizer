import streamlit as st
import time
import base64
import os

# --- 1. THE "BOX KILLER" & EXECUTIVE THEME ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* 1. COMPLETELY HIDE THE TOP WHITE BOX & MENU */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden !important; height: 0px !important;}
    footer {visibility: hidden;}
    .block-container {padding-top: 0px !important; margin-top: -50px !important;}
    [data-testid="stHeader"] {display: none !important;}
    
    /* 2. EXECUTIVE CARD DESIGN */
    .executive-card {
        background: white; padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-top: 6px solid #1B2631;
        text-align: center; max-width: 800px; margin: auto;
    }

    /* 3. METALLIC LOGO PULSE ANIMATION */
    @keyframes metallic-pulse {
        0% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
        50% { transform: scale(1.08); filter: brightness(120%) drop-shadow(0 0 20px rgba(0,102,204,0.4)); }
        100% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
    }
    .pulse-logo { animation: metallic-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE LOGO FINDER (RELIABLE) ---
def load_logo_robustly():
    # We look for the file you renamed, or common variations
    filenames = ["logo.jpg", "logo.jpeg", "tackyon logo.jpg", "tackyon logo.jpeg"]
    for f in filenames:
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
        st.error("❌ LOGO NOT FOUND: Please rename your file to 'logo.jpg' and put it in this folder.")

# --- 3. THE EXECUTIVE FLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# STAGE 1: THE 2-SECOND FULLSCREEN PULSE
if st.session_state.flow_stage == "animation":
    st.write(" ") # Spacer
    st.markdown('<div style="height: 25vh;"></div>', unsafe_allow_html=True)
    display_t_logo(size="300px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    display_t_logo(size="80px")
    st.title("Executive Onboarding")
    st.markdown("<p style='color: #5D6D7E;'>Identify yourself to access the Intelligence Hub.</p>", unsafe_allow_html=True)
    
    # Tabular Layout
    col1, col2, col3 = st.columns(3)
    with col1: name = st.text_input("Full Name", placeholder="e.g. Prapanchan V V")
    with col2: gender = st.selectbox("Gender", ["Male", "Female", "Executive"])
    with col3: age = st.number_input("Age", 18, 99, 19)
    
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
    display_t_logo(size="70px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    st.markdown("""
        <div style="background: #F4F6F7; border-left: 6px solid #1B2631; padding: 30px; border-radius: 0 15px 15px 0; margin: 25px 0; text-align: left;">
            <h2 style="color: #1B2631; font-family: 'serif';">கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.</h2>
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
    display_t_logo(size="120px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    
    with st.container():
        st.markdown("### 📥 Primary Data Acquisition")
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link")
        
        c1, c2, c3 = st.columns(3)
        with c1: st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi"])
        with c2: st.selectbox("Analysis Output", ["Summary", "Strategic Points"])
        with c3: st.selectbox("Interface Typography", ["Inter", "Arima"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")