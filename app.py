import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import random

# --- ⚠️ PASTE YOUR API KEY BELOW ⚠️ ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- FEATURE 2: Random Thirukkural Setup ---
# We use st.session_state so the quote doesn't constantly change while typing
if 'kural' not in st.session_state:
    kurals = [
        "அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு.",
        "கற்க கசடறக் கற்பவை கற்றபின்\nநிற்க அதற்குத் தக.",
        "எண்ணென்ப ஏனை எழுத்தென்ப இவ்விரண்டும்\nகண்ணென்ப வாழும் உயிர்க்கு.",
        "தொட்டனைத் தூறும் மணற்கேணி மாந்தர்க்குக்\nகற்றனைத் தூறும் அறிவு."
    ]
    st.session_state.kural = random.choice(kurals)

# --- UI BRANDING ---
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")
st.caption(f"✨ *{st.session_state.kural}*")
st.markdown("---")

# --- FEATURE 6: Language Translation ---
target_lang = st.selectbox(
    "Select your preferred language:",
    ["English", "Tamil", "Hindi", "Spanish", "Original Video Language"]
)

# --- INPUT ---
st.write("Paste your link here to summarise:")
youtube_link = st.text_input("YouTube Link:")

if st.button("Summarize Video"):
    # --- FEATURE 4: Fake Link Detection ---
    if "youtube.com" not in youtube_link and "youtu.be" not in youtube_link:
        st.warning("⚠️ Please paste a valid video link from YouTube.")
    else:
        try:
            # Extract Video ID
            clean_link = youtube_link.strip()
            if "youtu.be" in clean_link:
                video_id = clean_link.split("/")[-1].split("?")[0]
            else:
                video_id = clean_link.split("v=")[1].split("&")[0]
            
            st.info("Reading video subtitles...")
            
            # Fetch Transcript
            api = YouTubeTranscriptApi()
            # We fetch English by default to pass to the AI, the AI will translate it later
            fetched_data = api.fetch(video_id, languages=['en', 'ta', 'hi']) 
            transcript_list = fetched_data.to_raw_data()
            
            full_transcript = ""
            for item in transcript_list:
                full_transcript += " " + item["text"]
            
            st.info("Tackyon AI is analyzing the video length and generating the summary...")
            
            # --- FEATURE 3 & 5: Smart Length & Any Video Type ---
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"""
            You are Tackyon, a highly intelligent video summarizer. 
            Analyze the following video transcript. If the transcript is very long, provide a detailed, comprehensive summary. If it is short, provide a quick, brief summary. 
            Focus only on the most important points.
            The final output MUST be written in {target_lang}.
            
            Transcript:
            {full_transcript}
            """
            
            response = model.generate_content(prompt)
            
            st.success("Summary Complete!")
            st.markdown(response.text) 
            
        except Exception as e:
            st.error("Could not read this video. Make sure it has readable subtitles!")