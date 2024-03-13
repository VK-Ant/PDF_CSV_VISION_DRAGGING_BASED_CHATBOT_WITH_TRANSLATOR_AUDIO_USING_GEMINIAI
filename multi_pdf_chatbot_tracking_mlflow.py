import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as palm
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import mlflow
import tempfile
mlflow.set_tracking_uri("http://127.0.0.1:8120")
# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Sidebar contents
with st.sidebar:
    st.title('🦜️🔗VK: Multiple Pdf based Chatbot using Streamlit and MLFLOW')
    st.markdown('''
    ## About APP:

    The app's primary resource is utilized to create::

    - [streamlit](https://streamlit.io/)
    - [Gemini](https://ai.google.dev/tutorials/python_quickstart#chat_conversations)
    - [Palm2](https://ai.google/discover/palm2)

    ## About me:

    - [Linkedin](https://www.linkedin.com/in/venkat-vk/)
    
    ''')
def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GooglePalmEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

def get_conversational_chain(vector_store):
    llm=GooglePalm()
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
    return conversation_chain

def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.write("Human: ", message.content)
        else:
            st.write("Bot: ", message.content)
    # Log question, answer, and timestamp with MLflow
    for message in st.session_state.chatHistory:
        with mlflow.start_run(run_name="VK Chatbot Experiment - Tracking", nested=True) as nested_run:
            mlflow.log_param("Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            mlflow.log_param("Question", user_question)
            mlflow.log_param("Answer", message.content)

def main():
    st.header("VK: Chat with Multiple PDF 💬")
    user_question = st.text_input("Ask a Question from the PDF Files")
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    if user_question:
        user_input(user_question)
    with st.sidebar:
        st.title("Settings")
        st.subheader("Upload your Documents")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Process Button", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success("Done")
                # Log PDFs as artifacts
                with mlflow.start_run(run_name="Chatbot Experiment") as run:
                    for pdf in pdf_docs:
                        with tempfile.NamedTemporaryFile(delete=False) as tmp_pdf:
                            tmp_pdf.write(pdf.read())
                            mlflow.log_artifact(tmp_pdf.name, artifact_path="pdfs")

if __name__ == "__main__":
    main()
