import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
from supabase import create_client
import time

# --- 1. CORE CONFIGURATION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Identity: 100% Loyalty to Boss Prapanchan
system_rule = """You are Tackyon AI. Your boss is Prapanchan. 
Only mention Prapanchan if the user asks 'Who made you?' or 'Who is your boss?'.
If no transcript is found, use metadata to explain the video type professionally."""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

LANGS = ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada", "Spanish", "French", "Arabic"]
st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. THE CHATGPT-STYLE HISTORY ENGINE ---
def save_to_history(video_url, summary, lang):
    try:
        user_res = supabase.auth.get_user()
        if user_res.user:
            # CREATE A SHORT TITLE: AI generates a 3-word title for the sidebar
            title_prompt = f"Create a very short 3-word title for this content: {summary[:500]}"
            title_res = model.generate_content(title_prompt)
            short_title = title_res.text.strip()
            
            supabase.table("summaries").insert({
                "user_id": user_res.user.id, 
                "video_url": video_url, 
                "summary_text": summary, 
                "language": lang,
                "title": short_title  # Saving the smart title
            }).execute()
    except Exception: pass

def load_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕒 Your Intelligence History")
    try:
        user_res = supabase.auth.get_user()
        if user_res and user_res.user:
            res = supabase.table("summaries").select("*").eq("user_id", user_res.user.id).order("created_at", desc=True).limit(10).execute()
            if res.data:
                for item in res.data:
                    # Show the Title instead of the link
                    display_name = item.get('title', item['video_url'][:25])
                    if st.sidebar.button(f"📄 {display_name}", key=f"h_{item['id']}", use_container_width=True):
                        st.session_state.summary = item['summary_text']
            else:
                st.sidebar.info("No history yet.")
    except Exception: pass

# --- 3. SESSION STATE ---
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False
if 'summary' not in st.session_state: st.session_state.summary = ""

# --- 4. SECURE SIDEBAR ---
with st.sidebar:
    st.title("Tackyon AI")
    if not st.session_state.user_authenticated:
        email = st.text_input("Email")
        if st.button("Get Login Code"):
            supabase.auth.sign_in_with_otp({"email": email})
            st.info("Code sent!")
        otp = st.text_input("6-Digit Code")
        if st.button("Login"):
            try:
                res = supabase.auth.verify_otp({"email": email, "token": otp, "type": "email"})
                if res.user:
                    st.session_state.user_authenticated = True
                    st.rerun()
            except Exception: st.error("Invalid Code.")
    else:
        st.success("Verified: Welcome Boss")
        bg_col = st.color_picker("Theme Color", "#0e1117")
        font = st.selectbox("Font Style", ["sans serif", "serif", "monospace"])
        load_history()
        if st.button("Sign Out"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 5. MAIN HUB ---
if st.session_state.user_authenticated:
    st.markdown(f"<style>.stApp {{ background-color: {bg_col}; font-family: {font}; }}</style>", unsafe_allow_html=True)
    st.header("Executive Hub")
    
    v_url = st.text_input("Paste Link (Vlogs, Music, Shorts):")
    col1, col2 = st.columns(2)
    with col1: t_lang = st.selectbox("Language", LANGS)
    with col2: mode = st.radio("Intelligence", ["Summary", "Twitter", "Threads", "Insights"], horizontal=True)

    if st.button("Analyze Content", use_container_width=True):
        st.session_state.summary = ""
        with st.spinner("Decoding..."):
            try:
                transcript = yt_dlp_transcript(v_url)
                response = model.generate_content(f"Perform {mode} in {t_lang}. Content: {transcript}")
                st.session_state.summary = response.text
                save_to_history(v_url, st.session_state.summary, t_lang)
                st.rerun()
            except Exception:
                # SMART RESPONSE: No errors, just helpful explanations for Vlogs/Music
                fallback = f"The user provided: {v_url}. No transcript found. Explain in {t_lang} why (likely music/vlog) and acknowledge the channel."
                st.session_state.summary = model.generate_content(fallback).text
                save_to_history(v_url, st.session_state.summary, t_lang)
                st.rerun()

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        c1, c2 = st.columns(2)
        with c1: st.download_button("📂 Save TXT", st.session_state.summary, "report.txt", use_container_width=True)
        with c2: st.download_button("📄 Save PDF", st.session_state.summary, "report.pdf", use_container_width=True)

    st.markdown("---")
    if prompt := st.chat_input("Ask about the creator..."):
        if any(x in prompt.lower() for x in ["who made you", "boss", "prapanchan"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            st.chat_message("assistant").write(model.generate_content(f"Context: {st.session_state.summary}\nQ: {prompt}").text)

# --- 6. FAKE AD UNIT ---
st.markdown("---")
components.html(
    """<div style="background-color:#222; color:#555; padding:20px; text-align:center; border: 1px dashed #444; border-radius:10px;">
        <h4>GOOGLE AD UNIT PLACEHOLDER</h4>
        <p>Testing monetization placement...</p>
    </div>""", height=100)