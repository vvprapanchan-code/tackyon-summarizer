import streamlit as st
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai

# --- 1. SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 2. USER INPUT ---
url = st.text_input("Paste YouTube Link:")

# NEW: Allow users to type ANY language in the world
lang_choice = st.selectbox("Select Language Method:", ["Common Languages", "Type My Own Language"])

if lang_choice == "Common Languages":
    lang = st.selectbox("Choose Language:", ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"])
else:
    lang = st.text_input("Type any language in the world (e.g., Japanese, Italian, Arabic):")

if st.button("Summarize"):
    if url and lang:
        with st.spinner(f"Tackyon is working in {lang}..."):
            try:
                # Engine that bypasses blocks
                text = yt_dlp_transcript(url)
                
                if not text:
                    st.error("No transcript found for this video.")
                else:
                    # Your confirmed working model
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # The AI will translate into whatever language is stored in the 'lang' variable
                    response = model.generate_content(f"Summarize this in {lang}: {text}")
                    st.success(f"Victory! Summary in {lang} below:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please provide both a YouTube link and a language!")