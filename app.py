import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai  # For Intelligence Analysis
import re
import pandas as pd

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Tackyon AI", page_icon="🎯", layout="wide")

# Custom CSS for UI Personalization
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY: OTP & PERSISTENT LOGIN ---
# (Simplified logic; in production, connect this to your Supabase instance)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_ui():
    st.subheader("🔒 Secure Executive Access")
    otp = st.text_input("Enter 6-Digit OTP", type="password")
    if st.button("Verify Identity"):
        if otp == "123456": # Replace with Supabase OTP verification
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid OTP")

# --- 3. INTELLIGENCE ENGINE ---
def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_ai_intelligence(transcript, style, language):
    # Configure your Gemini API Key
    # genai.configure(api_key="YOUR_API_KEY")
    model = genai.GenerativeModel('gemini-pro')
    
    prompts = {
        "Executive Summary": f"Provide a concise executive summary in {language} for: ",
        "Twitter Thread": f"Transform this into a viral 5-tweet thread in {language}: ",
        "Key Insights": f"Extract the top 5 strategic insights in {language} from: "
    }
    
    response = model.generate_content(f"{prompts[style]} {transcript[:10000]}")
    return response.text

# --- 4. MAIN APPLICATION INTERFACE ---
if not st.session_state.logged_in:
    login_ui()
else:
    # Header Section
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    with col2:
        st.title("Tackyon AI: Video Intelligence & Dubbing")

    # Input Section
    url_input = st.text_input("Paste YouTube Link (Shorts/Vlogs/Long-form)", placeholder="https://youtube.com/...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        lang = st.selectbox("Language", ["Tamil", "English", "Hindi", "Malayalam"])
    with col_b:
        style = st.selectbox("Style", ["Executive Summary", "Twitter Thread", "Key Insights"])

    if st.button("Execute Deep Analysis"):
        video_id = extract_video_id(url_input)
        
        if video_id:
            try:
                # Map language to ISO codes
                lang_map = {"Tamil": "ta", "English": "en", "Hindi": "hi", "Malayalam": "ml"}
                
                with st.spinner(f"Extracting {lang} Intelligence..."):
                    # Step 1: Extract Transcript
                    transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_map[lang], 'en'])
                    full_text = " ".join([t['text'] for t in transcript_data])
                    
                    # Step 2: AI Analysis
                    intelligence = get_ai_intelligence(full_text, style, lang)
                    
                    st.success("Analysis Complete!")
                    st.markdown(f"### {style}")
                    st.write(intelligence)
                    
                    # Step 3: Download Options
                    st.download_button("Download Report (TXT)", intelligence, file_name="tackyon_report.txt")
                    
            except Exception as e:
                st.error(f"Intelligence extraction failed: {str(e)}")
                st.info("💡 Tip: Ensure the video has captions enabled for 'Smart Response' to function.")
        else:
            st.warning("Please provide a valid YouTube URL.")

    # Sidebar: History & Planned Features
    with st.sidebar:
        st.header("Executive Hub")
        st.info("🗂️ Private History (Supabase Locked)")
        st.divider()
        st.write("🚀 **Planned Features:**")
        st.write("- Thirukural Gateway")
        st.write("- AI Auto-Dubbing")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()