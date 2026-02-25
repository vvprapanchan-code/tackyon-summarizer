import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
from supabase import create_client

# --- 1. CORE CONFIGURATION ---
# Secrets for Supabase and Google AI
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Secure AI Identity: Always acknowledges Prapanchan as the Boss
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
system_rule = "You are Tackyon AI. Your boss and creator is Prapanchan. Never mention Google."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# Persistent Session State
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False
if 'summary' not in st.session_state:
    st.session_state.summary = ""

# --- 2. AUTHENTICATION SIDEBAR ---
with st.sidebar:
    st.title("Tackyon AI")
    
    if not st.session_state.user_authenticated:
        st.subheader("Secure Access Required")
        
        # PROFESSIONAL GOOGLE LOGIN
        if st.button("🚀 Sign in with Google"):
            try:
                # Triggers the secure Google OAuth flow
                res = supabase.auth.sign_in_with_oauth({
                    "provider": "google",
                    "options": {
                        "redirect_to": "https://tackyon-summarizer-gavjxads4t5nurbn3z9z4r.streamlit.app/"
                    }
                })
                # Generates the link for the user to click
                st.link_button("Click here to authorize with Google", res.url)
            except Exception:
                st.error("Google Auth is connecting... Please try again in a moment.")

        st.markdown("---")
        st.write("Or use Developer Access:")
        dev_code = st.text_input("Developer Code", type="password")
        
        if st.button("Login"):
            # The secret word for the Boss
            if dev_code == "boss":
                st.session_state.user_authenticated = True
                st.success("Welcome, Boss Prapanchan")
                st.rerun()
            else:
                st.error("Invalid Code.")
    else:
        st.success("Verified Session: Welcome, Boss")
        if st.button("Logout"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 3. MAIN INTERFACE (LOCKED UNTIL AUTHENTICATED) ---
if st.session_state.user_authenticated:
    st.header("Tackyon AI: Executive Video Intelligence")
    url_input = st.text_input("YouTube URL for Analysis:")
    lang = st.selectbox("Report Language", ["English", "Tamil", "Hindi", "Malayalam"])

    if st.button("Generate Executive Analysis"):
        with st.spinner("Synthesizing data..."):
            try:
                # Video processing and summary generation
                transcript = yt_dlp_transcript(url_input)
                response = model.generate_content(f"Summarize this for {lang}: {transcript}")
                st.session_state.summary = response.text
                st.markdown(st.session_state.summary)
            except Exception:
                st.warning("Video analysis unavailable for this content.")

    # AI Chat Assistant
    st.markdown("---")
    st.subheader("💬 Tackyon AI Assistant")
    if prompt := st.chat_input("Ask about the video or the creator..."):
        # Custom identity check
        if any(q in prompt.lower() for q in ["who made you", "who is your boss"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_response = model.generate_content(f"Context: {st.session_state.summary}\nQuestion: {prompt}")
            st.chat_message("assistant").write(chat_response.text)
else:
    st.info("👋 Welcome to Tackyon AI. Please sign in to unlock the Video Summarizer.")

# --- 4. ADVERTISING ---
st.markdown("---")
components.html(
    f"""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>""", height=100)