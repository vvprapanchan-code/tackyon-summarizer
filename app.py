import streamlit as st
from PIL import Image
import os
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai

# --- 1. MANDATORY SETUP (FIXES MOBILE ICON) ---
st.set_page_config(
    page_title="Tackyon AI",
    page_icon="logo.png",
    layout="centered"
)

# --- 2. API CONFIGURATION ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 3. BRANDING & LOGO ---
if os.path.exists('logo.png'):
    logo = Image.open('logo.png')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, use_container_width=True)
else:
    st.title("Tackyon 🚀")

st.subheader("AI YouTube Summariser")
st.markdown("---")

# --- 4. USER INPUT ---
url = st.text_input("Paste YouTube Link:")
lang = st.selectbox("Language:", ["English", "Tamil", "Hindi", "Malayalam"])

# --- 5. THE ENGINE (SATURDAY'S WORKING VERSION) ---
if st.button("Summarize"):
    if url:
        with st.spinner("Tackyon is working..."):
            try:
                # Using your bulletproof engine
                text = yt_dlp_transcript(url)
                
                if not text:
                    st.error("No transcript found for this video.")
                else:
                    # FIX: Using 'gemini-1.5-flash-latest' to bypass the 404 error
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    
                    response = model.generate_content(f"Summarize in {lang}: {text}")
                    
                    st.success("Victory! Summary below:")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please paste a link first!")