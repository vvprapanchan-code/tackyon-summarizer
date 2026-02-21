import streamlit as st
# The "Master Key" Import
from youtube_transcript_api import YouTubeTranscriptApi as yta
import google.generativeai as genai

# --- 1. SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- 2. UI ---
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 3. THE BRAIN ---
def get_transcript(video_id):
    try:
        # We are using the 'yta' nickname to make the call bulletproof
        data = yta.get_transcript(video_id, cookies='cookies.txt')
        return " ".join([item['text'] for item in data])
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. INPUT & ACTION ---
url = st.text_input("Paste YouTube Link:")
lang = st.selectbox("Language:", ["English", "Tamil", "Hindi"])

if st.button("Summarize"):
    if url:
        # Extract Video ID
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        else:
            video_id = url.split("/")[-1]
            
        with st.spinner("Tackyon is reading..."):
            text = get_transcript(video_id)
            if "Error:" in text:
                st.error(f"YouTube block detected. Technical info: {text}")
            else:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Summarize this in {lang}: {text}")
                st.write(response.text)