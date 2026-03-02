import streamlit as st
import time
import random
import uuid
import json
import os
import requests

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-card {
        background-color: white; padding: 40px; border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.07); text-align: center;
        border: 1px solid #e1e4e8;
    }
    .kural-text { color: #1a1a1a; font-weight: 600; font-size: 1.4em; line-height: 1.6; margin-bottom: 15px; white-space: pre-wrap; }
    .kural-meaning { color: #586069; font-size: 1.0em; font-style: italic; border-top: 1px solid #eee; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTOMATED THIRUKKURAL DOWNLOADER ---
def get_all_1330_kurals():
    file_path = "thirukkural_full.json"
    # If the file isn't there, download it automatically from GitHub
    if not os.path.exists(file_path):
        try:
            # Using a reliable open-source JSON source for all 1330 Kurals
            url = "https://raw.githubusercontent.com/pinnamaneni/thirukkural-json/master/thirukkural.json"
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f)
            else:
                raise Exception("Download failed")
        except:
            # Emergency backup if internet is down
            return [{"line1": "அகர முதல எழுத்தெல்லாம்", "line2": "ஆதி பகவன் முதற்றே உலகு.", "translation": "A leads the alphabet; God leads the world."}]
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        # Handle different JSON structures (Kural is usually in a 'kural' or 'chapters' list)
        return data.get("kural", data)

# --- 3. SESSION MANAGEMENT ---
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "tackyon_id" not in st.session_state:
    st.session_state.tackyon_id = None

# --- 4. THE EXECUTION FLOW ---

# STEP 1: First-Time Onboarding (Personalization)
if not st.session_state.user_data:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("Tackyon AI Onboarding 🚀")
    name = st.text_input("Executive Name")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with col2:
        age = st.number_input("Age", 10, 100, 25)
    
    if st.button("Initialize T-Core ID"):
        if name:
            st.session_state.user_data = {"name": name, "gender": gender, "age": age}
            st.session_state.tackyon_id = str(uuid.uuid4())[:8].upper()
            st.rerun()
        else:
            st.warning("Identification required.")
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2 & 3: Executive Splash & Full Thirukkural Gateway
elif "splash_done" not in st.session_state:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.header("Tackyon Executive Gateway")
    
    # Truly random pick from 1330
    kurals = get_all_1330_kurals()
    choice = random.choice(kurals)
    
    # Display logic handles lines for Tamil Kurals
    line1 = choice.get("line1", "")
    line2 = choice.get("line2", "")
    meaning = choice.get("translation", choice.get("meaning", "Cultural inspiration loading..."))
    
    st.markdown(f'<p class="kural-text">{line1}\n{line2}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="kural-meaning">{meaning}</p>', unsafe_allow_html=True)
    
    st.caption("Syncing Secure Device ID...")
    time.sleep(4) 
    st.session_state.splash_done = True
    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 4: MAIN DASHBOARD
else:
    st.sidebar.title("🚀 Tackyon AI")
    st.sidebar.markdown(f"**Executive:** {st.session_state.user_data['name']}")
    st.sidebar.markdown(f"**ID:** `TACK-{st.session_state.tackyon_id}`")
    
    st.title("Executive Intelligence Hub")
    st.write(f"Welcome, {st.session_state.user_data['name']}. Your workspace is secure.")
    
    # Placeholder for YouTube Logic
    st.text_input("Paste YouTube Link (Shorts/Vlogs/Long-form)")
    st.button("Execute Deep Analysis")

    if st.sidebar.button("System Reset (Test Mode)"):
        st.session_state.clear()
        st.rerun()