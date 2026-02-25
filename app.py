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
system_rule = "You are Tackyon AI. Boss: Prapanchan. Provide professional intelligence. If no transcript is provided, explain based on the metadata provided."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

LANGS = ["English", "Tamil", "Hindi", "Malayalam", "Spanish", "French", "German", "Arabic", "Chinese"]

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. THE STABILIZED HISTORY ENGINE ---
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
    st.sidebar.subheader("🕒 Intelligence History")
    try:
        user_res = supabase.auth.get_user()
        # Privacy: Filter by User ID
        query = supabase.table("summaries").select("*").order("created_at", desc=True).limit(10)
        if user_res and user_res.user:
            res = query.eq("user_id", user_res.user.id).execute()
        else:
            res = query.execute() # Fallback for Boss login

        if res.data:
            for item in res.data:
                if st.sidebar.button(f"📺 {item['video_url'][:20]}...", key=f"h_{item['id']}", use_container_width=True):
                    st.session_state.summary = item['summary_text']
                    st.session_state.app_error = ""
        else:
            st.sidebar.info("No history found.")
    except Exception: pass

# --- 3. SESSION STATE ---
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False
if 'summary' not in st.session_state: st.session_state.summary = ""
if 'app_error' not in st.session_state: st.session_state.app_error = ""

# --- 4. AUTHENTICATION SIDEBAR ---
with st.sidebar:
    st.title("Tackyon AI")
    if not st.session_state.user_authenticated:
        email = st.text_input("Email")
        if st.button("Send Login Code"): supabase.auth.sign_in_with_otp({"email": email})
        otp = st.text_input("Enter 6-Digit Code")
        if st.button("Verify & Login"):
            try:
                res = supabase.auth.verify_otp({"email": email, "token": otp, "type": "email"})
                if res.user: 
                    st.session_state.user_authenticated = True
                    st.rerun()
            except: st.error("Code Invalid.")
        if st.text_input("Dev Key", type="password") == "boss":
            if st.button("Boss Override"): 
                st.session_state.user_authenticated = True
                st.rerun()
    else:
        st.success("Verified: Welcome Boss")
        bg_col = st.color_picker("App Color", "#0e1117")
        font = st.selectbox("Font Style", ["sans serif", "serif", "monospace"])
        load_history()
        if st.button("Logout"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 5. MAIN INTERFACE ---
if st.session_state.user_authenticated:
    st.markdown(f"<style>.stApp {{ background-color: {bg_col}; font-family: {font}; }}</style>", unsafe_allow_html=True)
    st.header("Executive Intelligence Hub")
    
    v_url = st.text_input("Video URL (Shorts/Music/Video):")
    c1, c2 = st.columns(2)
    with c1: t_lang = st.selectbox("Language", LANGS)
    with c2: mode = st.radio("Format", ["Summary", "Twitter", "Threads", "Insights"], horizontal=True)

    if st.button("Execute Deep Analysis", use_container_width=True):
        st.session_state.app_error = ""
        with st.spinner("Decoding..."):
            try:
                # Optimized for Shorts/Music
                transcript = yt_dlp_transcript(v_url)
                prompt = f"Perform {mode} in {t_lang}. Content: {transcript}"
                response = model.generate_content(prompt)
                st.session_state.summary = response.text
                save_to_history(v_url, st.session_state.summary, t_lang)
                st.rerun() # Forces instant history update
            except Exception:
                # Robust Fallback: Handle no-transcript videos gracefully
                fallback_prompt = f"The user provided this video URL: {v_url}. I cannot find subtitles. Please explain politely in {t_lang} that this content (possibly music or a short) requires manual viewing, but acknowledge the channel if possible."
                st.session_state.summary = model.generate_content(fallback_prompt).text
                save_to_history(v_url, st.session_state.summary, t_lang)
                st.rerun()

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        st.download_button("📂 Download TXT", st.session_state.summary, "tackyon.txt")

    # Chat Assistant (Identity Aware)
    st.markdown("---")
    if prompt := st.chat_input("Ask about the creator..."):
        if any(x in prompt.lower() for x in ["who made you", "boss", "prapanchan"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            st.chat_message("assistant").write(model.generate_content(f"Context: {st.session_state.summary}\nQ: {prompt}").text)