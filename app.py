import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import random

# --- 1. SETUP ---
# Ensure your key is still set correctly in Streamlit Cloud Secrets
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
    "Select summary language:",
    ["English", "Tamil", "Hindi"]
)

youtube_link = st.text_input("Paste YouTube link here:")

# --- 5. THE BRAIN ---
if st.button("Summarize Video"):
    if youtube_link:
        try:
            # Extract Video ID
            if "v=" in youtube_link:
                video_id = youtube_link.split("v=")[1].split("&")[0]
            else:
                video_id = youtube_link.split("/")[-1]
            
            with st.spinner("Tackyon is reading the video..."):
                # Get Transcript using the API that worked yesterday
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([i['text'] for i in transcript])
                
                # Use the Model that was successful yesterday
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Summarize this YouTube video transcript in {target_lang} with key highlights: {full_text}"
                response = model.generate_content(prompt)
                
                st.success("Summary Ready!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please paste a link first!")