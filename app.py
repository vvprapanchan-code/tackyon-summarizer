import streamlit as st
import time
import random
import uuid

# --- 1. THEME & COLOR ARCHITECTURE ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    /* Professional Mixed Color Palette */
    :root {
        --primary-navy: #1B2631;
        --action-red: #E74C3C;
        --slate-gray: #5D6D7E;
        --gold-accent: #D4AC0D;
    }
    
    .main { background-color: #F4F7F9; }
    
    /* Executive Card Styling */
    .executive-card {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-top: 5px solid var(--primary-navy);
        text-align: center;
        max-width: 900px;
        margin: auto;
    }
    
    .instruction-text { color: var(--slate-gray); font-weight: 500; font-size: 1.1em; }
    
    /* Animation Keyframes */
    @keyframes pulse-logo {
        0% { transform: scale(0.9); opacity: 0.7; }
        50% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.7; }
    }
    .splash-logo { 
        width: 150px; 
        animation: pulse-logo 2s infinite ease-in-out; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BUILT-IN INTELLIGENCE (No Downloads Needed) ---
THIRUKURAL_DB = [
    {"k": "அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு.", "m": "A leads the alphabet; the Ancient Lord leads the world."},
    {"k": "கற்க கசடறக் கற்பவை கற்றபின்\nநிற்க அதற்குத் தக.", "m": "Learn thoroughly, then live according to that learning."},
    {"k": "அன்பிலார் எல்லாம் தமக்குரியர் அன்புடையார்\nஎன்பும் உரியர் பிறர்க்கு.", "m": "The loveless claim all; the loving yield even their bones."}
    # This list will be expanded to 1330 internally
]

# --- 3. STATE MANAGEMENT ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"

# --- 4. THE FLOW ---

# STAGE 1: 2-SECOND METALLIC ANIMATION
if st.session_state.flow_stage == "animation":
    st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 80vh;">', unsafe_allow_html=True)
    # Using your metallic logo image
    st.image("https://raw.githubusercontent.com/Prapanchan-vv/Tackyon-Assets/main/T-Core_Logo.png", width=250)
    st.markdown('</div>', unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.flow_stage = "onboarding"
    st.rerun()

# STAGE 2: EXECUTIVE ONBOARDING
elif st.session_state.flow_stage == "onboarding":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Prapanchan-vv/Tackyon-Assets/main/T-Core_Logo.png", width=80)
    st.title("Executive Onboarding")
    st.markdown('<p class="instruction-text">Please provide your credentials to access the hub.</p>', unsafe_allow_html=True)
    
    # Colorful Tabular Columns
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Full Name", placeholder="Enter Name")
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Non-Binary"])
    with col3:
        age = st.number_input("Age", 18, 99, 21)
    
    if st.button("Begin Your Journey", use_container_width=True):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.flow_stage = "gateway"
            st.rerun()
        else:
            st.error("Name is required to secure your session.")
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: THIRUKURAL GATEWAY (Static until read)
elif st.session_state.flow_stage == "gateway":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Prapanchan-vv/Tackyon-Assets/main/T-Core_Logo.png", width=60)
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    kural = random.choice(THIRUKURAL_DB)
    st.markdown(f"""
        <div style="background: #FDFEFE; border: 2px solid #D5D8DC; padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h2 style="color: #1B2631; font-family: 'Tamil';">{kural['k']}</h2>
            <hr>
            <p style="color: #5D6D7E; font-style: italic;">{kural['m']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Intelligence Hub", use_container_width=True):
        st.session_state.flow_stage = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 4: THE HUB (UI Ready for AI)
else:
    st.sidebar.image("https://raw.githubusercontent.com/Prapanchan-vv/Tackyon-Assets/main/T-Core_Logo.png", width=120)
    st.sidebar.markdown(f"### Welcome, Executive {st.session_state.user['name']}")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub 🚀")
    
    with st.container():
        st.markdown("### 📥 Primary Data Acquisition")
        url = st.text_input("Resource URL", placeholder="Paste YouTube Link (Shorts/Vlogs/Long-form)")
        
        # Professional Tabular Selection
        col_l, col_s, col_f = st.columns(3)
        with col_l:
            lang = st.selectbox("Intelligence Language", ["Tamil", "English", "Hindi", "Malayalam"])
        with col_s:
            style = st.selectbox("Analysis Output", ["Executive Summary", "Strategic Points", "Twitter Thread"])
        with col_f:
            font = st.selectbox("Interface Typography", ["Inter", "Roboto", "Montserrat", "Open Sans", "Arima"])

        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("System engaging... Initializing Tackyon Brain.")