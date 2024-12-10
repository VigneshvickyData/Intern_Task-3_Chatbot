import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# set ApI key directly
GEMINI_API_KEY = "GEMINI_API_KEY"   # Replace with your Gemini API key
if not GEMINI_API_KEY:
    st.error("Please provide a valid GEMINI_API_KEY.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")    


# Get response for text input
def get_gemini_response(prompt):
    try:
        with st.spinner("Generating response..."):
            response = gemini_model.generate_content(prompt)
            return response.text
    except Exception as e:
        st.error("An error occurred while processing the text.")
        return f"Technical Details: {e}"
        

# function to analysis image and generate a response
def analyze_image(image_file):
    try:
        with st.spinner("Analyzing image..."):
            image_data = image_file.getvalue() # get image bytes
            image = Image.open(io.BytesIO(image_data)) # open the image using PIL

            # Validate image format
            if image.format not in ["JPEG","PNG"]:
                return "Unsupported image format. Please upload a JPEG or PNG image."
            
            # send image for analysis using gemini multimodal API
            response = gemini_model.generate_content(
                [
                    {"mime_type": "image/jpeg", "data": image_data},
                    {"text": "Describe the content of this image."}
                ]
            )
            return response.text
    except Exception as e:
        st.error("An error occurred while analyzing the image.")
        return f"Technical Details: {e}"
    

# Streamlit UI
st.set_page_config(page_title="Multi-model Chatbot", layout="wide")
st.title("Multi-model Chatbot")

# Sidebar with instructions
st.sidebar.header("Instructions")
st.sidebar.markdown(
    """
    - **Text Input**: Enter a prompt to get a response from Gemini AI.
    - **Image Input**: Upload a JPEG or PNG image for analysis.
    - **API Key**: Ensure the correct API key is set for the application.
    """
)
st.sidebar.info("Gemini Model: gemini-1.5-flash")

# Text Input Section
st.header("Text Input")
input_text = st.text_area(
    "Enter your prompt (max 1000 characters):",
    max_chars=1000,
    help="Type a question or command for the chatbot to respond to."
)

# add a character counter
if input_text:
    st.caption(f"Characters used: {len(input_text)}/1000")

if st.button("Submit Text"):
    if not input_text:
        st.warning("Please enter a prompt.")
    else:
        gemini_response = get_gemini_response(input_text)
        st.subheader("MMC-Bot Response:")
        st.write(gemini_response)

# Image Input section
st.header("Image Input")  
uploaded_image = st.file_uploader(
    "Upload an image for analysis", type=["jpg", "jpeg", "png"], help="Supported formats: JPG, JPEG, PNG."
)

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Images", use_column_width=True)
    if st.button("Analyze Image"):
        image_response = analyze_image(uploaded_image)
        st.subheader("MMC-Bot Response:")
        st.write(image_response)

