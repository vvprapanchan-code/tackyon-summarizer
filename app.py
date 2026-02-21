import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import random

# --- 1. SETUP ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. UI ---
st.set_page_config(page_title="Tackyon AI", page_icon="🚀")
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 3. THE BRAIN ---
def get_transcript(video_id):
    try:
        # Correct command is get_transcript (singular)
        # We MUST use the cookies file you uploaded to GitHub
        data = YouTubeTranscriptApi.get_transcript(video_id, cookies='cookies.txt')
        return " ".join([item['text'] for item in data])
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. USER INPUT ---
lang = st.selectbox("Select language:", ["English", "Tamil", "Hindi"])
url = st.text_input("Paste YouTube Link:")

if st.button("Summarize Video"):
    if url:
        # Extract the ID from the link
        video_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
        
        with st.spinner("Tackyon is reading..."):
            transcript = get_transcript(video_id)
            
            if "Error:" in transcript:
                st.error(f"Issue found: {transcript}")
            else:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Summarize this in {lang}: {transcript}"
                response = model.generate_content(prompt)
                st.success("Done!")
                st.write(response.text)