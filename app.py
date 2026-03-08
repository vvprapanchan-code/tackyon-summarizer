import streamlit as st
import time
import random
import hashlib
import uuid
import yt_dlp
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from supabase import create_client
from datetime import datetime

# --------------------------------------
# CONFIG
# --------------------------------------

st.set_page_config(
    page_title="Tackyon AI",
    page_icon="T",
    layout="centered"
)

# --------------------------------------
# ENVIRONMENT VARIABLES
# --------------------------------------

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

# --------------------------------------
# SUPABASE CONNECTION
# --------------------------------------

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------------------
# GEMINI SETUP
# --------------------------------------

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

# --------------------------------------
# CSS STYLING
# --------------------------------------

st.markdown("""
<style>

body {
    background-color:#0b0b0b;
}

.card {
    padding:25px;
    border-radius:18px;
    background:#121212;
    border:1px solid #2c2c2c;
    box-shadow:0 0 20px rgba(0,0,0,0.4);
}

.center {
    text-align:center;
}

.tlogo {
    font-size:80px;
    font-weight:bold;
    color:#8ec5ff;
}

.watermark {
    text-align:right;
    opacity:0.3;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------
# THIRUKURAL DATA
# --------------------------------------

kurals = [
("அகர முதல எழுத்தெல்லாம்", "ஆதி பகவன் முதற்றே உலகு"),
("கற்றதனால் ஆய பயனென்கொல்", "வாலறிவன் நற்றாள் தொழாஅர்"),
("அன்பும் அறனும் உடைத்தாயின்", "இல்வாழ்க்கை பண்பும் அதுவே"),
("ஒழுக்கம் விழுப்பம் தரலான்", "ஒழுக்கம் உயிரினும் ஓம்பப் படும்"),
]

# --------------------------------------
# UTILS
# --------------------------------------

def generate_tackyon_id():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "TACK-" + str(random.randint(100,999)) + random.choice(letters)

def device_hash():
    raw = str(uuid.getnode())
    return hashlib.sha256(raw.encode()).hexdigest()

# --------------------------------------
# SPLASH SCREEN
# --------------------------------------

def splash():

    st.markdown(
        "<div class='center'><div class='tlogo'>T</div><h2>Tackyon AI</h2></div>",
        unsafe_allow_html=True
    )

    time.sleep(2)
    st.session_state["splash_done"] = True
    st.rerun()

# --------------------------------------
# ONBOARDING
# --------------------------------------

def onboarding():

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Welcome")

    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male","Female","Other"])
    age = st.number_input("Age", 10,100)

    if st.button("Continue"):

        tid = generate_tackyon_id()

        st.session_state["user"] = {
            "name":name,
            "gender":gender,
            "age":age,
            "tackyon_id":tid
        }

        if supabase:
            supabase.table("users").insert({
                "name":name,
                "gender":gender,
                "age":age,
                "tackyon_id":tid,
                "device_hash":device_hash(),
                "created_at":str(datetime.now())
            }).execute()

        st.session_state["onboard_done"] = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------
# THIRUKURAL GATEWAY
# --------------------------------------

def kural_screen():

    kural = random.choice(kurals)

    st.markdown("<div class='card center'>", unsafe_allow_html=True)

    st.subheader("திருக்குறள்")

    st.write("")
    st.write(kural[0])
    st.write(kural[1])
    st.write("")

    if st.button("Enter"):
        st.session_state["kural_done"] = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------
# YOUTUBE METADATA
# --------------------------------------

def extract_metadata(url):

    ydl_opts = {
        'quiet':True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title":info.get("title"),
        "description":info.get("description"),
        "duration":info.get("duration"),
        "channel":info.get("channel")
    }

# --------------------------------------
# TRANSCRIPT
# --------------------------------------

def get_transcript(video_id):

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([x["text"] for x in transcript])
        return text
    except:
        return None

# --------------------------------------
# GEMINI ANALYSIS
# --------------------------------------

def analyze(text):

    prompt = f"""
    Analyze this video content.

    Provide:
    - Summary
    - Key Insights
    - Learning Points
    - Important Quotes

    Content:
    {text}
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:

        if "429" in str(e):
            return "AI engine busy. Try again later."

        return "AI processing error."

# --------------------------------------
# EXPORT
# --------------------------------------

def export_report(text):

    watermark = """

--------------------------------
Generated by Tackyon AI

        T
--------------------------------
"""

    final = text + watermark

    st.download_button(
        "Download Report",
        final,
        file_name="tackyon_report.txt"
    )

# --------------------------------------
# ASSISTANT CHAT
# --------------------------------------

def assistant():

    st.subheader("Tackyon Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user = st.text_input("Ask something")

    if st.button("Send"):

        st.session_state.chat.append(("user",user))

        try:
            response = model.generate_content(
                f"You are Tackyon AI assistant. {user}"
            )

            answer = response.text

        except:
            answer = "Assistant busy."

        st.session_state.chat.append(("ai",answer))

    for role,msg in st.session_state.chat:

        if role == "user":
            st.write("You:",msg)
        else:
            st.write("Tackyon AI:",msg)

# --------------------------------------
# DASHBOARD
# --------------------------------------

def dashboard():

    st.sidebar.title("Settings")

    theme = st.sidebar.selectbox(
        "Accent",
        ["Blue","Purple","Red","Silver"]
    )

    st.title("Tackyon AI")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    url = st.text_input("Paste YouTube URL")

    if st.button("Analyze"):

        if not url:
            st.warning("Enter URL")
            return

        video_id = url.split("v=")[-1]

        metadata = extract_metadata(url)

        transcript = get_transcript(video_id)

        if transcript:
            result = analyze(transcript)
        else:

            fallback = f"""
            Title: {metadata['title']}
            Description: {metadata['description']}
            """

            result = analyze(fallback)

        st.session_state["report"] = result

        st.write(result)

        if supabase:

            supabase.table("analysis_history").insert({

                "youtube_url":url,
                "summary":result,
                "created_at":str(datetime.now())

            }).execute()

    st.markdown("</div>", unsafe_allow_html=True)

    if "report" in st.session_state:
        export_report(st.session_state["report"])

    assistant()

# --------------------------------------
# APP FLOW
# --------------------------------------

if "splash_done" not in st.session_state:
    splash()

elif "onboard_done" not in st.session_state:
    onboarding()

elif "kural_done" not in st.session_state:
    kural_screen()

else:
    dashboard()
