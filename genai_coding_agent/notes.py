from keybert import KeyBERT
from langchain_core.tools import tool
import datetime
from datetime import datetime
import os
import re
import logging

# Initialize the KeyBERT model
kw_model = KeyBERT()

def extract_keywords(text, max_keywords=2):
    """
    Extracts a limited number of keywords from the text.
    """
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=max_keywords)
    return [kw[0] for kw in keywords]

def sanitize_filename(text):
    """
    Sanitizes the input text to be a valid filename by replacing spaces and special characters.
    Also truncates the filename to a max length if necessary.
    """
    # Replace spaces with underscores and remove special characters
    sanitized = re.sub(r'\W+', '_', text)
    # Truncate the filename to the specified max_length
    return sanitized

@tool
def note_tool(note, question_prompt):
    """
    A tool that allows users to save a note to a uniquely named file based on the extracted keywords from the question prompt.
    Args:
        note (str): The note to save.
        question_prompt (str): The prompt used to generate the note.
    """
    # Extract keywords from the question prompt
    keywords = extract_keywords(question_prompt)
    
    # Generate a filename based on the sanitized keywords
    base_filename = sanitize_filename(keywords[0])
    ts = datetime.now().strftime("%Y%m%d")
    
    filename = f"{base_filename}_{ts}.txt"

    # Define the file path
    file_path = os.path.join("/Users/sjr11/Work/SelfLearning/GenAI Coding Agent/data/processed/", filename)

    # Save the note to the file
    with open(file_path, "w") as f:
        f.write(note)

    logging.info(f"Note saved as {filename}")


# if __name__ == "__main__":
#     ques = "What is the most common issue in Flask-Web-App-Tutorial? Make a summary note of these issues."
#     file_name_kw = extract_keywords(text=ques, max_keywords=2)
#     print(file_name_kw)
