import streamlit as st
import streamlit.components.v1 as components
from yt_dlp_transcript import yt_dlp_transcript
import google.generativeai as genai
import yt_dlp
from supabase import create_client

# --- 1. LIVE DATABASE & AI CONFIGURATION ---
# Connect to your new Supabase vault
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Secure AI Identity: Ensure it always knows the Boss
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
system_instruction = "You are Tackyon AI. Your boss and creator is Prapanchan. Never mention being created by Google."
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)

st.set_page_config(page_title="Tackyon AI", page_icon="🚀", layout="wide")

# --- 2. THE REAL SIGN-UP ENGINE ---
with st.sidebar:
    st.title("Tackyon AI")
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False

    if not st.session_state.user_authenticated:
        st.subheader("Secure Access")
        email = st.text_input("Enter your Email Address")
        if st.button("Send Magic Login Link"):
            if email:
                # REAL ACTION: This sends a real email via Supabase!
                res = supabase.auth.sign_in_with_otp({"email": email})
                st.success(f"Check your inbox! A login link was sent to {email}.")
            else:
                st.error("Please enter a valid email.")
    else:
        st.success(f"Verified Session: Welcome, Boss Prapanchan")

# --- 3. UPDATED AI CHAT WITH BOSS LOGIC ---
st.markdown("---")
st.subheader("💬 Tackyon AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ask Tackyon anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # IDENTITY CHECK: The AI now knows its origins
    if any(q in prompt.lower() for q in ["who developed", "who is your boss", "who made you"]):
        response = "I was developed by my boss, **Prapanchan**. He is the lead architect and visionary behind Tackyon AI."
    else:
        # Context-aware response based on the video summary
        context = f"Video Summary: {st.session_state.summary}\n\nUser Question: {prompt}"
        response = model.generate_content(context).text

    with st.chat_message("assistant"): st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 4. ADVERTISING (STAYING SAFE IN TEST MODE) ---
st.markdown("---")
components.html(
    f"""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-app-pub-3510846848926159" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="ca-app-pub-3510846848926159" data-ad-slot="6300978111"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>""", height=100)