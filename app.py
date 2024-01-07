import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Function to make a session with retry mechanism
def make_session():
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session

# Function to get the Skin Shade using the API
def get_skin_shade(api_key, image_path):
    skinshade_url = 'https://api.robomua.com/api/skinshade'

    headers = {
        'x-api-key': api_key.strip()  # Remove leading/trailing spaces
    }

    files = {
        'file': ('image', open(image_path, 'rb'))
    }

    session = make_session()  # Use the session for the request
    response = session.post(skinshade_url, headers=headers, files=files)
    result = response.json()

    return result.get('skinShade'), result.get('toneRange')

# Function to apply Lipstick using the API
def apply_lipstick(api_key, image_path, color_name):
    lips_url = 'https://api.robomua.com/api/lips'

    headers = {
        'x-api-key': api_key.strip()  # Remove leading/trailing spaces
    }

    files = {
        'file': ('image', open(image_path, 'rb'))
    }

    data = {
        'color': color_name
    }

    session = make_session()  # Use the session for the request
    response = session.post(lips_url, headers=headers, files=files, data=data)
    result = response.json()

    # Convert the base64 string to a PIL Image
    lipstick_image = Image.open(BytesIO(result.get('lipsImage').decode('base64')))

    return lipstick_image

# Streamlit UI
def main():
    st.title("Virtual Makeup Studio")

    # API Key Input
    api_key = st.text_input("Enter your API Key:")

    # Image Upload
    uploaded_file = st.file_uploader("Upload a photo of your face:", type=["jpg", "jpeg", "png", "heic"])

    if uploaded_file is not None and api_key:
        # Save the uploaded file locally
        image_path = save_uploaded_file(uploaded_file)

        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Skin Shade Detection
        if st.button("Detect Skin Shade"):
            skin_shade, tone_range = get_skin_shade(api_key, image_path)
            st.success(f"Detected Skin Shade: {skin_shade}, Tone Range: {tone_range}")

        # Lipstick Try-On
        lipstick_color = st.text_input("Enter Lipstick Color Name:")
        if lipstick_color and st.button("Try Lipstick"):
            lipstick_image = apply_lipstick(api_key, image_path, lipstick_color)
            st.image(lipstick_image, caption="Lipstick Try-On", use_column_width=True, output_format="JPEG")

# Function to save the uploaded file locally
def save_uploaded_file(uploaded_file):
    # Create a temporary directory if it doesn't exist
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())

    return file_path

if __name__ == "__main__":
    main()