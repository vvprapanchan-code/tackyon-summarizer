import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
import yt_dlp

# --- 1. SETUP ---
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
    lang = st.text_input("Type any language in the world:")

# --- 3. MAIN LOGIC (FIXED TO AVOID RED ERRORS) ---
if st.button("Summarize"):
    if url and lang:
        with st.spinner(f"Tackyon is analyzing..."):
            try:
                # STEP A: Get Details First
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Video')
                    uploader = info.get('uploader', 'Creator')

                # STEP B: Try for Transcript
                try:
                    text = yt_dlp_transcript(url)
                except:
                    text = None # This prevents the "cannot download subtitles" red box

                if text:
                    # SUCCESS: Detailed Summary
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"Provide a detailed summary of this video in {lang} with bullet points. Content: {text}"
                    response = model.generate_content(prompt)
                    st.success(f"Tackyon Victory! Summary for '{title}':")
                    st.write(response.text)
                else:
                    # FRIENDLY FALLBACK (Blue/Yellow Boxes)
                    st.info(f"Tackyon AI identified: **{title}** by **{uploader}**")
                    if "shorts" in url.lower():
                        st.warning("Tackyon AI cannot summarize this Short because it is too brief. Try a longer video!")
                    else:
                        st.warning("Tackyon AI cannot access a transcript for this video. This usually happens with Music, poor audio, or if the video is very new.")

            except Exception as e:
                # Catching Age Restrictions & Private Videos
                error_str = str(e).lower()
                if "sign in" in error_str or "age" in error_str:
                    st.info(f"Tackyon AI cannot access this video because it is Private or Age-Restricted.")
                else:
                    st.info(f"Tackyon AI is currently unable to process this specific link. Please try another one!")

    else:
        st.warning("Please provide a link and language for Tackyon!")

# --- 4. SAFE ADMOB TEST SECTION ---
st.markdown("---") 
st.write("Development Mode: Safety Test Ad")
components.html(
    f"""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159"
     crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px"
     data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins> 
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    """,
    height=100,
)