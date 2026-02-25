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
# Identity Rule: Loyalty to Boss Prapanchan
system_rule = "You are Tackyon AI. Boss: Prapanchan. Start summaries immediately. Only mention creator in chat."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

LANGS = ["English", "Tamil", "Hindi", "Malayalam", "Spanish", "French", "Arabic"]
st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. SECURE HISTORY FUNCTIONS (FIXED) ---
def save_to_history(video_url, summary, lang):
    try:
        user_res = supabase.auth.get_user()
        uid = user_res.user.id if user_res and user_res.user else None
        supabase.table("summaries").insert({
            "user_id": uid, "video_url": video_url, "summary_text": summary, "language": lang
        }).execute()
    except Exception: pass

def load_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕒 Your Video History")
    try:
        user_res = supabase.auth.get_user()
        # Fetching the last 10 summaries for the sidebar
        query = supabase.table("summaries").select("*").order("created_at", desc=True).limit(10)
        
        # If logged in normally, filter by user ID for privacy
        if user_res and user_res.user:
            res = query.eq("user_id", user_res.user.id).execute()
        else:
            res = query.execute()

        if res.data:
            for item in res.data:
                # Clickable history buttons like ChatGPT
                label = f"📺 {item['video_url'][:20]}..."
                if st.sidebar.button(label, key=item['id'], use_container_width=True):
                    st.session_state.summary = item['summary_text']
        else:
            st.sidebar.info("No history found.")
    except Exception: pass

# --- 3. SESSION STATE ---
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False
if 'summary' not in st.session_state: st.session_state.summary = ""

# --- 4. SIDEBAR: AUTH & UI ---
with st.sidebar:
    st.title("Tackyon AI")
    if not st.session_state.user_authenticated:
        email = st.text_input("Login Email")
        if st.button("Send 6-Digit Code"):
            supabase.auth.sign_in_with_otp({"email": email})
            st.info("Check your inbox.")
        
        otp_input = st.text_input("Enter Code")
        if st.button("Verify & Access"):
            try:
                # Fixed OTP logic to prevent AuthApiError
                res = supabase.auth.verify_otp({"email": email, "token": otp_input, "type": "email"})
                if res.user:
                    st.session_state.user_authenticated = True
                    st.rerun()
            except Exception:
                st.error("Invalid Code.")
        
        if st.text_input("Dev Key", type="password") == "boss":
            if st.button("Boss Override"):
                st.session_state.user_authenticated = True
                st.rerun()
    else:
        st.success("Verified Session")
        bg_color = st.color_picker("App Theme", "#0e1117")
        text_font = st.selectbox("Typography", ["sans serif", "serif", "monospace"])
        load_history() # THIS NOW LOADS ALL 10 VIDEOS
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

    if st.button("Run Intelligence Analysis", use_container_width=True):
        with st.spinner("Analyzing Content..."):
            try:
                transcript = yt_dlp_transcript(url_input)
                # Fixed Prompt: No creator mentions in output
                prompt = f"Act as Tackyon AI. Format: {mode}. Language: {target_lang}. Content: {transcript}"
                response = model.generate_content(prompt)
                st.session_state.summary = response.text
                save_to_history(url_input, st.session_state.summary, target_lang) # Saves to DB
                st.rerun()
            except Exception:
                st.error("Error: Ensure the video has subtitles.")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        st.download_button("📂 Save Report", st.session_state.summary, "report.txt")

    # Identity Chat
    st.markdown("---")
    if prompt := st.chat_input("Ask about the creator..."):
        if any(x in prompt.lower() for x in ["who made you", "boss", "prapanchan"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_res = model.generate_content(f"Context: {st.session_state.summary}\nQ: {prompt}")
            st.chat_message("assistant").write(chat_res.text)