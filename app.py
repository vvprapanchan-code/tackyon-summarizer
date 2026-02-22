import streamlit as st
from PIL import Image
import os
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai

# --- 0. MANDATORY FIRST STEP (FOR MOBILE ICON) ---
# This MUST be the very first Streamlit command to fix the shortcut logo
st.set_page_config(
    page_title="Tackyon AI",
    page_icon="logo.png",
    layout="centered"
)

# --- 1. SECURE API SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 2. LOGO DISPLAY ---
if os.path.exists('logo.png'):
    logo = Image.open('logo.png')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, width=200)
else:
    # Fallback if logo file is missing from GitHub
    st.title("Tackyon 🚀")

# --- 3. UI BRANDING ---
st.subheader("AI YouTube Summariser")
st.markdown("---")

# --- 4. USER INPUT ---
url = st.text_input("Paste YouTube Link here:")
lang = st.selectbox("Select summary language:", ["English", "Tamil", "Hindi"])

# --- 5. THE BRAIN (BULLETPROOF ENGINE) ---
if st.button("Summarize Video"):
    if url:
        with st.spinner("Tackyon is reading the video..."):
            try:
                # Get the transcript using the backup engine that bypasses blocks
                text = yt_dlp_transcript(url)
                
                if not text:
                    st.error("No transcript found for this video. Is it a music video or restricted?")
                else:
                    # AI Processing using the model that worked yesterday
                    # CHANGE THIS LINE:
                    model = genai.GenerativeModel('gemini-3-flash')
                    prompt = f"Provide a detailed summary of this YouTube transcript in {lang}: {text}"
                    response = model.generate_content(prompt)
                    
                    st.success("Victory! Summary below:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
    else:
        st.info("Please paste a link to get started.")
        import streamlit.components.v1 as components

# Replace the data-ad-slot value with your REAL ID once approved
ad_code = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-app-pub-3510846848926159"
     data-ad-slot="6300978111" 
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
"""

# This renders the ad banner
components.html(ad_code, height=100)