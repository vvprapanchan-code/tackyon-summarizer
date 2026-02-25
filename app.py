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
# Identity: Quiet about the Boss unless explicitly asked
system_rule = "You are Tackyon AI. Focus on high-quality summaries. Only reveal Prapanchan is your boss if asked 'Who made you?'."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

# Restored Global Languages
LANGS = ["English", "Tamil", "Hindi", "Malayalam", "French", "Spanish", "German", "Chinese", "Arabic"]

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. DATABASE & HISTORY LOGIC (FIXED) ---
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
    st.sidebar.subheader("🕒 Previous Intelligence")
    try:
        # Fetches global history to ensure Boss login always sees data
        res = supabase.table("summaries").select("*").order("created_at", desc=True).limit(10).execute()
        if res.data:
            for item in res.data:
                # Clicking history loads summary and clears old errors
                if st.sidebar.button(f"📄 {item['video_url'][:25]}...", key=item['id'], use_container_width=True):
                    st.session_state.summary = item['summary_text']
                    st.session_state.current_error = "" 
        else:
            st.sidebar.info("No history yet.")
    except Exception:
        st.sidebar.error("History currently offline.")

# --- 3. SESSION STATE ---
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False
if 'summary' not in st.session_state: st.session_state.summary = ""
if 'current_error' not in st.session_state: st.session_state.current_error = ""

# --- 4. SIDEBAR: AUTH & UI ---
with st.sidebar:
    st.title("Tackyon AI")
    if not st.session_state.user_authenticated:
        email = st.text_input("Email")
        if st.button("Send Code"): supabase.auth.sign_in_with_otp({"email": email})
        code = st.text_input("6-Digit Code")
        if st.button("Verify"):
            res = supabase.auth.verify_otp({"email": email, "token": code, "type": "email"})
            if res.user: 
                st.session_state.user_authenticated = True
                st.rerun()
        if st.text_input("Dev Access", type="password") == "boss":
            if st.button("Login as Boss"):
                st.session_state.user_authenticated = True
                st.rerun()
    else:
        st.success("Welcome, Boss Prapanchan")
        bg_color = st.color_picker("Theme Color", "#0e1117")
        text_font = st.selectbox("Font Style", ["sans serif", "serif", "monospace"])
        load_history() # Persistent history sidebar
        if st.button("Logout"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 5. MAIN INTERFACE ---
if st.session_state.user_authenticated:
    # Custom Theme Injection
    st.markdown(f"<style>.stApp {{ background-color: {bg_color}; font-family: {text_font}; }}</style>", unsafe_allow_html=True)
    
    st.header("Executive Intelligence Hub")
    url_input = st.text_input("Video/Social URL:")
    
    col1, col2 = st.columns(2)
    with col1: target_lang = st.selectbox("Language", LANGS)
    with col2: mode = st.radio("Output", ["Summary", "Twitter Thread", "Threads", "Insights"], horizontal=True)

    if st.button("Analyze Content", use_container_width=True):
        st.session_state.current_error = "" # CLEAR ERROR IMMEDIATELY
        st.session_state.summary = ""
        with st.spinner("Decoding..."):
            try:
                transcript = yt_dlp_transcript(url_input)
                prompt = f"Provide a {mode} in {target_lang}. Start immediately. Content: {transcript}"
                response = model.generate_content(prompt)
                st.session_state.summary = response.text
                save_to_history(url_input, st.session_state.summary, target_lang) # Auto-save
                st.rerun() # Refresh to update history sidebar
            except Exception:
                st.session_state.current_error = "Processing error. Ensure subtitles are available."

    # Only show error if analysis actually failed
    if st.session_state.current_error:
        st.error(st.session_state.current_error)

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        # Export Tools
        c1, c2 = st.columns(2)
        with c1: st.download_button("📂 Download TXT", st.session_state.summary, "report.txt", use_container_width=True)
        with c2: st.download_button("📄 Export PDF", st.session_state.summary, "report.pdf", use_container_width=True)

    # Chat Assistant (Boss-Loyal)
    st.markdown("---")
    st.subheader("💬 Assistant")
    if prompt := st.chat_input("Ask about the video or my creator..."):
        if any(x in prompt.lower() for x in ["who made you", "boss", "prapanchan"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_res = model.generate_content(f"Context: {st.session_state.summary}\nQ: {prompt}")
            st.chat_message("assistant").write(chat_res.text)

# --- 6. REVENUE ---
st.markdown("---")
components.html(
    f"""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>""", height=100)