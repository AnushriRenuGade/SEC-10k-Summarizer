PATH = "C:\\Users\anush\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts"

import streamlit as st
from google.cloud import aiplatform
from PIL import Image
import google.generativeai as genai
import os
import pdfplumber

genai.configure(api_key="AIzaSyCz--z1p1aPPYowM6QXvPRRQk7ZBnaMmmo")

#model = genai.GenerativeModel("gemini-1.5-flash")
#response = model.generate_content("Write a very short story about a crypto")
#print(response.text)

#Function to extract text from pdf using pdfplumber
def extract_text_from_pdf(pdf_file):
    text = ''
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

#Function to get a summary of text
def summarize_text(text):
    try: 
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([f'Please summarize the following text:\n\n{text}'])
        return response.text
    except Exception as e:
        return f'An error occured: {e}'


#Function to question the text using Gemini-pro API
def question_text(text, question):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([f'Please answer the following question based on the provided text:\n\nText: {text}\n\nQuestion: {question}'])
        return response.text
    except Exception as e:
        return f'An error occured: {e}'

#Extract text from pdf
#text = extract_text_from_pdf("C:/Users/anush/Downloads/Chipotle_2023_10k.pdf")
#text

#Summarize text using summarize_text function
#summary = summarize_text(text)
#print(summary)

#Ask and answer a question based on the text using question_text
#answer = question_text(text, 'How did Chipotle perform in 2023 compared to 2022?')
#print(answer)

#Streamlit app
def main():
    st.title("PDF Summarizer with Gemini")

    image = Image.open('Gemini_Image.png')
    st.image(image, use_column_width='always')

    uploaded_file = st.file_uploader('Upload a PDF file', type='pdf')

    if uploaded_file is not None:
        #extract text from uploaded pdf
        text = extract_text_from_pdf(uploaded_file)

        #limit the diplayed text to 500 characterss (dimensions of display text)
        display_text = text[:500] + ('...' if len(text) > 500 else '')

        #display the extracted text
        st.subheader("Extracted Text")
        st.text_area("Text from PDF", display_text, height = 300)

        #Get a summary
        if st.button ("Get Summary"):
            summary = summarize_text(text)
            st.subheader("Summary")
            st.write(summary)

        #Ask a question
        question = st.text_input("Enter your question about the text")
        if st.button("Get Answer"):
            if question:
                answer = question_text(text, question)
                st.subheader("Answer")
                st.write(answer)
            else:
                st.warning("Please enter a question to get an answer")

if __name__ == "__main__":
    main()
            
    

    
