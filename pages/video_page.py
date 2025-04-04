import streamlit as st
from utils import extract_transcript, generate_summary, generate_quiz, generate_notes
import ast

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

col1, col2, col3 = st.tabs(["Summary", "Quiz","Notes"])

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
    # Initialize quiz session states
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    # Generate Quiz Button
    if st.button("🧠 Generate Quiz"):
        with st.spinner("Fetching transcript..."):
            transcript = extract_transcript(video_id)

        if "Error" not in transcript:
            with st.spinner("Generating Quiz..."):
                quiz_string = generate_quiz(transcript)

            # Clean code block markdown if needed
            cleaned = quiz_string.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip("` \n")
                if "python" in cleaned.lower():
                    cleaned = "\n".join(cleaned.split("\n")[1:])

            try:
                st.session_state.quiz_data = ast.literal_eval(cleaned)
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = {}  # Reset user answers
            except Exception as e:
                st.error(f"Failed to parse quiz data: {str(e)}")
        else:
            st.error(transcript)

    # Display Quiz Questions
    if st.session_state.quiz_data and not st.session_state.quiz_submitted:
        st.subheader("🧠 Quiz Time!")

        for i, question in enumerate(st.session_state.quiz_data):
            st.markdown(f"*Q{i+1}. {question['question']}*")
            st.session_state.user_answers[i] = st.radio(
                label="Choose an answer:",
                options=question["options"],
                key=f"q{i}",
                index=None,  # ✅ Don't pre-select anything
                label_visibility="collapsed"
            )
            st.write("---")

        if st.button("✅ Submit Quiz"):
            st.session_state.quiz_submitted = True

    # Display Results After Submission
    if st.session_state.quiz_data and st.session_state.quiz_submitted:
        st.subheader("✅ Result")

        score = 0
        for idx, question in enumerate(st.session_state.quiz_data):
            user = st.session_state.user_answers.get(idx)
            correct = question["answer"]
            is_correct = user == correct
            if is_correct:
                score += 1
            st.markdown(
                f"*Q{idx+1}:* {question['question']}\n\n"
                f"- Your Answer: {'✅ ' if is_correct else '❌ '}{user}\n"
                f"- Correct Answer: {correct}\n"
            )
        st.success(f"🎯 Your Final Score: {score} / {len(st.session_state.quiz_data)}")

with col3:
    if st.button("Fetch PDF"):
        with st.spinner("Fetching transcript..."):
            transcript = extract_transcript(video_id)

        if "Error" not in transcript:
            pdf_data = generate_notes(transcript)
            st.download_button("Download Notes", pdf_data, "notes.pdf", mime="application/pdf")
        else:
            st.error(transcript)

if st.button("🔍 Back to Search"):
    st.switch_page("app.py")  # ✅ FIXED: Better navigation