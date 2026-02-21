import streamlit as st
# This specific way of importing is the key fix
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
        # Verified correct method call for the library
        # Uses your cookies.txt file to bypass blocks
        data = YouTubeTranscriptApi.get_transcript(video_id, cookies='cookies.txt')
        return " ".join([item['text'] for item in data])
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. USER INPUT ---
lang = st.selectbox("Select language:", ["English", "Tamil", "Hindi"])
url = st.text_input("Paste YouTube Link:")

if st.button("Summarize Video"):
    if url:
        # Smarter way to get the ID from any YouTube link
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            video_id = url.split("/")[-1]
        
        with st.spinner("Tackyon is reading..."):
            transcript = get_transcript(video_id)
            
            if "Error:" in transcript:
                st.error(f"Issue found: {transcript}")
            else:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Summarize this in {lang}: {transcript}"
                response = model.generate_content(prompt)
                st.success("Summary Ready!")
                st.write(response.text)