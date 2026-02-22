import streamlit as st
from PIL import Image
import os
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai

# --- 1. MOBILE CONFIGURATION ---
st.set_page_config(
    page_title="Tackyon AI",
    page_icon="logo.png",
    layout="centered"
)

# --- 2. API SETUP ---
# This uses your existing secret key from Streamlit Cloud
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 3. LOGO & BRANDING ---
if os.path.exists('logo.png'):
    logo = Image.open('logo.png')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, use_container_width=True)
else:
    st.title("Tackyon Summariser AI 🚀")

st.subheader("AI YouTube Summariser")
st.markdown("---")

# --- 4. USER INPUT ---
url = st.text_input("Paste YouTube Link here:", placeholder="https://www.youtube.com/watch?v=...")
lang = st.selectbox("Select summary language:", ["English", "Tamil", "Hindi", "Malayalam"])

# --- 5. THE BRAIN (GEMINI 3 FIX) ---
if st.button("Summarize Video"):
    if url:
        with st.spinner("Tackyon is analyzing the video..."):
            try:
                # Get transcript using your bulletproof engine
                text = yt_dlp_transcript(url)
                
                if text:
                    # UPDATED: Using Gemini 3 Flash to fix the 404 error
                    model = genai.GenerativeModel('gemini-3-flash') 
                    
                    prompt = f"Summarize this YouTube video transcript in {lang} with key highlights: {text}"
                    response = model.generate_content(prompt)
                    
                    st.success("Summary Ready!")
                    st.write(response.text)
                else:
                    st.error("Could not find a transcript for this video.")
            
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please paste a link first!")