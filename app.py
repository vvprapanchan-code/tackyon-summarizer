import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
from supabase import create_client
import io

# --- 1. CORE CONFIGURATION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
system_rule = "You are Tackyon AI. Your boss and creator is Prapanchan. Never mention Google."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_rule)

# --- 2. RESTORED GLOBAL LANGUAGES ---
LANGUAGES = ["English", "Tamil", "Hindi", "Malayalam", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Arabic", "Russian"]

# --- 3. DATABASE & UI LOGIC ---
def save_to_history(video_url, summary, lang):
    try:
        user_res = supabase.auth.get_user()
        uid = user_res.user.id if user_res and user_res.user else None
        data = {"user_id": uid, "video_url": video_url, "summary_text": summary, "language": lang}
        supabase.table("summaries").insert(data).execute()
    except Exception: pass

def load_history():
    st.sidebar.markdown("---")
    st.sidebar.subheader("📜 Your Video History")
    try:
        res = supabase.table("summaries").select("*").order("created_at", desc=True).limit(10).execute()
        if res.data:
            for item in res.data:
                if st.sidebar.button(f"📺 {item['video_url'][:20]}...", key=item['id']):
                    st.session_state.summary = item['summary_text']
    except Exception: pass

# --- 4. UI SETUP ---
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False
if 'summary' not in st.session_state:
    st.session_state.summary = ""

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 5. SIDEBAR: AUTH & CUSTOMIZATION ---
with st.sidebar:
    st.title("Tackyon AI")
    
    if not st.session_state.user_authenticated:
        # (Verification Logic Kept for Security)
        user_email = st.text_input("Enter Email Address")
        if st.button("Send 6-Digit Code"):
            supabase.auth.sign_in_with_otp({"email": user_email})
            st.success("Check your inbox!")
        
        otp_code = st.text_input("Enter Code")
        if st.button("Verify"):
            res = supabase.auth.verify_otp({"email": user_email, "token": otp_code, "type": "email"})
            if res.user: 
                st.session_state.user_authenticated = True
                st.rerun()
        
        st.markdown("---")
        if st.text_input("Boss Code", type="password") == "boss":
            if st.button("Unlock as Boss"):
                st.session_state.user_authenticated = True
                st.rerun()
    else:
        st.success("Welcome, Boss Prapanchan")
        
        # RESTORED: UI Customization
        bg_color = st.color_picker("Background Color", "#0e1117")
        text_font = st.selectbox("Text Font", ["sans serif", "serif", "monospace"])
        
        load_history() # History restored
        if st.button("Logout"):
            st.session_state.user_authenticated = False
            st.rerun()

# --- 6. MAIN INTERFACE (LOCKED) ---
if st.session_state.user_authenticated:
    # Inject Custom UI
    st.markdown(f"""<style>.stApp {{ background-color: {bg_color}; font-family: {text_font}; }}</style>""", unsafe_allow_html=True)
    
    st.header("Executive Intelligence Hub")
    url_input = st.text_input("Video/Social URL:")
    target_lang = st.selectbox("Analysis Language", LANGUAGES)
    
    # RESTORED: Multi-Platform Analysis Options
    mode = st.radio("Intelligence Type", ["Full Summary", "Twitter Thread", "Threads Post", "Key Insights"])

    if st.button("Execute Deep Analysis"):
        with st.spinner("Processing..."):
            try:
                transcript = yt_dlp_transcript(url_input)
                prompt = f"Perform a {mode} in {target_lang} for this content: {transcript}"
                response = model.generate_content(prompt)
                st.session_state.summary = response.text
                save_to_history(url_input, st.session_state.summary, target_lang)
                st.rerun()
            except Exception:
                st.error("Processing error. Please verify the URL.")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)
        
        # RESTORED: Export Options
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📂 Download TXT", st.session_state.summary, file_name="tackyon_report.txt")
        with col2:
            # Simple PDF workaround using Text
            st.download_button("📄 Export PDF (Text)", st.session_state.summary, file_name="tackyon_report.pdf")

    # Chat Assistant
    st.markdown("---")
    st.subheader("💬 Tackyon AI Assistant")
    if prompt := st.chat_input("Ask me anything..."):
        if "boss" in prompt.lower() or "developed" in prompt.lower():
            st.chat_message("assistant").write("I was developed by my boss, **Prapanchan**.")
        else:
            chat_res = model.generate_content(f"Context: {st.session_state.summary}\nQuestion: {prompt}")
            st.chat_message("assistant").write(chat_res.text)
else:
    st.info("👋 Welcome to Tackyon AI. Secure your session via the sidebar to begin.")