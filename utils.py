import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

load_dotenv()


genai.configure(api_key=os.getenv("AIzaSyAhPb-x252CQduuzsOEjX6kz3YXEN2tHJI"))

def extract_transcript(video_url):
    """Fetch transcript from a YouTube video, prioritizing English but allowing other languages."""
    try:
        # Extract video ID from URL
        video_id = video_url.split("v=")[-1].split("&")[0]

        try:
            # Try getting English transcript first
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
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

            # Fetch transcript text
            transcript_list = transcript.fetch()

        # Combine transcript text properly
        transcript_text = " ".join([t.text for t in transcript_list])  # FIX: Use `.text`

        return transcript_text
    except TranscriptsDisabled:
        return "Error: Transcripts are disabled for this video."
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"


def generate_summary(transcript_text):
    """Generate a summary using Google Generative AI."""
    try:
        model = "models/gemini-1.5-flash"  # or "models/gemini-1.5-flash-latest"
        
        prompt = (
            "I am a learner want to learn from youtube vide. I watched the video but i want the summery for futher use please help me in learning.I'm taking you as a YouTube video summarizer.You will be taking transcript text and summarizing the entire video and provide the important points"
            "Summarize the following transcript in bullet points (you can make as many points you want to create):\n\n"
            f"{transcript_text}"
        )
        
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"
def generate_quiz(transcript_text):
    """Generate a summary using Google Generative AI."""
    try:
        model = "models/gemini-1.5-flash"  # or "models/gemini-1.5-flash-latest"
        
        prompt = (
            "I am a learner want to learn from youtube vide. I watched the video but i want to go through my concepts so i want you to generate quiz or multiple-choice questions for checking if i properly learned these or not please help me in learning.I'm taking you as my teacher who can give me a multiple-choice questions.You will be taking transcript text and making the quize from it."
            "Make the quiz of the following transcript(you can make as many multiple-choice questions you want but insure that the all topics are covered):\n\n"
            f"{transcript_text}"
        )
        
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"