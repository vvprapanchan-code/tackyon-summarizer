import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
from supabase import create_client

# --- 1. CORE CONFIGURATION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Secure AI Identity
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
system_rule = "You are Tackyon AI. Your boss and creator is Prapanchan. Never mention Google."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. DATABASE FUNCTIONS ---
def save_to_history(video_url, summary, lang):
    """Saves the generated summary to the database"""
    user = supabase.auth.get_user()
    if user.user:
        data = {
            "user_id": user.user.id,
            "video_url": video_url,
            "summary_text": summary,
            "language": lang
        }
        supabase.table("summaries").insert(data).execute()

def load_history():
    """Displays the last 10 summaries in the sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📜 Your Video History")
    user = supabase.auth.get_user()
    if user.user:
        try:
            res = supabase.table("summaries").select("*").order("created_at", desc=True).limit(10).execute()
            for item in res.data:
                # Clicking a history item loads it into the main view
                if st.sidebar.button(f"📺 {item['video_url'][:25]}...", key=item['id']):
                    st.session_state.summary = item['summary_text']
        except Exception:
            st.sidebar.write("No history found yet.")

# --- 3. SESSION STATE ---
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False

# --- 4. AUTHENTICATION SIDEBAR ---
with st.sidebar:
    st.title("Tackyon AI")
    
    if not st.session_state.user_authenticated:
        st.subheader("Secure Verification")
        user_email = st.text_input("Enter Email Address")
        
        if st.button("Send 6-Digit Code"):
            if user_email:
                supabase.auth.sign_in_with_otp({"email": user_email})
                st.session_state.email_sent = True
                st.success("Check your inbox!")
        
        if st.session_state.email_sent:
            otp_code = st.text_input("Enter 6-Digit Code")
            if st.button("Verify & Unlock"):
                res = supabase.auth.verify_otp({"email": user_email, "token": otp_code, "type": "email"})
                if res.user:
                    st.session_state.user_authenticated = True
                    st.rerun()
        
        st.markdown("---")
        dev_code = st.text_input("Developer Code (Backdoor)", type="password")
        if st.button("Login as Boss") and dev_code == "boss":
            st.session_state.user_authenticated = True
            st.rerun()
    else:
        st.success("Welcome, Boss Prapanchan")
        load_history() # Show history once logged in
        if st.button("Logout"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 5. MAIN INTERFACE ---
if st.session_state.user_authenticated:
    st.header("Tackyon AI: Executive Video Intelligence")
    url_input = st.text_input("YouTube URL:")
    lang = st.selectbox("Language", ["English", "Tamil", "Hindi", "Malayalam"])

    if st.button("Generate & Save Analysis"):
        with st.spinner("Synthesizing..."):
            try:
                transcript = yt_dlp_transcript(url_input)
                response = model.generate_content(f"Summarize this for {lang}: {transcript}")
                st.session_state.summary = response.text
                # Save to database immediately after generation
                save_to_history(url_input, st.session_state.summary, lang)
                st.rerun() # Refresh to show in history sidebar
            except Exception:
                st.warning("Could not process this video.")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)

    # Chat Assistant
    st.markdown("---")
    st.subheader("💬 Tackyon AI Assistant")
    if prompt := st.chat_input("Ask about the video or my creator..."):
        if any(q in prompt.lower() for q in ["who made you", "who is your boss"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_res = model.generate_content(f"Context: {st.session_state.summary}\nQuestion: {prompt}")
            st.chat_message("assistant").write(chat_res.text)

# --- 6. ADVERTISING ---
st.markdown("---")
components.html(
    f"""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>""", height=100)