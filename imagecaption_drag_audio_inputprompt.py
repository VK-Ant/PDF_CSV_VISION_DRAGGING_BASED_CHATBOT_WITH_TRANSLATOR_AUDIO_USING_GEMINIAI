import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_extras.add_vertical_space import add_vertical_space
import PIL.Image
from streamlit_cropperjs import st_cropperjs
import tempfile
import shutil
from gtts import gTTS
import io
from googletrans import Translator

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Function to convert text to audio using gTTS
def text_to_audio(text, language):
    tts = gTTS(text=text, lang=language)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    return audio_bytes

# Function to translate text using Google Translate
def translate_text(text, dest_language):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

# Sidebar contents
with st.sidebar:
    st.title('🦜️🔗VK - DRAGING BASED IMAGE CAPTION CHATBOT WITH TRANSLATOR ')
    st.markdown('''
    ## About APP:
                
    In this chatbot helps user easily identify the image caption through the draging. Its very much
    useful application for Drone, Manufacturing industry etc...

    The app's primary resource is utilized to create:

    - [streamlit](https://streamlit.io/)
    - [Gemini](https://ai.google.dev/tutorials/python_quickstart#chat_conversations)

    ## About me:

    - [Linkedin](https://www.linkedin.com/in/venkat-vk/)
    
    ''')
    add_vertical_space(1)
    st.write('💡All about exploration...., created by VK🤗')

# List available models
models = [m.name for m in genai.list_models()]

# Streamlit app
st.title("VK - DRAGING BASED IMAGE CAPTION WITH TRANSLATOR (AUDIO RESPONSE) CHATBOT")

# Model selection
selected_model = st.selectbox("Select a Model", models)

# File uploader for vision model
if 'generateContent' in genai.get_model(selected_model).supported_generation_methods:
    pic = st.file_uploader("Upload a picture", key="uploaded_pic")

    # Define temporary directory
    temp_dir = None
    temp_cropped_image_path = None

    # Display uploaded image
    if pic is not None:

        # Get crop coordinates
        if pic:
            pic = pic.read()
            cropped_pic = st_cropperjs(pic=pic, btn_text="Select Particular Portion and Submit!", key="foo")

            #st.image(cropped_pic)

            # If the cropped image is selected
            if cropped_pic:
                # Create a temporary directory
                temp_dir = tempfile.mkdtemp()

                # Define the path for the temporary cropped image
                temp_cropped_image_path = os.path.join(temp_dir, "cropped_image.png")

                # Write the cropped image content to the temporary file
                with open(temp_cropped_image_path, "wb") as temp_file:
                    temp_file.write(cropped_pic)

                # Process the cropped image
                # st.image(temp_cropped_image_path)

        if temp_cropped_image_path:
            # Generate content based on the image

            vision_model = genai.GenerativeModel(selected_model)
            prompt = st.text_input(label='ask question')
            img = PIL.Image.open(temp_cropped_image_path)

            response = vision_model.generate_content(contents=[prompt,img])

            # Display generated content
            st.subheader("Generated Content:")
            st.write(response.text)

            # Language selection for audio conversion
            languages = {'Tamil': 'ta','English': 'en', 'French': 'fr', 'Hindi': 'hi', 'German': 'de', 'Japanese': 'ja'}
            selected_language = st.selectbox("Select Language for Audio Conversion", list(languages.keys()))

            if selected_language:
                # Translate the text to the selected language
                translated_text = translate_text(response.text, languages[selected_language])

                # Convert translated text to audio
                audio_bytes = text_to_audio(translated_text, languages[selected_language])
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.warning("Please select a language for audio conversion.")

    # Remove the temporary directory and its contents
    if temp_dir:
        shutil.rmtree(temp_dir)
