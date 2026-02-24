import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
import yt_dlp
import datetime

# --- 1. CORE CONFIGURATION ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Global App Settings
st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# Session State for Persistence
if 'summary' not in st.session_state: st.session_state.summary = ""
if 'transcript' not in st.session_state: st.session_state.transcript = ""
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False

# --- 2. PROFESSIONAL INTERFACE (SIDEBAR) ---
with st.sidebar:
    st.title("Tackyon AI")
    
    # AUTHENTICATION SECTION
    if not st.session_state.user_authenticated:
        st.subheader("User Login")
        auth_method = st.radio("Method", ["Email", "Phone Number"])
        user_id = st.text_input(f"Enter {auth_method}")
        if st.button("Request Verification Code"):
            st.info(f"Verification code sent to {user_id}. (Backend Connection Required)")
            # Logic: When code is verified, set st.session_state.user_authenticated = True
    else:
        st.success("Authenticated: User Session Active")

    st.markdown("---")
    # UI CUSTOMIZATION
    st.subheader("Personalization")
    bg_color = st.color_picker("Background Color", "#0e1117")
    font_style = st.selectbox("Application Font", ["sans-serif", "serif", "monospace"])
    
    st.markdown("---")
    st.subheader("Analysis History")
    # Placeholder for Database retrieval logic
    st.write("1. Finland Education System...")
    st.write("2. Samsung Tech Review...")

# --- 3. CUSTOM THEME INJECTION ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; font-family: {font_style}; }}
    .stButton>button {{ border-radius: 5px; height: 3em; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. ANALYTICS ENGINE ---
st.header("Tackyon AI: Advanced Video Analytics")
url = st.text_input("Enter YouTube URL for Analysis:")
lang = st.selectbox("Target Language", ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"])

if st.button("Analyze Video Content"):
    if url and lang:
        with st.spinner("Tackyon AI is processing the request..."):
            try:
                # Metadata Retrieval
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title, uploader = info.get('title', 'N/A'), info.get('uploader', 'N/A')
                
                # Transcript Processing
                try:
                    text = yt_dlp_transcript(url)
                    st.session_state.transcript = text
                except:
                    text = None

                if text:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"""
                    Provide a professional analysis of this video in {lang}:
                    - Executive Summary (Bullet points)
                    - Structural Table of Contents
                    - Tone and Sentiment Assessment
                    Original Content: {text}
                    """
                    response = model.generate_content(prompt)
                    st.session_state.summary = response.text
                    st.success(f"Analysis Complete: {title}")
                else:
                    st.info(f"Metadata Identified: **{title}** by **{uploader}**")
                    st.warning("Transcript unavailable. This typically occurs with music-only content or poor audio quality.")

            except Exception:
                st.info("System Notification: Unable to access private or restricted content.")

# --- 5. POST-ANALYSIS TOOLS ---
if st.session_state.summary:
    t1, t2, t3 = st.tabs(["📊 Insights", "📝 Content Suite", "💬 Video Query"])
    
    with t1:
        st.markdown(st.session_state.summary)
        st.download_button("Export Analysis (.txt)", st.session_state.summary, file_name="Tackyon_Report.txt")

    with t2:
        st.write("Content Transformation Tools")
        if st.button("Generate Professional Blog Draft"):
            model = genai.GenerativeModel('gemini-2.5-flash')
            res = model.generate_content(f"Convert this to a formal blog post in {lang}: {st.session_state.summary}")
            st.markdown(res.text)
        
        if st.button("Generate Social Media Thread"):
            model = genai.GenerativeModel('gemini-2.5-flash')
            res = model.generate_content(f"Draft a 5-part educational thread in {lang}: {st.session_state.summary}")
            st.markdown(res.text)

    with t3:
        query = st.chat_input("Query specific details from this video...")
        if query:
            # BRAND LOGIC: "BOSS" RESPONSE
            if any(x in query.lower() for x in ["who developed", "who made", "who is your boss"]):
                st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**. He is the lead architect of the Tackyon AI project.")
            else:
                model = genai.GenerativeModel('gemini-2.5-flash')
                res = model.generate_content(f"Using this transcript: {st.session_state.transcript}, answer: {query}")
                st.chat_message("assistant").write(res.text)

# --- 6. ADVERTISING (DEVELOPMENT MODE) ---
st.markdown("---")
st.write("Commercial Placement")
components.html(
    f"""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159"
     crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px"
     data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    """, height=100,
)