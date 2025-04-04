import streamlit as st
from utils import extract_transcript, generate_summary, generate_quiz
import requests
from firebase_config import auth  # ✅ Import Firebase auth

# YouTube API Key
YOUTUBE_API_KEY = st.secrets["youtube_api"]["api_key"]

def search_youtube(query):
    """Search for YouTube videos based on a query."""
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}&maxResults=15"
    response = requests.get(url).json()
    return response.get("items", [])

# Streamlit UI
st.title("EdSetu v5.0")
st.write("🎥 YouTube Video Summarizer & Quiz Generator")

# ✅ Streamlit UI
st.sidebar.title("🔐 Login / Signup")

# ✅ User input fields
email = st.sidebar.text_input("📧 Email")
password = st.sidebar.text_input("🔑 Password", type="password")

# ✅ Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None


# ✅ Login Function
def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state.authenticated = True
        st.session_state.user = user
        st.sidebar.success(f"✅ Logged in as {email}")
    except Exception as e:
        st.sidebar.error(f"❌ Login Failed: {e}")

# ✅ Signup Function
def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        st.sidebar.success("✅ Account Created! Please login.")
    except Exception as e:
        st.sidebar.error(f"❌ Signup Failed: {e}")

# ✅ Logout Function
def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.sidebar.success("🚪 Logged out successfully.")

# ✅ Login / Signup Buttons
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.sidebar.button("Login"):
        login(email, password)
with col2:
    if st.sidebar.button("Signup"):
        signup(email, password)

if st.session_state.authenticated:
    st.sidebar.button("Logout", on_click=logout)


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


else:
    st.warning("⚠️ Please login to access the app.")