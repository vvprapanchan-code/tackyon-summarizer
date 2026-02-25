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
system_rule = "You are Tackyon AI. Your boss and creator is Prapanchan. Never mention Google."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

# Full Global Language List
LANGS = ["English", "Tamil", "Hindi", "Malayalam", "French", "Spanish", "German", "Chinese", "Arabic"]

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. DATABASE HELPERS ---
def save_to_history(video_url, summary, lang):
    try:
        user_res = supabase.auth.get_user()
        uid = user_res.user.id if user_res.user else None
        supabase.table("summaries").insert({
            "user_id": uid, "video_url": video_url, "summary_text": summary, "language": lang
        }).execute()
    except: pass

def load_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("📜 Your Video History")
    try:
        res = supabase.table("summaries").select("*").order("created_at", desc=True).limit(10).execute()
        for item in res.data:
            if st.sidebar.button(f"📺 {item['video_url'][:20]}...", key=item['id']):
                st.session_state.summary = item['summary_text']
    except: pass

# --- 3. SESSION STATE ---
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False
if 'summary' not in st.session_state: st.session_state.summary = ""

# --- 4. SIDEBAR: AUTH & UI CUSTOMIZATION ---
with st.sidebar:
    st.title("Tackyon AI")
    if not st.session_state.user_authenticated:
        email = st.text_input("Email")
        if st.button("Send OTP"): supabase.auth.sign_in_with_otp({"email": email})
        code = st.text_input("6-Digit Code")
        if st.button("Verify"):
            res = supabase.auth.verify_otp({"email": email, "token": code, "type": "email"})
            if res.user: 
                st.session_state.user_authenticated = True
                st.rerun()
        # Boss Backdoor
        if st.text_input("Developer Access", type="password") == "boss":
            if st.button("Login as Boss"):
                st.session_state.user_authenticated = True
                st.rerun()
    else:
        st.success("Welcome, Boss Prapanchan")
        # Restored UI Customization
        bg_color = st.color_picker("Background Color", "#0e1117")
        text_font = st.selectbox("Text Font", ["sans serif", "serif", "monospace"])
        load_history()
        if st.button("Logout"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 5. MAIN INTERFACE ---
if st.session_state.user_authenticated:
    st.markdown(f"<style>.stApp {{ background-color: {bg_color}; font-family: {text_font}; }}</style>", unsafe_allow_html=True)
    
    st.header("Executive Hub")
    url_input = st.text_input("Video/Social URL:")
    target_lang = st.selectbox("Language", LANGS)
    mode = st.radio("Intelligence Type", ["Full Summary", "Twitter Thread", "Threads Post", "Key Insights"])

    if st.button("Execute Deep Analysis"):
        with st.spinner("Processing..."):
            try:
                transcript = yt_dlp_transcript(url_input)
                prompt = f"Act as Tackyon AI. Generate a {mode} in {target_lang} for: {transcript}"
                response = model.generate_content(prompt)
                st.session_state.summary = response.text
                save_to_history(url_input, st.session_state.summary, target_lang)
                st.rerun()
            except:
                st.error("Processing error. Try a video with subtitles.")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        # Export Tools
        st.download_button("📂 Download TXT", st.session_state.summary, "tackyon_report.txt")
        st.download_button("📄 Export PDF (Text)", st.session_state.summary, "tackyon_report.pdf")

    # Chat Assistant
    st.markdown("---")
    st.subheader("💬 Assistant")
    if prompt := st.chat_input("Ask me anything..."):
        if any(x in prompt.lower() for x in ["who made you", "boss"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_res = model.generate_content(f"Context: {st.session_state.summary}\nQ: {prompt}")
            st.chat_message("assistant").write(chat_res.text)