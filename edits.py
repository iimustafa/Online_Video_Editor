import streamlit as st
import moviepy.editor as mp
import numpy as np
import tempfile
import os

st.title("🎬 Streamlit Video Editor (MoviePy Ready)")
st.write("This application confirms that Streamlit, MoviePy, and Pillow are all installed and compatible.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload a video file to test (e.g., .mp4)", type=['mp4', 'mov'])

if uploaded_file is not None:
    # --- Create a temporary file ---
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    tfile.close()
    video_path = tfile.name

    try:
        # --- MoviePy Processing (The Critical Step) ---
        st.subheader("Processing Video with MoviePy")

        # Load the video clip
        clip = mp.VideoFileClip(video_path)
        
        st.success(f"Video loaded successfully! Duration: {clip.duration:.2f} seconds.")

        # Simple edit: creating a small subclip to prove functionality
        # We ensure the clip is long enough before trying to take a subclip
        if clip.duration > 2:
            subclip = clip.subclip(0, 2)
        else:
            subclip = clip.subclip(0, clip.duration)

        # Create a temp output file for the edited video
        output_tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        output_path = output_tfile.name
        output_tfile.close()

        # Write the edited video (small clip)
        subclip.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac', 
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False, 
            logger=None
        )
        
        st.subheader("Result")
        st.video(output_path, format="video/mp4")
        st.success("Successfully processed and displayed a 2-second clip!")

    except Exception as e:
        st.error(f"An error occurred during video processing: {e}")
    finally:
        # Clean up temporary files
        os.unlink(video_path)
        if 'output_path' in locals() and os.path.exists(output_path):
             os.unlink(output_path)
        if os.path.exists('temp-audio.m4a'):
             os.unlink('temp-audio.m4a')
