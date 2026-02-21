import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import random

# --- 1. SECURE API SETUP ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. THIRUKKURAL SETUP ---
if 'kural' not in st.session_state:
    kurals = [
        "அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு.",
        "கற்க கசடறக் கற்பவை கற்றபின் நிற்க அதற்குத் தக.",
        "எண்ணென்ப ஏனை எழுத்தென்ப இவ்விரண்டும் கண்ணென்ப வாழும் உயிர்க்கு.",
        "தொட்டனைத் தூறும் மணற்கேணி மாந்தர்க்குக் கற்றனைத் தூறும் அறிவு."
    ]
    st.session_state.kural = random.choice(kurals)

# --- 3. UI BRANDING ---
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")
st.info(st.session_state.kural)

# --- 4. THE BRAIN ---
def get_transcript(video_id):
    try:
        # Using your uploaded cookies.txt for the VIP Pass
        data = YouTubeTranscriptApi.get_transcript(video_id, cookies='cookies.txt')
        return " ".join([item['text'] for item in data])
    except Exception as e:
        return f"Error: {str(e)}"

# --- 5. USER INPUT ---
lang = st.selectbox("Select language:", ["English", "Tamil", "Hindi"])
url = st.text_input("YouTube Link:")

if st.button("Summarize Video"):
    if "v=" in url or "youtu.be/" in url:
        # Extracting Video ID
        video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1].split("?")[0]
        
        with st.spinner("Tackyon is reading the video..."):
            text = get_transcript(video_id)
            
            if "Error:" in text:
                st.error(f"YouTube block detected. Technical info: {text}")
            else:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Summarize this YouTube transcript in {lang}: {text}"
                response = model.generate_content(prompt)
                st.write(response.text)
    else:
        st.warning("Please enter a valid YouTube link.")