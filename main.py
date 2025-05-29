import streamlit as st
from pytubefix import YouTube
import os


def download_video(url, output_path="downloads"):
    try:
        # Create downloads folder if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Get YouTube video
        yt = YouTube(url)

        # Get the highest resolution stream
        stream = yt.streams.filter(res='144p').first()

        # Display video info
        st.info(f"Downloading: **{yt.title}**")
        st.image(yt.thumbnail_url, width=300)

        # Download with progress
        progress_bar = st.progress(0)

        def progress_callback(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            progress = bytes_downloaded / total_size
            progress_bar.progress(progress)

        yt.register_on_progress_callback(progress_callback)
        file_path = stream.download(output_path)

        st.success("✅ Download Complete!")
        st.download_button(
            label="Download Video",
            data=open(file_path, "rb"),
            file_name=os.path.basename(file_path),
            mime="video/mp4"
        )
    except Exception as e:
        st.error(f"❌ Error: {e}")


# --- Streamlit UI ---
st.title("YouTube Video Downloader 🎥")
st.write("Download any YouTube video in MP4 format")

# Input URL
video_url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Download"):
    if video_url:
        download_video(video_url)
    else:
        st.warning("Please enter a valid YouTube URL!")
