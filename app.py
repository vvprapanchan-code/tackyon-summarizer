import streamlit as st
import streamlit as st
from PIL import Image  # Add this line to handle images

# --- LOGO SETUP ---
# This opens your logo file
logo = Image.open('logo.png')

# This displays the logo at the top, centered
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo, width=200)
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai

# --- 1. SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# --- 0. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Tackyon AI",
    page_icon="logo.png",  # This changes the browser tab and shortcut icon!
    layout="centered"
)
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 2. USER INPUT ---
url = st.text_input("Paste YouTube Link:")
lang = st.selectbox("Language:", ["English", "Tamil", "Hindi"])

if st.button("Summarize"):
    if url:
        with st.spinner("Tackyon is working..."):
            try:
                # Engine from Step 15 that bypasses blocks
                text = yt_dlp_transcript(url)
                
                if not text:
                    st.error("No transcript found for this video.")
                else:
                    # Using the exact model name from yesterday's success
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    response = model.generate_content(f"Summarize in {lang}: {text}")
                    st.success("Victory! Summary below:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")