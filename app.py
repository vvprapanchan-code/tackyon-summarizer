import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai

# --- 1. SETUP ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 2. USER INPUT ---
url = st.text_input("Paste YouTube Link:")
lang_choice = st.selectbox("Select Language Method:", ["Common Languages", "Type My Own Language"])

if lang_choice == "Common Languages":
    lang = st.selectbox("Choose Language:", ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"])
else:
    lang = st.text_input("Type any language in the world:")

if st.button("Summarize"):
    if url and lang:
        with st.spinner(f"Tackyon is working..."):
            try:
                # Engine that bypasses blocks
                text = yt_dlp_transcript(url)
                
                if text:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(f"Summarize this in {lang}: {text}")
                    st.success(f"Tackyon Victory! Summary in {lang} below:")
                    st.write(response.text)
                else:
                    # SMART TACKYON LOGIC
                    if "shorts" in url.lower():
                        st.warning("Tackyon AI can't summarize this Short because it's too brief or has no dialogue. Please give Tackyon a longer video!")
                    else:
                        st.info("Tackyon AI can't find a transcript for this video. It might be a Music Video or have poor audio quality. Please try a video with Subtitles (CC).")
            
            except Exception as e:
                # Tackyon friendly error messages
                if "sign in" in str(e).lower() or "confirm your age" in str(e).lower():
                    st.error("Tackyon AI cannot access this video because it is Private or Age-Restricted.")
                else:
                    st.error(f"Tackyon encountered an issue: {str(e)}")
    else:
        st.warning("Please provide both a YouTube link and a language for Tackyon!")

# --- 3. SAFE ADMOB TEST SECTION ---
st.markdown("---") 
st.write("Development Mode: Safety Test Ad")

# USING GOOGLE TEST ID: ca-app-pub-3940256099942544/6300978111
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