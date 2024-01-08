## Skin Shade and Makeup Recommendation App
This application utilizes an API to determine the skin shade from an uploaded image and provides makeup recommendations based on the detected skin shade. Users can also provide feedback and ratings for the makeup recommendations.

## How to Use
- Upload an Image:

- Click on the "Choose an image..." button to upload a JPG, JPEG, or PNG file.
View Makeup Recommendation:
The app will display the uploaded image along with the detected skin shade and makeup recommendation.

- Provide Feedback:
Users can provide feedback on the makeup recommendation by entering comments in the "Provide feedback" text box.

- Rate the Recommendation:
Users can rate the makeup recommendation on a scale from 1 to 5 using the slider.
Submit Feedback:

- Click the "Submit Feedback" button to submit user feedback and rating.

## Code Overview
The application is built using Python and the Streamlit library. The main components of the code include:

- API Integration:
The get_skinshade_from_api function sends the uploaded image to an API (https://api.robomua.com/api/skinshade) to obtain the skin shade information.

- Makeup Recommendation:
The recommend_makeup function maps the detected hex color to makeup recommendations using a predefined dictionary.

- Color Processing:
The hex_to_rgb, find_closest_color, and color_distance functions handle color conversion and comparison.

- User Interface:
The Streamlit library is used to create a user-friendly interface, allowing users to upload images, view recommendations, provide feedback, and submit ratings.

- Feedback Submission:
The submit_feedback function is called when users click the "Submit Feedback" button, displaying success messages with the submitted feedback and rating.

- Dependencies
Ensure that the following Python libraries are installed before running the application:


## How to Run

- creat an environment 

- pip install requirments.txt

- run the command "streamlit run app.py".






