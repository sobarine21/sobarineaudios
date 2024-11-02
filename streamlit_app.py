import streamlit as st
import PyPDF2
from gtts import gTTS
import os

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"  # Adding newline for better formatting
    return text

def convert_text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_file = 'output.mp3'
    tts.save(audio_file)
    return audio_file

def main():
    st.title("Podcast creator")
    
    uploaded_file = st.file_uploader("Upload content pdf", type="pdf")

    if uploaded_file is not None:
        # Extract text from the PDF
        lyrics = extract_text_from_pdf(uploaded_file)
        if not lyrics.strip():
            st.error("No text found in the PDF.")
            return

        st.subheader("Extracted Lyrics:")
        st.write(lyrics)

        if st.button("Generate podcast Audio"):
            audio_file = convert_text_to_audio(lyrics)
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
