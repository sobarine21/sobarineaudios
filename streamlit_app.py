import streamlit as st
import PyPDF2
import os
from gtts import gTTS
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import tempfile

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def convert_text_to_audio(text, lang='en', speed=1.0):
    tts = gTTS(text=text, lang=lang)
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(audio_file.name)
    
    # Adjust speed (pydub allows us to speed up/slower the audio)
    audio = AudioSegment.from_file(audio_file.name)
    new_audio = audio.speedup(playback_speed=speed)
    new_audio.export(audio_file.name, format="mp3")
    
    return audio_file.name

def main():
    st.title("Podacst creator from PDF")

    uploaded_file = st.file_uploader("Upload a PDF file containing content", type="pdf")

    if uploaded_file is not None:
        # Extract text from the PDF
        lyrics = extract_text_from_pdf(uploaded_file)
        if not lyrics.strip():
            st.error("No text found in the PDF.")
            return

        st.subheader("Extracted Lyrics:")
        st.write(lyrics)

        # Voice and speed options
        speed = st.slider("Choose playback speed", min_value=0.5, max_value=2.0, value=1.0)
        
        if st.button("Generate Singing Audio"):
            audio_file = convert_text_to_audio(lyrics, speed=speed)
            st.success("Audio generated successfully!")

            # Provide option to download the audio file
            with open(audio_file, "rb") as f:
                st.download_button("Download podcast Audio", f, file_name="podcast_audio.mp3")

            # Optionally play audio in the app
            st.audio(audio_file)

            # Clean up the generated audio file after download
            os.remove(audio_file)

if __name__ == "__main__":
    main()
