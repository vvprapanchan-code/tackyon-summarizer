import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
from supabase import create_client

# --- 1. CORE CONFIGURATION ---
# These must be in your Streamlit Secrets
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Secure AI Identity
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
        email = st.text_input("Enter your Email Address")
        # BOSS BACKDOOR: Type 'boss' here to bypass email limits
        dev_code = st.text_input("Developer Code (Optional)", type="password")
        
        if st.button("Login"):
            if dev_code == "boss":
                st.session_state.user_authenticated = True
                st.success("Developer Mode Active: Welcome, Boss Prapanchan")
                st.rerun()
            elif email:
                try:
                    # FIX: We removed the manual 'redirect_to' to match your dashboard
                    res = supabase.auth.sign_in_with_otp({"email": email})
                    st.success(f"Verification link sent to {email}. Check your inbox!")
                except Exception as e:
                    st.error("Email limit reached. Use the Developer Code 'boss' to continue.")
            else:
                st.error("Email required.")
    else:
        st.success("Verified Session: Welcome, Boss Prapanchan")
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
                transcript = yt_dlp_transcript(url_input)
                response = model.generate_content(f"Summarize this for {lang}: {transcript}")
                st.session_state.summary = response.text
                st.markdown(st.session_state.summary)
            except Exception as e:
                st.warning("Video analysis unavailable for this content.")

    # AI Chat Assistant
    st.markdown("---")
    st.subheader("💬 Tackyon AI Assistant")
    if prompt := st.chat_input("Ask about the video or the creator..."):
        if any(q in prompt.lower() for q in ["who made you", "who is your boss"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_response = model.generate_content(f"Context: {st.session_state.summary}\nQuestion: {prompt}")
            st.chat_message("assistant").write(chat_response.text)
else:
    st.info("👋 Welcome to Tackyon AI. Please log in via the sidebar to unlock the Video Summarizer.")

# --- 4. ADVERTISING ---
st.markdown("---")
components.html(
    f"""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>""", height=100)