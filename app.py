# Import necessary libraries
import streamlit as st
import google.generativeai as genai  # Google Gemini Pro Vision API client
import os
from dotenv import load_dotenv  # For loading environment variables
from PIL import Image

# ------------------------------------------------------------------------------
# Stage: Environment Variable Setup
# ------------------------------------------------------------------------------
# Load environment variables from a .env file. Ensure your .env file contains:
# GOOGLE_API_KEY=your_actual_api_key
load_dotenv()  # loading all the environment variables

# Configure the Google Generative AI client with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ------------------------------------------------------------------------------
# Stage: Helper Function to Get Generative Response from Image
# ------------------------------------------------------------------------------
def get_gemini_response(input_prompt, image_data):
    """
    This function interacts with the Google Gemini Pro Vision API.
    
    Parameters:
      - input_prompt (str): The text prompt that instructs the API on what to do.
      - image_data (list): A list containing dictionaries with the image's MIME type and bytes.
    
    Returns:
      - str: The text response generated by the API.
    """
    # Initialize the generative model; 'gemini-1.5-flash' is the image processing model.
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Generate content based on the provided prompt and image data.
    response = model.generate_content([input_prompt, image_data[0]])
    
    # Return the textual response from the model.
    return response.text

# ------------------------------------------------------------------------------
# Stage: Helper Function to Process Uploaded Image
# ------------------------------------------------------------------------------
def input_image_setup(uploaded_file):
    """
    Converts the uploaded file into a format required by the API.
    
    Parameters:
      - uploaded_file: The file object returned by Streamlit's file_uploader.
    
    Returns:
      - list: A list containing dictionaries with keys 'mime_type' and 'data'.
    """
    if uploaded_file is not None:
        # Read the entire file as bytes
        image_bytes = uploaded_file.getvalue()
        # Return a list with the required format:
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": image_bytes
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# ------------------------------------------------------------------------------
# Stage: Streamlit Web Interface
# ------------------------------------------------------------------------------
# Set the header for the app
st.set_page_config(page_title="Calorie Advisor App")
st.header("Calorie Advisor App")

# Create a file uploader that accepts JPG and PNG images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
image = None

# If an image is uploaded, display it on the app
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_container_width=True)


# When the user clicks the "Tell me about the calories" button
submit = st.button("Tell me about the calories")

if submit:
    # ------------------------------------------------------------------------------
    # Stage: Define the Input Prompt for the API
    # ------------------------------------------------------------------------------
    input_prompt = """
    You are an expert in nutrition. Given the food items in the image,
    calculate the total calories and provide a detailed breakdown of each food item
    with its calorie content in the format 
    1. Item 1 - number of calories
    2. Item 2 - number of calories
    ----
    ----
    Finally, indicate whether the food is healthy and provide the percentage split of 
    carbohydrates, fats, fiber, sugar, and other macronutrients and your best advice regarding the diet and also what other items we need to add to make it healthy.
    """
    
    # Get the response text from the API using the prompt and image data.
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    
    # Display the response on the app
    st.header("Here is the composition")
    st.write(response)
