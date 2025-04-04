import streamlit as st
from utils import extract_transcript, generate_summary, generate_quiz
import requests

# YouTube API Key
YOUTUBE_API_KEY = "AIzaSyDKwheB2EpmoTmF_EvXpitoNb3sGZb1_kI"

def search_youtube(query):
    """Search for YouTube videos based on a query."""
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}&maxResults=5"
    response = requests.get(url).json()
    return response.get("items", [])

# Streamlit UI
st.title("🎥 YouTube Video Summarizer & Quiz Generator")

# Search bar
query = st.text_input("Search for YouTube videos:")
if query:
    results = search_youtube(query)
    for video in results:
        video_id = video["id"]["videoId"]
        title = video["snippet"]["title"]
        thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]

        # Display video thumbnail & title
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(thumbnail_url, use_container_width=True)  # ✅ FIX: Deprecated `use_column_width`
        with col2:
            st.write(f"**{title}**")
            # Clicking the button stores video ID & navigates to video page
            if st.button(f"▶ Watch {title}", key=video_id):
                st.session_state["selected_video"] = video_id
                st.switch_page("pages/video_page.py")
                # st.rerun()  # ✅ FIXED: Deprecated `st.experimental_rerun()`

# Redirect to video page when a video is selected
# if "selected_video" in st.session_state:
    # st.switch_page("video_page")  # ✅ FIXED: Better navigation