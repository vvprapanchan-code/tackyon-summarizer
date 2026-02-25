import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
from supabase import create_client

# --- 1. CORE CONFIGURATION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
system_rule = "You are Tackyon AI. Boss: Prapanchan. Never mention creator in summaries."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

LANGS = ["English", "Tamil", "Hindi", "Malayalam", "Spanish", "French", "Arabic"]
st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. SECURE DATABASE HELPERS ---
def save_to_history(video_url, summary, lang):
    try:
        user_res = supabase.auth.get_user()
        if user_res.user:
            # Explicitly link to the current User ID for privacy
            supabase.table("summaries").insert({
                "user_id": user_res.user.id, 
                "video_url": video_url, 
                "summary_text": summary, 
                "language": lang
            }).execute()
    except Exception: pass

def load_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕒 Your Secure History")
    try:
        user_res = supabase.auth.get_user()
        if user_res.user:
            # Filter history so users ONLY see their own data
            res = supabase.table("summaries").select("*").eq("user_id", user_res.user.id).order("created_at", desc=True).limit(10).execute()
            if res.data:
                for item in res.data:
                    if st.sidebar.button(f"📄 {item['video_url'][:20]}...", key=item['id'], use_container_width=True):
                        st.session_state.summary = item['summary_text']
            else:
                st.sidebar.info("No personal history yet.")
    except Exception: pass

# --- 3. SESSION STATE ---
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False
if 'summary' not in st.session_state: st.session_state.summary = ""

# --- 4. SIDEBAR: AUTH & UI ---
with st.sidebar:
    st.title("Tackyon AI")
    if not st.session_state.user_authenticated:
        email = st.text_input("User Email")
        if st.button("Get OTP Code"):
            supabase.auth.sign_in_with_otp({"email": email})
            st.info("Code sent to your email.")
        
        otp_input = st.text_input("6-Digit Code")
        if st.button("Verify & Login"):
            try:
                # Fixed OTP verification to prevent AuthApiError
                res = supabase.auth.verify_otp({"email": email, "token": otp_input, "type": "email"})
                if res.user:
                    st.session_state.user_authenticated = True
                    st.rerun()
            except Exception:
                st.error("Invalid or expired code. Please try again.")
        
        if st.text_input("Developer Key", type="password") == "boss":
            if st.button("Boss Override"):
                st.session_state.user_authenticated = True
                st.rerun()
    else:
        st.success("Verified Session")
        bg_color = st.color_picker("App Theme", "#0e1117")
        text_font = st.selectbox("Typography", ["sans serif", "serif", "monospace"])
        load_history() # Securely loads ONLY the user's history
        if st.button("Sign Out"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 5. MAIN INTERFACE ---
if st.session_state.user_authenticated:
    st.markdown(f"<style>.stApp {{ background-color: {bg_color}; font-family: {text_font}; }}</style>", unsafe_allow_html=True)
    st.header("Tackyon Executive Hub")
    
    url_input = st.text_input("Video URL:")
    col1, col2 = st.columns(2)
    with col1: target_lang = st.selectbox("Language", LANGS)
    with col2: mode = st.radio("Style", ["Summary", "Twitter", "Threads", "Insights"], horizontal=True)

    if st.button("Run Deep Analysis", use_container_width=True):
        with st.spinner("Analyzing..."):
            try:
                transcript = yt_dlp_transcript(url_input)
                response = model.generate_content(f"Format: {mode}. Language: {target_lang}. Content: {transcript}")
                st.session_state.summary = response.text
                save_to_history(url_input, st.session_state.summary, target_lang)
                st.rerun()
            except Exception:
                st.error("Processing failed. Check if video has subtitles.")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        st.download_button("📂 Save TXT", st.session_state.summary, "tackyon.txt")

    # Identity Chat
    st.markdown("---")
    if prompt := st.chat_input("Ask about the creator..."):
        if any(x in prompt.lower() for x in ["who made you", "boss", "prapanchan"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_res = model.generate_content(f"Context: {st.session_state.summary}\nQ: {prompt}")
            st.chat_message("assistant").write(chat_res.text)