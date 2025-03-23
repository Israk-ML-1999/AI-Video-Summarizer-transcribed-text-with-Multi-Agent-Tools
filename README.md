# AI-Video-Summarizer-transcribed-text-with-Multi-Agent-Tools
This project uses a combination of Groq API, OpenAI Whisper for audio transcription, and multi-agent tools to process and analyze video content. Users can upload videos, get transcriptions, and request summarizations, fact-checking, or web searches. It leverages cutting-edge **llama3-8b-8192 models** for AI-based responses.

## Features:
- **Upload a video**: Easily upload your video file for analysis.
- **Audio Transcription**: Automatically transcribe the audio content of the video using OpenAI Whisper.
- **Summarization**: Summarize the video based on the transcript.
- **Query-based Interactions**: Ask questions related to the video content (e.g., key points, fact-checking, searching more info).
- **Multi-Agent Tools**: Includes Groq for summarizing and other agents for fact-checking and searching.

## Technologies Used:
- **Streamlit**: For building interactive web apps.
- **OpenAI Whisper**: For transcribing video audio into text.
- **Groq API**: For AI-powered summarization using llama3-8b-8192.
- **Python**: For developing the backend logic.


  ## Install dependencies:
  pip install -r requirements.txt

  
## Set up environment variables:
- Create a `.env` file in the root directory and add your **Groq API key**:
  ```
  GROQ_API_KEY=your_api_key
  ```

## Run the Streamlit app.py

