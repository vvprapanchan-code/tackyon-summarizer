import streamlit as st
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai

# --- 1. API SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 2. BRANDING ---
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 3. USER INPUT ---
url = st.text_input("Paste YouTube Link:")
lang = st.selectbox("Language:", ["English", "Tamil", "Hindi"])

# --- 4. THE ENGINE (WORKING VERSION) ---
if st.button("Summarize"):
    if url:
        with st.spinner("Tackyon is working..."):
            try:
                # Using your bulletproof engine
                text = yt_dlp_transcript(url)
                
                if not text:
                    st.error("No transcript found for this video.")
                else:
                    # RESTORED: The specific model that gave you victory yesterday
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    response = model.generate_content(f"Summarize in {lang}: {text}")
                    
                    st.success("Victory! Summary below:")
                    st.write(response.text)
                    
            except Exception as e:
                # Simplified error reporting just like before
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please paste a link first!")