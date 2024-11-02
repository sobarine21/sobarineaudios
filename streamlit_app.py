import streamlit as st
import PyPDF2
import os
from gtts import gTTS
import tempfile

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file, handling potential errors."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except PyPDF2.PdfReadError as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def convert_text_to_audio(text, lang='en'):
    """Converts text to audio, handling potential errors."""
    try:
        tts = gTTS(text=text, lang=lang)
        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(audio_file.name)
        return audio_file.name
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

def main():
    st.title("Singing Audio Generator from Lyrics PDF")

    uploaded_file = st.file_uploader("Upload a PDF file containing lyrics", type="pdf")

    if uploaded_file is not None:
        # Extract text from the PDF
        lyrics = extract_text_from_pdf(uploaded_file)

        if not lyrics.strip():
            st.error("No text found in the PDF.")
        else:
            st.subheader("Extracted Lyrics:")
            st.write(lyrics)

            if st.button("Generate Singing Audio"):
                # Allow user to choose language
                lang = st.selectbox("Select Language", ["en", "fr", "de", "es", "it"])

                audio_file = convert_text_to_audio(lyrics, lang)

                if audio_file:
                    st.success("Audio generated successfully!")

                    # Provide option to download the audio file
                    with open(audio_file, "rb") as f:
                        st.download_button("Download Singing Audio", f, file_name="singing_audio.mp3")

                    # Optionally play audio in the app
                    st.audio(audio_file)

                    # Clean up the generated audio file after download
                    os.remove(audio_file)

if __name__ == "__main__":
    main()
