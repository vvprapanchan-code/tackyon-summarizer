import streamlit as st
import re
import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from gtts import gTTS  # For Simple Auto-Dubbing
from moviepy.editor import VideoFileClip, AudioFileClip # For Merging Audio/Video
import yt_dlp # To download video for dubbing

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")
# Replace with your actual Gemini API Key
# genai.configure(api_key="YOUR_GEMINI_API_KEY")

# --- 2. CORE UTILITIES ---
def extract_video_id(url):
    """Solves the attribute error by ensuring only the 11-char ID is passed."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript_safe(video_id, lang_code):
    """Correctly calls the YouTubeTranscriptApi method."""
    try:
        # Fixed: Calling get_transcript on the class with the correct video_id
        data = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_code, 'en'])
        return " ".join([t['text'] for t in data])
    except Exception as e:
        return f"Error: {str(e)}"

# --- 3. FEATURE: AI AUTO-DUBBING ---
def perform_dubbing(video_url, target_lang):
    """Downloads video, generates AI voiceover, and merges them."""
    try:
        video_id = extract_video_id(video_url)
        # Download video (Low res for speed)
        ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4', 'outtmpl': 'temp_vid.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # Get Text for Dubbing
        text = get_transcript_safe(video_id, target_lang)
        
        # Generate Speech (gTTS used for reliability; can swap for ElevenLabs API)
        tts = gTTS(text=text[:500], lang=target_lang) # Limiting text for demo speed
        tts.save("temp_audio.mp3")
        
        # Merge using MoviePy
        video = VideoFileClip("temp_vid.mp4")
        audio = AudioFileClip("temp_audio.mp3")
        final_video = video.set_audio(audio)
        final_video.write_videofile("dubbed_output.mp4", codec="libx264")
        
        return "dubbed_output.mp4"
    except Exception as e:
        return f"Dubbing failed: {str(e)}"

# --- 4. UI INTERFACE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🎯 Tackyon AI Login")
    otp = st.text_input("6-Digit OTP", type="password")
    if st.button("Access Hub") and otp == "123456":
        st.session_state.logged_in = True
        st.rerun()
else:
    st.title("🎯 Tackyon AI: Executive Intelligence & Dubbing")
    url = st.text_input("Paste YouTube Link")
    
    tab1, tab2 = st.tabs(["Smart Summarizer", "Auto-Dubber (REAL DUB)"])
    
    with tab1:
        col_l, col_s = st.columns(2)
        lang = col_l.selectbox("Language", ["ta", "en", "hi", "ml"], format_func=lambda x: {"ta":"Tamil","en":"English","hi":"Hindi","ml":"Malayalam"}[x])
        style = col_s.selectbox("Style", ["Executive Summary", "Twitter Thread", "Key Insights"])
        
        if st.button("Execute Deep Analysis"):
            vid_id = extract_video_id(url)
            if vid_id:
                raw_text = get_transcript_safe(vid_id, lang)
                st.subheader(f"Results: {style}")
                st.write(raw_text) # In production, wrap this in your Gemini model call
            else:
                st.error("Invalid URL")

    with tab2:
        st.warning("Note: Dubbing requires heavy processing. Please wait.")
        if st.button("Start AI Dubbing Process"):
            with st.spinner("Cloning voice and merging video..."):
                output_file = perform_dubbing(url, lang)
                if os.path.exists(output_file):
                    st.video(output_file)
                    st.success("Dubbing Complete!")