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
# AI Identity: Only reveals Boss Prapanchan when asked
system_rule = """You are Tackyon AI. Your boss is Prapanchan. 
Start all summaries immediately without introductions. 
Only mention Prapanchan if the user asks 'Who made you?' or 'Who is your boss?'."""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

# --- 2. THE COMPLETE FEATURE LIST ---
# Restoration of your global language database
LANGS = [
    "English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada", 
    "Spanish", "French", "German", "Chinese", "Japanese", "Arabic"
]

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 3. DATABASE & HISTORY (ChatGPT STYLE) ---
def save_to_history(video_url, summary, lang):
    try:
        user_res = supabase.auth.get_user()
        uid = user_res.user.id if user_res and user_res.user else None
        supabase.table("summaries").insert({
            "user_id": uid, "video_url": video_url, "summary_text": summary, "language": lang
        }).execute()
    except: pass

def load_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕒 Previous Intelligence")
    try:
        # Fetches the last 10 sessions from your database
        res = supabase.table("summaries").select("*").order("created_at", desc=True).limit(10).execute()
        if res.data:
            for item in res.data:
                # Clicking a button loads the old summary instantly
                if st.sidebar.button(f"📄 {item['video_url'][:20]}...", key=item['id'], use_container_width=True):
                    st.session_state.summary = item['summary_text']
        else:
            st.sidebar.info("No history yet. Start a search!")
    except:
        st.sidebar.error("History offline.")

# --- 4. SESSION STATE ---
if 'user_authenticated' not in st.session_state: st.session_state.user_authenticated = False
if 'summary' not in st.session_state: st.session_state.summary = ""

# --- 5. THE SIDEBAR (AUTH & DESIGN) ---
with st.sidebar:
    st.title("Tackyon AI")
    if not st.session_state.user_authenticated:
        st.subheader("Boss Login")
        email = st.text_input("Email")
        if st.button("Request OTP"): supabase.auth.sign_in_with_otp({"email": email})
        code = st.text_input("Enter 6-Digit Code")
        if st.button("Verify & Enter"):
            res = supabase.auth.verify_otp({"email": email, "token": code, "type": "email"})
            if res.user: 
                st.session_state.user_authenticated = True
                st.rerun()
        # Backdoor for Prapanchan
        if st.text_input("Developer Code", type="password") == "boss":
            if st.button("Login as Boss"):
                st.session_state.user_authenticated = True
                st.rerun()
    else:
        st.success("Identity Verified: Prapanchan")
        # RESTORED: Professional UI Control
        bg_color = st.color_picker("Theme Color", "#0e1117")
        text_font = st.selectbox("Interface Font", ["sans serif", "serif", "monospace"])
        load_history() # History persistent sidebar
        if st.button("Sign Out"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 6. MAIN INTELLIGENCE HUB ---
if st.session_state.user_authenticated:
    # Applying the Boss's Custom UI
    st.markdown(f"<style>.stApp {{ background-color: {bg_color}; font-family: {text_font}; }}</style>", unsafe_allow_html=True)
    
    st.header("Executive Hub")
    url_input = st.text_input("YouTube / Social Media URL:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        target_lang = st.selectbox("Global Language", LANGS)
    with col_b:
        # RESTORED: Multi-Platform Analysis
        mode = st.radio("Output Format", ["Full Summary", "Twitter Thread", "Threads Post", "Key Insights"], horizontal=True)

    if st.button("Execute Deep Analysis", use_container_width=True):
        with st.spinner("Decoding Intelligence..."):
            try:
                transcript = yt_dlp_transcript(url_input)
                prompt = f"Perform a {mode} in {target_lang}. Be direct and professional. Content: {transcript}"
                response = model.generate_content(prompt)
                st.session_state.summary = response.text
                save_to_history(url_input, st.session_state.summary, target_lang) # Auto-save
                st.rerun()
            except:
                st.error("Processing error. Ensure the video has subtitles.")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        # RESTORED: Export Tools
        c1, c2 = st.columns(2)
        with c1: st.download_button("📂 Download TXT", st.session_state.summary, "tackyon_report.txt", use_container_width=True)
        with c2: st.download_button("📄 Export PDF", st.session_state.summary, "tackyon_report.pdf", use_container_width=True)

    # Chat Assistant (Identity-Aware)
    st.markdown("---")
    st.subheader("💬 Executive Assistant")
    if prompt := st.chat_input("Analyze further or ask about my creator..."):
        if any(x in prompt.lower() for x in ["who made you", "boss", "prapanchan"]):
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_res = model.generate_content(f"Context: {st.session_state.summary}\nQ: {prompt}")
            st.chat_message("assistant").write(chat_res.text)

# --- 7. REVENUE ---
st.markdown("---")
components.html(
    f"""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>""", height=100)