import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_extras.add_vertical_space import add_vertical_space
import PIL.Image
from streamlit_cropperjs import st_cropperjs
import tempfile
import shutil

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Sidebar contents
with st.sidebar:
    st.title('🦜️🔗VK - DRAGING BASED IMAGE CAPTION CHATBOT')
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
st.title("VK - DRAGING BASED IMAGE CAPTION CHATBOT")

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
                #st.image(temp_cropped_image_path)
        
        if temp_cropped_image_path:
            # Generate content based on the image
            vision_model = genai.GenerativeModel(selected_model)
            response = vision_model.generate_content(PIL.Image.open(temp_cropped_image_path))

            # Display generated content
            st.subheader("Generated Content:")
            st.write(response.text)

    # Remove the temporary directory and its contents
    if temp_dir:
        shutil.rmtree(temp_dir)
