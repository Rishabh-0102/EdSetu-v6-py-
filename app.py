import streamlit as st
from utils import extract_transcript, generate_summary, generate_quiz

# App title
st.title("🎥 YouTube Video Transcriber & Summarizer")

# Input for YouTube video link
video_url = st.text_input("Enter YouTube Video URL:")

# Display video thumbnail (if URL is provided)
if video_url:
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        st.image(thumbnail_url, caption="Video Thumbnail", use_column_width=True)
    except:
        st.error("Invalid YouTube URL")

# Button to fetch transcript and summary
if st.button("Get Summary"):
    if video_url:
        with st.spinner("Fetching transcript..."):
            transcript = extract_transcript(video_url)

        if "Error" not in transcript:
            st.subheader("📜 Video Transcript")
            st.text_area("Transcript", transcript, height=200)

            with st.spinner("Generating summary..."):
                summary = generate_summary(transcript)
            
            st.subheader("📝 Summary")
            st.write(summary)
        else:
            st.error(transcript)
    else:
        st.warning("Please enter a valid YouTube video URL.")

if st.button("Get Quiz"):
    if video_url:
        with st.spinner("Fetching transcript..."):
            transcript = extract_transcript(video_url)

        if "Error" not in transcript:
            # st.subheader("📜 Video Transcript")
            # st.text_area("Transcript", transcript, height=200)

            with st.spinner("Generating Quiz..."):
                quiz = generate_quiz(transcript)
            
            st.subheader("Quiz")
            st.write(quiz)
        else:
            st.error(transcript)
    else:
        st.warning("Please enter a valid YouTube video URL.")

# if st.download_button("Download Notes"):
    