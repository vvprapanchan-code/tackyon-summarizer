import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import random

# --- 1. SETUP ---
# We keep the 'st.secrets' because it is required for the cloud to work
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. THIRUKKURAL ---
if 'kural' not in st.session_state:
    kurals = [
        "அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு.",
        "கற்க கசடறக் கற்பவை கற்றபின்\nநிற்க அதற்குத் தக.",
        "எண்ணென்ப ஏனை எழுத்தென்ப இவ்விரண்டும்\nகண்ணென்ப வாழும் உயிர்க்கு.",
        "தொட்டனைத் தூறும் மணற்கேணி மாந்தர்க்குக்\nகற்றனைத் தூறும் அறிவு."
    ]
    st.session_state.kural = random.choice(kurals)

# --- 3. UI BRANDING ---
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")
st.caption(f"✨ *{st.session_state.kural}*")
st.markdown("---")

# --- 4. USER INPUT ---
target_lang = st.selectbox(
    "Select your preferred language:",
    ["English", "Tamil", "Hindi"]
)

youtube_link = st.text_input("Paste your link here:")

# --- 5. THE BRAIN ---
if st.button("Summarize Video"):
    if "youtube.com" not in youtube_link and "youtu.be" not in youtube_link:
        st.warning("⚠️ Please paste a valid video link from YouTube.")
    else:
        try:
            # We use the direct ID extraction that worked yesterday
            if "v=" in youtube_link:
                video_id = youtube_link.split("v=")[1].split("&")[0]
            else:
                video_id = youtube_link.split("/")[-1]
                
            with st.spinner("Tackyon is reading the video..."):
                # We add the cookies file to bypass the "automated request" block
                data = YouTubeTranscriptApi.get_transcript(video_id, cookies='cookies.txt')
                transcript_text = " ".join([item['text'] for item in data])
                
                # AI Summarization
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Summarize this YouTube transcript in {target_lang}: {transcript_text}"
                response = model.generate_content(prompt)
                
                st.success("Summary Generated!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")