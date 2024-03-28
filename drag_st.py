'''
import streamlit as st
from streamlit_cropperjs import st_cropperjs

pic = st.file_uploader("Upload a picture", key="uploaded_pic")
if pic:
    pic = pic.read()
    cropped_pic = st_cropperjs(pic=pic, btn_text="Detect!", key="foo")
    st.image(cropped_pic)
'''
import streamlit as st
import os
import tempfile
import shutil
from streamlit_cropperjs import st_cropperjs

# Function to process the cropped image
def process_cropped_image(cropped_image):
    # Your processing logic goes here
    st.image(cropped_image)

# Main Streamlit code
def main():
    st.title("Cropped Image Uploader")

    # Upload the image
    pic = st.file_uploader("Upload a picture", key="uploaded_pic")

    # If image uploaded
    if pic:
        pic_content = pic.read()

        # Display the image cropper
        cropped_pic = st_cropperjs(pic=pic_content, btn_text="Detect!", key="cropper")

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
            process_cropped_image(temp_cropped_image_path)

            # Remove the temporary directory and its contents
            shutil.rmtree(temp_dir)

# Run the Streamlit app
if __name__ == "__main__":
    main()

