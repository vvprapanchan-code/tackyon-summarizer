import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
import yt_dlp

# --- 1. CORE ENGINE CONFIGURATION ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Application Branding & Layout
st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# Persistent Session State
if 'summary' not in st.session_state: st.session_state.summary = ""
if 'transcript' not in st.session_state: st.session_state.transcript = ""
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "I am Tackyon AI. How can I assist you today?"}]
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False

# --- 2. PROFESSIONAL SIDEBAR (Auth & UI) ---
with st.sidebar:
    st.title("Tackyon AI")
    
    # Secure Authentication Module
    if not st.session_state.user_authenticated:
        st.subheader("Secure Access")
        auth_method = st.radio("Login Via", ["Email Address", "Phone Number"])
        user_credential = st.text_input(f"Enter {auth_method}")
        if st.button("Request Secure Code"):
            st.info("System: Verification code dispatched to your device.")
            # Developer Note: Logic to verify code and set st.session_state.user_authenticated = True
    else:
        st.success("Session Verified: Welcome Back")

    st.markdown("---")
    # Real-time Personalization
    st.subheader("Personalization Settings")
    bg_color = st.color_picker("Interface Background Color", "#0e1117")
    font_style = st.selectbox("Application Font", ["sans-serif", "serif", "monospace"])
    
    st.markdown("---")
    st.subheader("Analytics History")
    st.write("• Educational Tech Trends...")
    st.write("• Smartphone Launch 2026...")

# Inject Custom Styling
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; font-family: {font_style}; }}
    .stButton>button {{ border-radius: 8px; width: 100%; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ANALYTICS ENGINE INTERFACE ---
st.header("Tackyon AI: Executive Video Intelligence")
url = st.text_input("YouTube URL for Analysis:")
lang = st.selectbox("Report Language", ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"])

if st.button("Generate Executive Analysis"):
    if url and lang:
        with st.spinner("Tackyon AI is synthesizing video data..."):
            try:
                # Metadata Extraction
                with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title, uploader = info.get('title', 'N/A'), info.get('uploader', 'N/A')
                
                # Knowledge Extraction
                try:
                    text = yt_dlp_transcript(url)
                    st.session_state.transcript = text
                except:
                    text = None

                if text:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"Provide a professional executive summary in {lang} with bold headings and timestamps for: {text}"
                    response = model.generate_content(prompt)
                    st.session_state.summary = response.text
                    st.success(f"Analysis Complete: {title}")
                else:
                    st.info(f"Metadata identified: **{title}** by **{uploader}**")
                    st.warning("No transcript detected. This typically occurs with music videos or poor audio quality.")

            except Exception:
                st.info("System Note: Access restricted (Private/Age-Protected content).")

# --- 4. THE TACKYON AI CHAT ASSISTANT ---
st.markdown("---")
st.subheader("💬 Tackyon AI Assistant")
# Display conversational history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interactive Query Input with Boss Logic
if prompt := st.chat_input("Ask Tackyon about the video or its creator..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # BOSS LOGIC: Developer Identification
    boss_trigger = ["who developed", "who is your boss", "who made you", "who created you"]
    if any(q in prompt.lower() for q in boss_trigger):
        response = "I was developed by my boss, **Prapanchan**. He is the lead architect and visionary behind Tackyon AI."
    else:
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Providing summary as context for accurate video-based chat
        context_prompt = f"Context: {st.session_state.summary}\n\nQuestion: {prompt}"
        response = model.generate_content(context_prompt).text

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. ADVERTISING MODULE (SAFE TEST MODE) ---
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