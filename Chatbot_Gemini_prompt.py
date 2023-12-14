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

#sidebar contents

with st.sidebar:
    st.title('🦜️🔗VK - Generative AI ChatBot(Gemini API)')
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
st.title("Gemini pro: Chatbot")

# Model selection
selected_model = st.selectbox("Select a Generative Model", models)

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


