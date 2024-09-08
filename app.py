##Invoice Extractor

from dotenv import load_dotenv

load_dotenv() ##load all env variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

## configuring api key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load gemini pro vision and get response

def get_gemini_response(input, image, prompt):
    ## loading the gemini model
    model=genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
       ## Read the file into bytes
       bytes_data = uploaded_file.getvalue()
       image_parts = [
            {
                "mime_type": uploaded_file.type,  #get the mimi type of the uploaded file
                "data": bytes_data
            }        
       ]
       return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

##initialize our strealit app
st.set_page_config(page_title="Invoice Extractor")
st.header("Gemini Application")
input=st.text_input("Input Prompt:", key="Input")
uploaded_file = st.file_uploader("Choose an image...", type = ["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width = True)

submit = st.button("Tell me about the invoice.")
input_prompt = """
You are an expert in understanding invoices. 
You will receive input images as invoices and 
you will have to answer questions based on input image.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is:")
    st.write(response)
