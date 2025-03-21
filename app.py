import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from io import BytesIO
import base64

# Function to convert audio file to text
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError:
            return "Could not request results; check your internet connection"

# Function to translate text from English to Hindi
def translate_to_hindi(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='hi')
    return translated.text

# Function to convert text to audio and return playable HTML
def text_to_audio(text, lang='hi'):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
    audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
    return audio_html

# Streamlit app
st.title("Live English to Hindi Translator")
st.write("Upload an audio file (WAV format) with English speech, and get the Hindi translation as audio!")

# File uploader for audio input
uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Convert audio to text
    st.write("Processing audio...")
    english_text = audio_to_text("temp_audio.wav")
    st.write("English Text:", english_text)

    # Translate to Hindi
    hindi_text = translate_to_hindi(english_text)
    st.write("Hindi Translation:", hindi_text)

    # Convert Hindi text to audio
    audio_output = text_to_audio(hindi_text)
    st.write("Hindi Audio Output:")
    st.markdown(audio_output, unsafe_allow_html=True)

    # Clean up temporary file
    os.remove("temp_audio.wav")

st.write("Note: This app works with uploaded WAV files due to Streamlit Cloud limitations. For live mic input, run locally with additional setup.")
