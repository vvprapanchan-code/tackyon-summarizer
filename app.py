import streamlit as st
import youtube_transcript_api
import google.generativeai as genai

# --- 1. SETUP ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. UI BRANDING ---
st.set_page_config(page_title="Tackyon AI", page_icon="🚀")
st.title("Tackyon 🚀")
st.subheader("AI YouTube Summariser")

# --- 3. THE BRAIN ---
def get_transcript(video_id):
    try:
        # This specific call method is the industry standard for this library
        loader = youtube_transcript_api.YouTubeTranscriptApi()
        data = loader.get_transcript(video_id, cookies='cookies.txt')
        return " ".join([item['text'] for item in data])
    except Exception as e:
        return f"Error: {str(e)}"

# --- 4. USER INPUT ---
lang = st.selectbox("Select language:", ["English", "Tamil", "Hindi"])
url = st.text_input("Paste YouTube Link here:")

if st.button("Summarize Video"):
    if url:
        # This extracts the ID from both long and short links
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            video_id = url.split("/")[-1]
            
        with st.spinner("Tackyon is reading..."):
            transcript_text = get_transcript(video_id)
            
            if "Error:" in transcript_text:
                st.error(f"Issue found: {transcript_text}")
            else:
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Provide a detailed summary of this in {lang}: {transcript_text}"
                response = model.generate_content(prompt)
                st.success("Summary Ready!")
                st.write(response.text)