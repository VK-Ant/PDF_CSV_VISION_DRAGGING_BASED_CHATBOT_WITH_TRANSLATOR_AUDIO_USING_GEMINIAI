import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_extras.add_vertical_space import add_vertical_space
import PIL.Image

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Sidebar contents
with st.sidebar:
    st.title('🦜️🔗VK - Gemini Bot integrating with streamlit')
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
    st.write('💡Full credit: Gemini AI🤗')



# List available models
models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

# Streamlit app
st.title("VK: Vision and Prompt Based Chatbot")

# Model selection
selected_model = st.selectbox("Select a Generative Model", models)

# File uploader for vision model
if 'generateContent' in genai.get_model(selected_model).supported_generation_methods:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Display uploaded image
    if uploaded_file is not None:
        # Read the uploaded image
        img = PIL.Image.open(uploaded_file)

        # Display the uploaded image
        st.subheader("Uploaded Image:")
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Generate content based on the image
        vision_model = genai.GenerativeModel(selected_model)
        response = vision_model.generate_content(img)

        # Display generated content
        st.subheader("Generated Content:")
        st.write(response.text)
    else:
        # Text input form
        question = st.text_input("Ask a question:")
        submitted = st.button("Submit")

        # Generate content on submission
        if submitted:
            model = genai.GenerativeModel(selected_model)
            response = model.generate_content(question)

            # Display question and generated content
            st.subheader("Question:")
            st.write(question)

            st.subheader("Generated Content:")
            st.write(response.text)
