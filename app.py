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
system_rule = "You are Tackyon AI. Boss: Prapanchan. Start summaries immediately. Only mention Prapanchan if asked in chat."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

LANGS = ["English", "Tamil", "Hindi", "Malayalam", "Spanish", "French", "Arabic"]
st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. THE CHATGPT-STYLE HISTORY ENGINE ---
def save_to_history(video_url, summary, lang):
    try:
        user_res = supabase.auth.get_user()
        if user_res.user:
            # Generate a 3-word title for the history list
            try:
                title_res = model.generate_content(f"Create a 3-word title for: {summary[:200]}")
                short_title = title_res.text.strip()
            except: short_title = "Video Analysis"
            
            supabase.table("summaries").insert({
                "user_id": user_res.user.id, "video_url": video_url, 
                "summary_text": summary, "language": lang, "title": short_title
            }).execute()
    except Exception: pass

def load_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕒 Your Intelligence History")
    try:
        user_res = supabase.auth.get_user()
        if user_res and user_res.user:
            # Strictly filter by logged-in User ID for privacy
            res = supabase.table("summaries").select("*").eq("user_id", user_res.user.id).order("created_at", desc=True).limit(10).execute()
            if res.data:
                for item in res.data:
                    # Show the Smart Title instead of the link
                    label = item.get('title') or "Video Summary"
                    if st.sidebar.button(f"📄 {label}", key=f"h_{item['id']}", use_container_width=True):
                        st.session_state.summary = item['summary_text']
            else:
                st.sidebar.info("No personal history found.")
    except Exception: pass

# --- 3. SESSION STATE ---
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False
if 'summary' not in st.session_state: st.session_state.summary = ""

# --- 4. SECURE SIDEBAR ---
with st.sidebar:
    st.title("Tackyon AI")
    if not st.session_state.user_authenticated:
        email = st.text_input("User Email")
        if st.button("Send Login Code"): supabase.auth.sign_in_with_otp({"email": email})
        otp = st.text_input("6-Digit Code")
        if st.button("Verify & Login"):
            try:
                res = supabase.auth.verify_otp({"email": email, "token": otp, "type": "email"})
                if res.user:
                    st.session_state.user_authenticated = True
                    st.rerun()
            except Exception: st.error("Code Invalid.")
    else:
        st.success("Verified: Welcome Boss")
        bg_col = st.color_picker("Theme Color", "#0e1117")
        font = st.selectbox("Font Style", ["sans serif", "serif", "monospace"])
        load_history() # LOADS HISTORY HERE
        if st.button("Sign Out"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 5. MAIN INTERFACE ---
if st.session_state.user_authenticated:
    st.markdown(f"<style>.stApp {{ background-color: {bg_col}; font-family: {font}; }}</style>", unsafe_allow_html=True)
    st.header("Executive Intelligence Hub")
    
    v_url = st.text_input("Paste YouTube Link:")
    col1, col2 = st.columns(2)
    with col1: t_lang = st.selectbox("Language", LANGS)
    with col2: mode = st.radio("Style", ["Summary", "Twitter", "Threads", "Insights"], horizontal=True)

    if st.button("Execute Deep Analysis", use_container_width=True):
        st.session_state.summary = ""
        with st.spinner("Decoding Intelligence..."):
            try:
                transcript = yt_dlp_transcript(v_url)
                response = model.generate_content(f"Perform {mode} in {t_lang}. Content: {transcript}")
                st.session_state.summary = response.text
                save_to_history(v_url, st.session_state.summary, t_lang)
                st.rerun() # Refresh to update history sidebar instantly
            except Exception as e:
                # Handle Quota / Resource Exhausted
                if "ResourceExhausted" in str(e) or "429" in str(e):
                    st.warning("Google is busy. Retrying in 5 seconds...")
                    time.sleep(5)
                    st.rerun()
                else:
                    # Smart Fallback for Vlogs/Music without subtitles
                    fb_prompt = f"No subtitles for {v_url}. Explain politely in {t_lang} that this is likely a vlog or song."
                    st.session_state.summary = model.generate_content(fb_prompt).text
                    save_to_history(v_url, st.session_state.summary, t_lang)
                    st.rerun()

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        st.download_button("📂 Save Report", st.session_state.summary, "tackyon.txt")

    # Chat Assistant (Identity Aware)
    st.markdown("---")
    if prompt := st.chat_input("Ask about the creator..."):
        if any(x in prompt.lower() for x in ["who made you", "boss", "prapanchan"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            try:
                chat_res = model.generate_content(f"Context: {st.session_state.summary}\nQ: {prompt}")
                st.chat_message("assistant").write(chat_res.text)
            except: st.error("AI Busy. Try again in 5 seconds.")

# --- 6. FAKE AD UNIT ---
st.markdown("---")
components.html(
    f"""<div style="background-color:#222; color:#555; padding:20px; text-align:center; border: 1px dashed #444; border-radius:10px;">
        <h4>MONETIZATION UNIT</h4>
        <p>Google Ad Placement Testing...</p>
    </div>""", height=100)