import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from fpdf import FPDF
from io import BytesIO

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
        # print("DEBUG: Transcript List Type ->", type(transcript_list))
        # print("DEBUG: First Item ->", transcript_list[0] if isinstance(transcript_list, list) else transcript_list)

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
            "I am a learner want to learn from youtube video. I watched the video but i want the summery of video, please help me in learning.I'm taking you as a YouTube video summarizer.You will be taking transcript text and summarizing the entire video and provide the important points"
            f"\n\nTranscript is here(can you summarize this in most minimum points):\n{transcript_text}"
        )
        
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_quiz(transcript_text):
    """Generate quiz using Google Generative AI in Python list-of-dict format."""
    try:
        model = "models/gemini-1.5-flash"

        prompt = (
            "You are a Python assistant. Based on the transcript below, generate a list of multiple-choice questions.\n\n"
            "Each question must be a Python dictionary in this format:\n"
            "{\n"
            '  "question": "Question text?",\n'
            '  "options": ["Option 1", "Option 2", "Option 3", "Option 4"],\n'
            '  "answer": "Correct Option Text"\n'
            "}\n\n"
            "Your final output must be ONLY a valid Python list of such dictionaries, like:\n"
            '[{"question": "...", "options": [...], "answer": "..."}, ...]\n\n'
            "*Important*: DO NOT include any explanation, comments, or markdown formatting (like  or python). Return ONLY the pure Python list.\n\n"
            "Transcript:\n"
            f"{transcript_text}"
        )
        
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating quiz: {str(e)}"
    
def generate_notes(transcript_text):
    """Generate a notes using Google Generative AI."""
    try:
        model = "models/gemini-1.5-flash"  # or "models/gemini-1.5-flash-latest"
        
        prompt = (
            "I am a learner want to learn from youtube vide. I watched the video but i want the notes for futher use please help me in learning.I'm taking you as a YouTube video notes generator.You will be taking transcript text and of the entire video and provide the notes of it."
            f"\n\nTranscript is here(make as lengthy and detalide notes you want):\n{transcript_text}"
        )
        
        response = genai.GenerativeModel(model).generate_content(prompt)
        return generate_pdf(response.text)
    except Exception as e:
        return f"Error generating quiz: {str(e)}"

def generate_pdf(text):
    """Generate a PDF from the given transcript text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)  # Multi-cell for line wrapping

    # Save PDF to BytesIO buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer, "F")
    pdf_buffer.seek(0)  # Move to the beginning of the buffer

    return pdf_buffer.getvalue()  # Return the binary content of the PDF