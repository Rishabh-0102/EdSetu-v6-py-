import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

load_dotenv()


genai.configure(api_key=os.getenv("AIzaSyAhPb-x252CQduuzsOEjX6kz3YXEN2tHJI"))

def extract_transcript(video_id):
    """Fetch transcript from a YouTube video, prioritizing English but allowing other languages."""
    try:
        
        try:
            # Try getting English transcript first
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi','en'])
        except NoTranscriptFound:
            # Get list of available transcripts
            available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

            # Find an auto-generated transcript (fallback if English is not available)
            transcript = None
            for transcript_item in available_transcripts:
                if transcript_item.is_generated:  # Pick first auto-generated transcript
                    transcript = transcript_item
                    break
            
            if transcript is None:
                return "Error: No available transcript found for this video."

            # Fetch transcript text correctly
            transcript_list = transcript.fetch()

        # ✅ DEBUG: Print transcript_list to see what it contains
        print("DEBUG: Transcript List Type ->", type(transcript_list))
        print("DEBUG: First Item ->", transcript_list[0] if isinstance(transcript_list, list) else transcript_list)

        # ✅ FIX: Ensure transcript_list is a list of dicts before accessing "text"
        if isinstance(transcript_list, list) and all(isinstance(item, dict) for item in transcript_list):
            transcript_text = " ".join([item["text"] for item in transcript_list])
            return transcript_text
        else:
            return f"Error: Unexpected response format from YouTubeTranscriptApi. Response: {transcript_list}"

    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"


def generate_summary(transcript_text):
    """Generate a summary using Google Generative AI."""
    try:
        model = "models/gemini-1.5-flash"  # or "models/gemini-1.5-flash-latest"
        
        prompt = (
            "I watched a YouTube video, and I need a summary for learning. Please summarize the key points in bullet format."
            f"\n\nTranscript:\n{transcript_text}"
        )
        
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_quiz(transcript_text):
    """Generate a quiz using Google Generative AI."""
    try:
        model = "models/gemini-1.5-flash"  # or "models/gemini-1.5-flash-latest"
        
        prompt = (
            "Generate multiple-choice questions (MCQs) from the given YouTube video transcript to test my understanding."
            f"\n\nTranscript:\n{transcript_text}"
        )
        
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating quiz: {str(e)}"