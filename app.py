import streamlit as st
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import requests
import base64
import whisper  # OpenAI Whisper for transcription

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit config
st.set_page_config(
    page_title="Groq Video Summarizer",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 AI Video Summarizer with Groq")
st.subheader("Powered by Open Source LLMs - LLaMA3 + Whisper")

# Get Groq API headers
def get_groq_headers():
    return {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

# Query Groq API
def query_groq(prompt, model="llama3-8b-8192"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for summarizing video content."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    response = requests.post(url, headers=get_groq_headers(), json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Groq API Error: {response.status_code} - {response.text}"

# Load Whisper model (cached)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

# Transcribe video
def transcribe_audio(video_path):
    model = load_whisper_model()
    result = model.transcribe(video_path)
    return result["text"]

# Convert video to base64 and embed with custom size
def get_base64_video(video_path):
    with open(video_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return f"data:video/mp4;base64,{encoded}"

def show_custom_sized_video(video_path, width=480, height=320):
    base64_video = get_base64_video(video_path)
    video_html = f"""
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 10px;">
        <video width="{width}" height="{height}" controls>
            <source src="{base64_video}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    """
    st.markdown(video_html, unsafe_allow_html=True)

# Web Search Agent
def web_search(query):
    search_url = f"https://www.duckduckgo.com/?q={query}"
    return f"Web search results: [Click here]({search_url})"

# Fact-Checking Agent
def fact_checking(query):
    # Placeholder for fact-checking
    return f"Fact-checking: [Search for verification](https://www.duckduckgo.com/?q={query})"

# Multi-Agent Class
class VideoAgent:
    def __init__(self, video_path, user_query):
        self.video_path = video_path
        self.user_query = user_query
        self.transcript = self.transcribe_video()

    def transcribe_video(self):
        return transcribe_audio(self.video_path)

    def summarize_video(self):
        prompt = (
            f"Here is the transcript of a video:\n\n{self.transcript}\n\n"
            f"Now respond to the following request:\n{self.user_query}"
        )
        return query_groq(prompt)

    def search_web(self):
        return web_search(self.user_query)

    def fact_check(self):
        return fact_checking(self.user_query)

    def process_query(self):
        user_query_lower = self.user_query.lower()
        
        # Checking if the user query suggests summarization
        if any(keyword in user_query_lower for keyword in ["summarize", "key points", "summary", "main ideas"]):
            return self.summarize_video()
        
        # Checking if the user query suggests a web search
        elif any(keyword in user_query_lower for keyword in ["search", "find more", "look up", "additional info"]):
            return self.search_web()
        
        # Checking if the user query suggests fact-checking
        elif any(keyword in user_query_lower for keyword in ["fact-check", "verify", "is this true", "check"]):
            return self.fact_check()
        
        # If none of the above keywords are found, return a default message
        else:
            return "Sorry, I couldn't understand the query. Please ask for a summary, search, or fact-check."

# File uploader UI
video_file = st.file_uploader("📤 Upload a video file", type=['mp4', 'mov', 'avi'])

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    st.markdown("""<h3 style="text-align: center;">📺 Preview Uploaded Video</h3>""", unsafe_allow_html=True)
    
    show_custom_sized_video(video_path, width=480, height=320)

    # Show Transcript of Video
    st.subheader("📝 Video Transcript")
    transcript = transcribe_audio(video_path)
    st.text_area("Transcript:", value=transcript, height=300)

    user_query = st.text_area(
        "🧠 What do you want to know from this video?",
        placeholder="Example: Summarize the key points, search for info, or fact-check something...",
        help="Ask anything based on the video content"
    )

    if st.button("✨ Get Analysis"):
        with st.spinner("⏳ Processing..."):
            agent = VideoAgent(video_path, user_query)
            result = agent.process_query()

        st.subheader("✅ Analysis Result")
        st.markdown(result)

        # Clean up temp file
        Path(video_path).unlink(missing_ok=True)
else:
    st.info("📥 Please upload a video to get started.")

# Style
st.markdown("""
    <style>
    .stTextArea textarea {
        height: 60px;
    }
    </style>
    """, unsafe_allow_html=True)
