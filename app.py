import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
import yt_dlp
import datetime

# --- 1. SETUP & SESSION STATE ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

if 'summary' not in st.session_state: st.session_state.summary = ""
if 'transcript' not in st.session_state: st.session_state.transcript = ""

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")
st.title("Tackyon 🚀")
st.subheader("The Undefeatable AI YouTube Suite")

# --- 2. USER INPUT ---
col1, col2 = st.columns([2, 1])
with col1:
    url = st.text_input("Paste YouTube Link:")
with col2:
    lang = st.selectbox("Choose Language:", ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada", "Custom"])
    if lang == "Custom":
        lang = st.text_input("Type Language:")

# --- 3. MAIN ENGINE ---
if st.button("🚀 Execute Tackyon Engine"):
    if url and lang:
        with st.spinner(f"Tackyon is processing..."):
            try:
                # Metadata Extraction
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title, uploader = info.get('title', 'Video'), info.get('uploader', 'Creator')
                
                # Transcript with Safety Try-Catch
                try:
                    text = yt_dlp_transcript(url)
                    st.session_state.transcript = text
                except:
                    text = None

                if text:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    # ADVANCED PROMPT: Summary + Timestamps + Sentiment
                    prompt = f"""Analyze this YouTube video: {text}. 
                    Provide:
                    1. A detailed Summary in {lang} with bold headings.
                    2. A 'Table of Contents' with approximate Interactive Timestamps.
                    3. A 'Sentiment Analysis' (is the tone happy, angry, or informative?).
                    Use bullet points for everything."""
                    
                    response = model.generate_content(prompt)
                    st.session_state.summary = response.text
                    st.success(f"Tackyon Victory! Analysis for '{title}' complete.")
                else:
                    st.info(f"Tackyon AI identified: **{title}** by **{uploader}**")
                    st.warning("Tackyon AI can't access a transcript for this video. This happens with Music or low-audio videos.")

            except Exception as e:
                st.info(f"Tackyon AI is currently unable to process this link. (Private/Restricted content)")

# --- 4. ADVANCED FEATURE TABS ---
if st.session_state.summary:
    tab1, tab2, tab3 = st.tabs(["📊 Summary & Insights", "✍️ Content Creator", "💬 Chat with Video"])
    
    with tab1:
        st.markdown(st.session_state.summary)
        # FEATURE: Download Summary
        st.download_button("📥 Download Summary as Text", st.session_state.summary, file_name="tackyon_summary.txt")

    with tab2:
        st.write("Convert this video into content for your social media!")
        if st.button("Generate Blog Post"):
            model = genai.GenerativeModel('gemini-2.5-flash')
            blog_resp = model.generate_content(f"Rewrite this summary as a professional blog post in {lang}: {st.session_state.summary}")
            st.markdown(blog_resp.text)
        
        if st.button("Create Twitter (X) Thread"):
            model = genai.GenerativeModel('gemini-2.5-flash')
            tweet_resp = model.generate_content(f"Create a 5-tweet thread from this summary in {lang}: {st.session_state.summary}")
            st.markdown(tweet_resp.text)

    with tab3:
        # FEATURE: Chat with Video Context
        user_query = st.chat_input("Ask Tackyon a specific question about this video...")
        if user_query:
            model = genai.GenerativeModel('gemini-2.5-flash')
            chat_resp = model.generate_content(f"Using this transcript: {st.session_state.transcript}, answer this: {user_query}")
            with st.chat_message("assistant"):
                st.write(chat_resp.text)

# --- 5. FAKE AD SECTION ---
st.markdown("---")
st.write("Development Mode: Safety Test Ad")
components.html(
    f"""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159"
     crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px"
     data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    """, height=100,
)