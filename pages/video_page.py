import streamlit as st
from utils import extract_transcript, generate_summary, generate_quiz

# Check if a video is selected
if "selected_video" not in st.session_state:
    st.warning("No video selected! Please go back and choose a video.")
    if st.button("🔍 Back to Search"):
        st.switch_page("app.py")
    st.stop()

video_id = st.session_state["selected_video"]

# Show the video player
st.title("🎬 Watching Video")
st.video(f"https://www.youtube.com/watch?v={video_id}")

col1, col2 = st.tabs(["Summary", "Quiz"])

# Buttons for Summarization & Quiz
with col1:
    if st.button("📜 Get Summary"):
        with st.spinner("Fetching transcript..."):
            transcript = extract_transcript(video_id)  # ✅ FIXED: Now correctly passing `video_id` instead of full URL

        if "Error" not in transcript:
            with st.spinner("Generating summary..."):
                summary = generate_summary(transcript)
            st.subheader("📝 Summary")
            st.write(summary)
        else:
            st.error(transcript)
with col2:
    if st.button("🧠 Generate Quiz"):
        with st.spinner("Fetching transcript..."):
            transcript = extract_transcript(video_id)  # ✅ FIXED: Now correctly passing `video_id`

        if "Error" not in transcript:
            with st.spinner("Generating Quiz..."):
                quiz = generate_quiz(transcript)
            st.subheader("🔢 Quiz")
            st.write(quiz)
        else:
            st.error(transcript)

if st.button("🔍 Back to Search"):
    st.switch_page("app.py")  # ✅ FIXED: Better navigation