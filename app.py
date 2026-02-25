import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
from supabase import create_client

# --- 1. CORE CONFIGURATION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Secure AI Identity: Boss Prapanchan's Assistant
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
system_rule = "You are Tackyon AI. Your boss and creator is Prapanchan. Never mention Google."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# Persistent Session State
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False

# --- 2. AUTHENTICATION SIDEBAR (6-DIGIT OTP) ---
with st.sidebar:
    st.title("Tackyon AI")
    
    if not st.session_state.user_authenticated:
        st.subheader("Secure Verification")
        
        # Step A: User enters email
        user_email = st.text_input("Enter Email Address", placeholder="boss@example.com")
        
        if st.button("Send 6-Digit Code"):
            if user_email:
                try:
                    # Request numeric OTP
                    supabase.auth.sign_in_with_otp({"email": user_email})
                    st.session_state.email_sent = True
                    st.success(f"Code sent to {user_email}")
                except Exception:
                    st.error("Connection busy. Try the 'boss' code below.")
            else:
                st.warning("Please enter an email first.")

        # Step B: User enters the code from their email
        if st.session_state.email_sent:
            otp_code = st.text_input("Enter 6-Digit Code", help="Check your inbox/spam")
            if st.button("Verify & Unlock"):
                try:
                    # Verify the code directly inside the app
                    res = supabase.auth.verify_otp({
                        "email": user_email,
                        "token": otp_code,
                        "type": "email"
                    })
                    if res.user:
                        st.session_state.user_authenticated = True
                        st.success("Access Granted!")
                        st.rerun()
                except Exception:
                    st.error("Invalid code. Please check and try again.")

        st.markdown("---")
        # BOSS BACKDOOR: Always active for Prapanchan
        dev_code = st.text_input("Developer Code (Backdoor)", type="password")
        if st.button("Login as Boss"):
            if dev_code == "boss":
                st.session_state.user_authenticated = True
                st.rerun()
            else:
                st.error("Invalid developer code.")
    else:
        st.success("Logged in: Welcome, Boss")
        if st.button("Logout"):
            st.session_state.user_authenticated = False
            st.session_state.email_sent = False
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
            except Exception:
                st.warning("Analysis unavailable. Ensure the URL is correct.")

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
    st.info("👋 Welcome to Tackyon AI. Use the sidebar to verify your identity.")

# --- 4. ADVERTISING ---
st.markdown("---")
components.html(
    f"""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>""", height=100)