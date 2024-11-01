import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.generic_loader import load_content

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo")

# Set up the Streamlit app layout
st.set_page_config(page_title="Web Page Summarizer", layout="centered")
st.markdown(
    """
    <style>
        body {
            background-color: #f0f4f8;
            color: #333;
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            color: #007bff;
            font-size: 2em;
            margin-bottom: 20px;
        }
        .button {
            background-color: #007bff;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .summary {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 10px;
        }
        .copy-button {
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-top: 5px;
        }
        .copy-button:hover {
            background-color: #218838;
        }
        .download-button {
            background-color: #17a2b8;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            cursor: pointer;
            transition: background-color 0.3s;
            margin-top: 5px;
        }
        .download-button:hover {
            background-color: #138496;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
st.markdown("<h1 class='title'>Web Page Summarizer</h1>", unsafe_allow_html=True)

# Brief description of the summarizer
st.write("""
This application allows you to generate concise summaries of web pages or any text you provide. 
Simply enter a URL or paste your text, and the app will return a bullet-point summary to help you grasp the main ideas quickly.
""")

# Input options: URL or Text
input_option = st.radio("Choose input method:", ("URL", "Text"))

if input_option == "URL":
    url = st.text_input("Enter URL:", "https://learnwithhasan.com/create-ai-agents-with-python/")
else:
    url = ""
    text_input = st.text_area("Paste your text here:", height=150)

# Summarize button
if st.button("Summarize", key='summarize'):
    if input_option == "URL" and url:
        try:
            # Load content from the given URL
            content = load_content(url).content
            
            # Create the summarization prompt
            summarize_prompt = f"Generate a bullet point summary for the following: {content}"
            
        except Exception as e:
            st.error(f"Error loading content from URL: {e}")
            content = None
    elif input_option == "Text" and text_input:
        content = text_input
        summarize_prompt = f"Generate a bullet point summary for the following: {content}"
    else:
        st.error("Please enter a valid input.")

    if content:
        try:
            # Generate the summary using the language model
            generated_text = llm_instance.generate_response(prompt=summarize_prompt)

            # Display the summary
            st.subheader("Generated Summary:")
            summary_box = st.empty()  # Create an empty container for the summary
            summary_box.markdown(f"<div class='summary'>{generated_text}</div>", unsafe_allow_html=True)

            # Copy button for the generated text
            if st.button("Copy Summary"):
                # Use Streamlit's session state to manage clipboard copying
                st.markdown(
                    f"<script>navigator.clipboard.writeText(`{generated_text}`); alert('Summary copied to clipboard!');</script>",
                    unsafe_allow_html=True
                )

            # Download button for the generated text
            st.download_button(
                label="Download Summary",
                data=generated_text,
                file_name="summary.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred while generating the summary: {e}")
