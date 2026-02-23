import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
import yt_dlp

# --- 1. SETUP ---
# Using your confirmed stable model: gemini-2.5-flash
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Tackyon AI", page_icon="🚀")
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 2. USER INPUT ---
url = st.text_input("Paste YouTube Link:")
lang_choice = st.selectbox("Select Language Method:", ["Common Languages", "Type My Own Language"])

if lang_choice == "Common Languages":
    lang = st.selectbox("Choose Language:", ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"])
else:
    lang = st.text_input("Type any language in the world (e.g., Japanese, Arabic):")

# --- 3. MAIN LOGIC ---
if st.button("Summarize"):
    if url and lang:
        with st.spinner(f"Tackyon is analyzing the video..."):
            try:
                # Get Video Details (Metadata) first
                video_title = "Unknown Title"
                uploader = "Unknown Creator"
                
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', 'Video')
                    uploader = info.get('uploader', 'Creator')

                # Try to get the Transcript (Manual or Auto)
                text = yt_dlp_transcript(url)
                
                if text:
                    # SITUATION 1 & 2: Full Summary with Points
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"Provide a detailed summary of this video in {lang}. Use clear bullet points and bold headings. Video content: {text}"
                    response = model.generate_content(prompt)
                    
                    st.success(f"Tackyon Victory! Here is your summary for '{video_title}':")
                    st.write(response.text)
                
                else:
                    # SITUATION 3 & 4: Music or Missing Transcripts
                    st.info(f"Tackyon AI found the details: **{video_title}** by **{uploader}**")
                    
                    if "shorts" in url.lower():
                        st.warning("Tackyon AI found this Short, but it is too brief or has no dialogue to summarize. Please try a longer video!")
                    else:
                        st.warning("Tackyon AI can't access a transcript for this video. This usually happens if it is a Music Video or if the audio quality is not clear enough for YouTube to generate text.")

            except Exception as e:
                # Handling Restricted/Private Videos
                error_msg = str(e).lower()
                if "sign in" in error_msg or "confirm your age" in error_msg:
                    st.error("Tackyon AI cannot access this video because it is Private or Age-Restricted.")
                else:
                    st.error(f"Tackyon AI encountered an issue: {str(e)}")
    else:
        st.warning("Please provide both a YouTube link and a language for Tackyon!")

# --- 4. SAFE ADMOB TEST SECTION ---
st.markdown("---") 
st.write("Development Mode: Safety Test Ad")

# USING GOOGLE TEST ID FOR SAFETY: ca-app-pub-3940256099942544/6300978111
components.html(
    f"""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159"
     crossorigin="anonymous"></script>
    <ins class="adsbygoogle"
     style="display:inline-block;width:320px;height:50px"
     data-ad-client="ca-app-pub-3510846848926159"
     data-ad-slot="6300978111"></ins> 
    <script>
     (adsbygoogle = window.adsbygoogle || []).push({{}});
    </script>
    """,
    height=100,
)