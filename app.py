import streamlit as st
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# --- 1. SETUP ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. UI BRANDING ---
st.set_page_config(page_title="Tackyon AI", page_icon="🚀")
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 3. THE BRAIN ---
def get_transcript(video_id):
    try:
        # This is the most stable way to call the library
        # It uses your uploaded cookies.txt to bypass the block
        data = YouTubeTranscriptApi.get_transcript(video_id, cookies='cookies.txt')
        return " ".join([item['text'] for item in data])
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. USER INPUT ---
lang = st.selectbox("Select language:", ["English", "Tamil", "Hindi"])
url = st.text_input("Paste YouTube Link here:")

if st.button("Summarize Video"):
    if url:
        # Simplified ID extraction
        video_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1].split("?")[0]
        
        with st.spinner("Tackyon is reading..."):
            transcript_text = get_transcript(video_id)
            
            if "Error:" in transcript_text:
                st.error(f"Issue found: {transcript_text}")
            else:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Provide a detailed summary of this in {lang}: {transcript_text}"
                response = model.generate_content(prompt)
                st.success("Summary Ready!")
                st.write(response.text)