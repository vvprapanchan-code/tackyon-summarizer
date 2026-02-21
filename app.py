import streamlit as st
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai

# --- SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser (Bulletproof Version)")

# --- USER INPUT ---
url = st.text_input("Paste YouTube Link:")
lang = st.selectbox("Language:", ["English", "Tamil", "Hindi"])

if st.button("Summarize"):
    if url:
        with st.spinner("Tackyon is bypassing blocks..."):
            try:
                # Using the new engine to get the transcript
                text = yt_dlp_transcript(url)
                
                if not text:
                    st.error("No transcript found for this video.")
                else:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"Summarize in {lang}: {text}")
                    st.success("Victory! Summary below:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Even the backup failed: {str(e)}")