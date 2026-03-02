import streamlit as st
import random
import uuid
import json
import os
import requests

# --- 1. PREMIUM CONFIGURATION ---
st.set_page_config(page_title="Tackyon AI | Executive Hub", page_icon="🎯", layout="wide")

# High-End CSS for Professional Interface
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #FDFDFD; }
    
    .main-card {
        background: white;
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
        max-width: 800px;
        margin: auto;
    }
    .kural-box {
        background-color: #F8F9FB;
        border-left: 5px solid #2C3E50;
        padding: 30px;
        margin: 25px 0;
        border-radius: 0 15px 15px 0;
    }
    .kural-tamil { font-size: 1.5em; font-weight: 600; color: #1A1A1A; line-height: 1.6; }
    .kural-eng { font-size: 1.1em; color: #5D6D7E; font-style: italic; margin-top: 15px; }
    .stButton>button {
        background-color: #1A1A1A; color: white; border-radius: 8px;
        padding: 10px 25px; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #333; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ASSET & DATA MANAGEMENT ---
LOGO_URL = "https://raw.githubusercontent.com/Prapanchan-vv/Tackyon-Assets/main/T-Core_Logo.png" # Placeholder for your uploaded T-Logo

def get_thirukural():
    file_path = "thirukkural_full.json"
    if not os.path.exists(file_path):
        url = "https://raw.githubusercontent.com/pinnamaneni/thirukkural-json/master/thirukkural.json"
        r = requests.get(url)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(r.json(), f)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return random.choice(data.get("kural", data))

# --- 3. SESSION IDENTITY ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "gateway_passed" not in st.session_state:
    st.session_state.gateway_passed = False

# --- 4. EXECUTIVE WORKFLOW ---

# STAGE 1: EXECUTIVE CREDENTIALING (Onboarding)
if not st.session_state.authenticated:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.image(LOGO_URL, width=120)
    st.title("Executive Credentialing")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Legal Name", placeholder="e.g. Prapanchan V V")
        gender = st.selectbox("Gender Identity", ["Male", "Female", "Prefer not to say"])
    with col2:
        age = st.number_input("Age Group", 18, 99, 19)
    
    if st.button("Initialize T-Core Identity"):
        if name:
            st.session_state.user = {"name": name, "gender": gender, "age": age}
            st.session_state.id = str(uuid.uuid4())[:8].upper()
            st.session_state.authenticated = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 2: THE THIRUKURAL GATEWAY (Static until read)
elif not st.session_state.gateway_passed:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.image(LOGO_URL, width=80)
    st.subheader("Intelligence Gateway | Daily Reflection")
    
    kural = get_thirukural()
    st.markdown(f"""
        <div class="kural-box">
            <div class="kural-tamil">{kural['line1']}<br>{kural['line2']}</div>
            <div class="kural-eng">"{kural['translation']}"</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Proceed to Intelligence Hub"):
        st.session_state.gateway_passed = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STAGE 3: EXECUTIVE INTELLIGENCE HUB
else:
    # Sidebar: Managed Identity
    st.sidebar.image(LOGO_URL, width=100)
    st.sidebar.markdown(f"**Executive:** {st.session_state.user['name']}")
    st.sidebar.markdown(f"**T-Core ID:** `TACK-{st.session_state.id}`")
    st.sidebar.divider()
    
    st.title("Executive Intelligence Hub")
    st.markdown(f"Welcome back, **{st.session_state.user['name']}**. Your secure environment is active.")
    
    # Input Engine
    with st.container():
        st.markdown("### 📥 Video Acquisition")
        url = st.text_input("YouTube Resource Locator", placeholder="Paste URL (Vlogs, Shorts, or Briefs)")
        
        # Professional Tabular UI
        col_a, col_b = st.columns(2)
        with col_a:
            lang = st.selectbox("Target Intelligence Language", ["English", "Tamil", "Hindi", "Malayalam"])
        with col_b:
            style = st.selectbox("Intelligence Output Style", ["Executive Summary", "Strategic Points", "Viral Social Thread"])
        
        if st.button("Execute Deep Analysis", use_container_width=True):
            st.info("Initiating Tackyon Decryption Engine...")