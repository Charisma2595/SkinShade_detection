import streamlit as st
import requests
import json

# Function to get skin shade from API
def get_skinshade_from_api(uploaded_file):
    url = 'https://api.robomua.com/api/skinshade'
    headers = {'x-api-key': 'iqbb3Z-lpRsKF5GpS7C0Ow=='}

    try:
        # Get the content of the uploaded file
        file_content = uploaded_file.read()

        # Send the content in the request
        files = {'file': ('image.jpg', file_content)}

        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # Raise an exception for HTTP errors

        return json.loads(response.text)

    except requests.exceptions.RequestException as e:
        st.error(f"Error in API request: {str(e)}")
        return None

# Function to recommend makeup based on hex color
def recommend_makeup(hex_color):
    makeup_dict = {
        'FF0000': 'Red Lipstick',
        'FF6347': 'Salmon Blush',
        '8B4513': 'Brown Eyeliner, Brown Foundation, and Red Lipstick',
        '4B0082': 'Purple Eyeshadow',
        '8A2BE2': 'Violet Lip Gloss',
        'c79982': 'Black Hair Attachment and Natural Lipstick',
        '2E8B57': 'Sea Green Nail Polish',
        'FFD700': 'Gold Highlighter',
        'B22222': 'Brick Red Lipstick',
        'CD5C5C': 'Rosy Cheek Tint',
        '00FF00': 'Green Eyeshadow',
        '0000FF': 'Blue Mascara',
        'FFFF00': 'Yellow Blush',
        'FF00FF': 'Magenta Lipstick',
        '00FFFF': 'Turquoise Eyeliner',
        '808080': 'Silver Metallic Eyeshadow',
        '800080': 'Purple Lipstick',
        'FF1493': 'Pink Blush',
        '7CFC00': 'Lime Green Nail Polish',
        '8B0000': 'Dark Red Lipstick',
        '9370DB': 'Lavender Blush and Lilac Eyeshadow',
        '48D1CC': 'Medium Turquoise Eyeliner',
        'FA8072': 'Salmon-Colored Lip Gloss',
        'FF4500': 'Orange Blush',
    }

    closest_match = find_closest_color(hex_color, makeup_dict.keys())
    return makeup_dict.get(closest_match, 'No specific recommendation')

# Function to convert hex color to RGB
def hex_to_rgb(hex_color):
    try:
        # Check if the hex color starts with '#'
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]  # Remove the '#' if present

        # Ensure the hex color is valid
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        else:
            raise ValueError("Invalid hex color format")

    except ValueError as e:
        st.error(f"Error converting hex color to RGB: {str(e)}")
        return None

# Function to find the closest color
def find_closest_color(target_color, color_list):
    target_rgb = hex_to_rgb(target_color)
    if target_rgb is None:
        return None

    closest_color = min(color_list, key=lambda color: color_distance(target_rgb, hex_to_rgb(color)))
    return closest_color

# Function to calculate color distance
def color_distance(color1, color2):
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

# Function to display recommendation and collect feedback
def display_recommendation(hex_color, makeup_recommendation):
    st.write(f"Skin shade: {hex_color}")
    st.write(f"Makeup Recommendation: {makeup_recommendation}")

    # Collect user feedback and rating
    user_feedback = st.text_input("Provide feedback:")
    user_rating = st.slider("Rate the recommendation (1-5)", 1, 5, 3)

    # Display feedback and rating
    st.write(f"User Feedback: {user_feedback}")
    st.write(f"User Rating: {user_rating}")

    # Submit Feedback button
    if st.button("Submit Feedback"):
        submit_feedback(hex_color, makeup_recommendation, user_feedback, user_rating)

# Function to submit feedback
def submit_feedback(hex_color, makeup_recommendation, user_feedback, user_rating):
    st.success(f"Feedback submitted: {user_feedback}")
    st.success(f"Rating submitted: {user_rating}")

# Main function
def main():
    st.title("Skin Shade and Makeup Recommendation App")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        
        api_response = get_skinshade_from_api(uploaded_file)
        
        if api_response and 'skinShade' in api_response:
            hex_color = api_response['skinShade']
            makeup_recommendation = recommend_makeup(hex_color)
            display_recommendation(hex_color, makeup_recommendation)
        else:
            st.error("Error: Hex color not found in the API response.")

if __name__ == "__main__":
    main()