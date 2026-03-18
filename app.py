import streamlit as st
import streamlit.components.v1 as components
import time
import base64
import os
import random
import json
import google.generativeai as genai
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
from gtts import gTTS

# --- 1. THEME & EXECUTIVE ARCHITECTURE (PROTECTED) ---
st.set_page_config(page_title="Tackyon AI", page_icon="logo.jpg", layout="wide")

st.markdown("""
<style>
header, [data-testid="stHeader"], .stAppHeader { display: none !important; visibility: hidden !important; }
.block-container { padding-top: 0px !important; margin-top: -30px !important; }

.kural-box {
    background-color: #FDFEFE;
    border-bottom: 3px solid #D4AC0D;
    padding: 20px;
    text-align: center;
    width: 100%;
    margin-bottom: 35px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.kural-line1 { font-size: 1.5em; font-weight: bold; color: #1B2631; margin-bottom: 8px; }
.kural-line2 { font-size: 1.3em; color: #5D6D7E; font-style: italic; }

.executive-card {
    background: white; 
    padding: 45px; 
    border-radius: 25px;
    box-shadow: 0 15px 50px rgba(0,0,0,0.12); 
    border-top: 8px solid #1B2631;
    text-align: center; 
    max-width: 900px; 
    margin: auto;
    margin-bottom: 30px;
}

@keyframes t-pulse {
    0% { transform: scale(1); filter: brightness(100%); }
    50% { transform: scale(1.06); filter: brightness(130%); }
    100% { transform: scale(1); filter: brightness(100%); }
}
.pulse-layer { animation: t-pulse 2.5s infinite ease-in-out; }

.analysis-result {
    background: #F8F9F9; 
    padding: 30px; 
    border-radius: 18px;
    border-left: 10px solid #1B2631; 
    text-align: left;
    margin-top: 25px; 
    color: #1C2833; 
    line-height: 1.8;
    font-family: 'Inter', sans-serif;
}

.report-watermark {
    text-align: right; font-size: 10px; color: #BDC3C7;
    font-weight: 900; letter-spacing: 2px; margin-top: 15px;
}

.assistant-header {
    display: flex; align-items: center; margin-top: 30px;
    padding: 15px; background: #1B2631; color: white; border-radius: 15px 15px 0 0;
}
.assistant-icon {
    width: 30px; height: 30px; background: white; color: #1B2631;
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-weight: 900; margin-right: 12px;
}
.assistant-body {
    background: white; border: 1px solid #1B2631;
    border-radius: 0 0 15px 15px; padding: 20px; margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)

# --- GLOBAL LANGUAGE HUB ---
LANG_HUB = {
    "Tamil": "ta", "English": "en", "Hindi": "hi", "Malayalam": "ml", "Telugu": "te",
    "Kannada": "kn", "French": "fr", "German": "de", "Spanish": "es", "Japanese": "ja",
    "Chinese": "zh-cn", "Arabic": "ar", "Russian": "ru", "Portuguese": "pt", "Korean": "ko"
}

# --- 2. LOGO ENGINE (STABLE SCANNER) ---
def load_logo_proven():
    try:
        search_list = ["logo.jpg", "logo.jpg.jpeg", "tackyon logo", "logo.jpeg"]
        for f in search_list:
            if os.path.exists(f):
                with open(f, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
        for file in os.listdir("."):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                with open(file, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
    except:
        return None
    return None

logo_data = load_logo_proven()

def render_t_logo(size="100px", animate=False):
    if logo_data:
        anim_class = "pulse-layer" if animate else ""
        st.markdown(
            f'<div class="{anim_class}" style="text-align: center; margin-bottom: 25px;">'
            f'<img src="data:image/jpeg;base64,{logo_data}" style="width:{size}; border-radius: 20px;"></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="text-align: center; font-size: 35px; font-weight: bold; color: #1B2631;">TACKYON AI</div>',
            unsafe_allow_html=True
        )

# --- 3. DATABASE ENGINE (KURAL LOADER) ---
def get_random_kural():
    try:
        if os.path.exists("thirukural.json"):
            with open("thirukural.json", "r", encoding="utf-8") as f:
                db = json.load(f)
                return random.choice(db)
    except:
        pass
    return {"top": "கற்க கசடறக் கற்பவை கற்றபின்", "bottom": "நிற்க அதற்குத் தக"}

# --- 4. INTELLIGENCE ENGINE (GLOBAL & SECURE) ---
def get_video_data(url):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            metadata = {
                "title": info.get('title', 'Unknown Resource'),
                "channel": info.get('uploader', 'Independent Creator'),
                "description": info.get('description', '')[:2000],
                "id": info.get('id', '')
            }
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(info['id'])
                transcript = " ".join([t['text'] for t in transcript_list])
                return metadata, transcript, "full"
            except:
                return metadata, None, "meta_only"
    except:
        return None, None, "error"

def generate_ai_analysis(transcript, metadata, style, lang, mode):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        if mode == "meta_only":
            prompt = f"Act as a Brand Expert. Based on Title: {metadata['title']} and Description: {metadata['description']}, provide a detailed {style} in {lang}."
        else:
            prompt = f"Act as an Executive Analyst. Analyze: {transcript}. Provide a deep {style} in {lang}."

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Intelligence Hub Offline. Error: {str(e)}"

# --- FIXED DUBBING ENGINE WITH SMART FALLBACK ---
def execute_neural_dubbing(transcript, metadata, lang_name, mode):
    """Bypasses missing transcripts by using metadata for dubbing context."""
    try:
        target_code = LANG_HUB.get(lang_name, "en")
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        if mode == "meta_only":
            dub_prompt = f"Create a natural spoken audio script in {lang_name} based on this video metadata: Title: {metadata['title']}, Description: {metadata['description']}. Just output the speech script."
        else:
            dub_prompt = f"Translate this transcript into a natural spoken script for {lang_name}. Output only the speech: {transcript[:4000]}"

        translated_script = model.generate_content(dub_prompt).text
        tts = gTTS(text=translated_script, lang=target_code, slow=False)
        tts.save("dubbed_audio.mp3")
        return "dubbed_audio.mp3"

    except Exception as e:
        st.error(f"Dubbing Studio Error: {str(e)}")
        return None

def run_tackyon_assistant(user_query, context, lang):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        persona_prompt = f"Role: Tackyon AI Assistant. Creator: Prapanchan. Context: {context[:4000]}. Query: {user_query} in {lang}."
        response = model.generate_content(persona_prompt)
        return response.text

    except:
        return "Assistant is processing."

# --- 5. THE EXECUTIVE WORKFLOW ---
if "flow_stage" not in st.session_state:
    st.session_state.flow_stage = "animation"
    st.session_state.daily_kural = get_random_kural()
    st.session_state.chat_history = []
    # Add this line so the app knows who you are without asking
    st.session_state.user = {"name": "Executive", "gender": "Executive", "age": 25}

if st.session_state.flow_stage == "animation":
    st.markdown('<div style="height: 30vh;"></div>', unsafe_allow_html=True)
    render_t_logo(size="380px", animate=True)
    time.sleep(2.5)
    st.session_state.flow_stage = "hub" # This jumps straight to the main app
    st.rerun()





else:
    st.sidebar.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    render_t_logo(size="150px")
    st.sidebar.markdown(f"### Executive: {st.session_state.user['name']}")
    st.sidebar.divider()

    st.title("Executive Intelligence Hub")
    url = st.text_input("Resource URL", placeholder="Paste YouTube Link")

    tab_sum, tab_dub, tab_ast = st.tabs(["Intelligence Summary", "Neural Dubbing Studio", "Tackyon Assistant"])

    with tab_sum:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            lang_sum = st.selectbox("Summary Language", list(LANG_HUB.keys()))
        with c2:
            style = st.selectbox("Analysis Style", ["Comprehensive Summary", "Strategic Points", "Exam Guide"])

        if st.button("Generate Intelligence Report", use_container_width=True):
            if url:
                with st.spinner("Decoding via Gemini 2.5 Flash..."):
                    m, t, mode = get_video_data(url)

                    if mode == "error": 
                        st.error("Access Denied.")
                    else:
                        res = generate_ai_analysis(t, m, style, lang_sum, mode)
                        st.session_state.last_analysis = res
                        
                        st.markdown(f'<div class="analysis-result">{res}<div class="report-watermark">(T) TACKYON AI</div></div>', unsafe_allow_html=True)
                        st.download_button("📥 Export Report", f"REPORT\n\n{res}", file_name="Tackyon_Report.txt")

                        # The Ad component is now properly indented inside the 'else' block
                        components.html(
                            f"""
                            <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159"
                            crossorigin="anonymous"></script>
                            <ins class="adsbygoogle"
                                 style="display:inline-block;width:320px;height:50px"
                                 data-ad-client="ca-pub-3510846848926159"
                                 data-ad-slot="1148139407"></ins>
                            <script>
                                 (adsbygoogle = window.adsbygoogle || []).push({{}});
                            </script>
                            """,
                            height=100,
                        )

        st.markdown('</div>', unsafe_allow_html=True)

    with tab_dub:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.subheader("Neural Overdubbing (Audio Only)")

        dub_lang = st.selectbox("Dubbing Target Language", list(LANG_HUB.keys()), key="dub_lang")

        if st.button("Start Neural Dubbing", use_container_width=True):
            if url:
                with st.spinner(f"Synthesizing {dub_lang} Voice..."):
                    m, t, mode = get_video_data(url)

                    if m:
                        audio_path = execute_neural_dubbing(t, m, dub_lang, mode)

                        if audio_path:
                            st.success(f"Dubbing Complete: {dub_lang} Persona Ready.")
                            st.audio(audio_path)
                    else:
                        st.error("Resource inaccessible.")

        st.markdown('</div>', unsafe_allow_html=True)

    with tab_ast:
        st.markdown('<div class="assistant-header"><div class="assistant-icon">T</div><b>Tackyon AI Assistant</b></div>', unsafe_allow_html=True)
        st.markdown('<div class="assistant-body">', unsafe_allow_html=True)

        if "last_analysis" in st.session_state:
            for chat in st.session_state.chat_history:
                with st.chat_message(chat["role"]):
                    st.write(chat["content"])

            assistant_query = st.chat_input("Ask Tackyon...")

            if assistant_query:
                st.session_state.chat_history.append({"role": "user", "content": assistant_query})

                with st.chat_message("user"):
                    st.write(assistant_query)

                with st.chat_message("assistant"):
                    response = run_tackyon_assistant(
                        assistant_query,
                        st.session_state.last_analysis,
                        "English"
                    )
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
        else:
            st.caption("Generate a report first.")

        st.markdown('</div>', unsafe_allow_html=True)
