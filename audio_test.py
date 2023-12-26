import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_extras.add_vertical_space import add_vertical_space
import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
#sidebar contents

with st.sidebar:
    st.title('🦜️🔗VK - Chatbot')
    st.markdown('''
    ## About APP:

    The app's primary resource is utilised to create::

    - [streamlit](https://streamlit.io/)
    - [Gemini](https://ai.google.dev/tutorials/python_quickstart#chat_conversations)



    ## About me:

    - [Linkedin](https://www.linkedin.com/in/venkat-vk/)
    
    ''')

    add_vertical_space(4)
    st.write('💡All about Gemini exploration...., created by VK🤗')

# List available models
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

# Streamlit app
st.title("VK-Audio based Chatbot")

# Model selection
selected_model = st.selectbox("Select a Generative Model", models)

# Real-time audio input and speech-to-text conversion
fs = 16000  # Sample rate
duration = 5  # Recording duration in seconds

# Check if the user has submitted audio
submitted = st.button("Speak and Submit")

# Initialize transcription variable
transcribed_text = ""

if submitted:
    st.write("Speak now...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait for recording to finish

    # Save the recorded audio to a temporary file
    temp_file = "temp.wav"
    sf.write(temp_file, recording, fs)

    # Speech recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_file) as source:
        audio = recognizer.record(source)
        transcribed_text = recognizer.recognize_google(audio)

    # Display transcribed text
    st.subheader("Transcribed Text:")
    st.write(transcribed_text)

    # Process the transcribed text 
    processed_text = transcribed_text.upper()  

    # Display processed text
    st.subheader("Processed Text:")
    st.write(processed_text)

    # Generate content using Gemini
    model = genai.GenerativeModel(selected_model)
    response = model.generate_content(processed_text)  
    # Display generated content
    st.subheader("Generated Content:")
    st.write(response.text)

    # Clean up the temporary audio file
    os.remove(temp_file)
