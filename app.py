import streamlit as st
import time
import base64
import os

# --- 1. TOTAL UI ARCHITECTURE (THE "BOX KILLER") ---
# We set wide mode and professional page config
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* FORCE-HIDE THE TOP WHITE BOX AND ALL STREAMLIT HEADERS */
    header, [data-testid="stHeader"], .stAppHeader {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* REMOVE TOP PADDING AND PULL CONTENT UP */
    .block-container {
        padding-top: 0px !important;
        margin-top: -80px !important;
    }
    
    /* EXECUTIVE CARD DESIGN */
    .executive-card {
        background: white; 
        padding: 50px; 
        border-radius: 25px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.1); 
        border-top: 8px solid #1B2631;
        text-align: center; 
        max-width: 900px; 
        margin: auto;
    }

    /* METALLIC LOGO PULSE ANIMATION */
    @keyframes t-pulse {
        0% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
        50% { transform: scale(1.1); filter: brightness(130%) drop-shadow(0 0 30px rgba(0,102,204,0.6)); }
        100% { transform: scale(1); filter: brightness(100%) drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
    }
    .pulse-layer { animation: t-pulse 2s infinite ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE CUMULATIVE LOGO ENGINE (SEARCHES ALL POSSIBILITIES) ---
def load_logo_master():
    """
    Specifically finds 'tackyon logo' as seen in your folder.
    It checks for every common extension so it never fails.
    """
    search_names = [
        "tackyon logo", "tackyon logo.jpg", "tackyon logo.jpeg", 
        "tackyon logo.png", "logo.jpg", "logo.jpeg"
    ]
    for name in search_names:
        if os.path.exists(name):
            try:
                with open(name, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except:
                continue
    return None

logo_b64 = load_logo_master()

def show_t_logo(size="100px", animate=False):
    """Displays the metallic logo with optional pulsing animation."""
    if logo_b64:
        div_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{div_class}" style="text-align: center; margin-bottom: 25px;">'
            f'<img src="data:image/jpeg;base64,{logo_b64}" style="width:{size}; border-radius: 20px;">'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        # Emergency fallback if the file is moved
        st.markdown(f'<div style="font-size: {size}; text-align: center;">🎯</div>', unsafe_allow_html=True)

# --- 3. THE BRANDED FLOW (CUMULATIVE BUILD) ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# STAGE 1: 2-SECOND METALLIC PULSE (The "Soul" of the Launch)
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 35vh;"></div>', unsafe_allow_html=True)
    show_t_logo(size="350px", animate=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING (Personalization Stage)
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="100px")
    st.title("Executive Onboarding")
    st.markdown("<p style='color: #5D6D7E; font-size: 1.2em;'>Credentials required to initialize the Intelligence Hub.</p>", unsafe_allow_html=True)
    
    # 3-Column Tabular Layout for Onboarding
    col1, col2, col3 = st.columns(3)
    with col1: 
        name = st.text_input("Full Legal Name", placeholder="e.g. Prapanchan V V")
    with col2: 
        gender = st.selectbox("Gender Identity", ["Male", "Female", "Executive"])
    with col3: 
        age = st.number_input("Age Group", 18, 99, 19)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
        else:
            st.error("Credential identification is mandatory.")
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: THE THIRUKURAL GATEWAY (Static Inspiration Stage)
elif st.session_state.flow_stage == "gateway":
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    show_t_logo(size="80px")
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    st.markdown("""
        <div style="background: #F4F6F7; border-left: 8px solid #1B2631; padding: 35px; border-radius: 0 20px 20px 0; margin: 30px 0; text-align: left;">
            <h2 style="color: #1B2631; font-family: 'serif';">கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.</h2>
            <hr style="border: 0.5px solid #D5D8DC;">
            <p style="color: #5D6D7E; font-size: 1.2em; font-style: italic;">"Learn thoroughly, then live according to that learning."</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: MAIN EXECUTIVE HUB (Final Layout Stage)
else:
    # Sidebar Identity & Branding
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    show_t_logo(size="150px")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<h3 style='text-align: center;'>Executive: {st.session_state.user['name']}</h3>", unsafe_allow_html=True)
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    
    # Primary Data Acquisition Container
    with st.expander("📥 Primary Data Acquisition", expanded=True):
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link (Shorts/Vlogs/Long-form)")
        
        # Professional Tabular Selection for Intelligence Settings
        col_l, col_s, col_f = st.columns(3)
        with col_l: 
            st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi", "Malayalam"])
        with col_s: 
            st.selectbox("Analysis Output", ["Executive Summary", "Strategic Key Points", "Viral Social Thread"])
        with col_f: 
            st.selectbox("Interface Typography", ["Inter", "Arima", "Roboto", "Montserrat"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")