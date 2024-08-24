import re
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text):
    """
    Clean a given text by removing non-printable characters and normalizing whitespace.
    1. Removes non-ASCII characters, which may cause encoding issues.
    2. Normalizes whitespace by replacing multiple spaces with a single space.
    3. Strips leading and trailing whitespace for consistency.
    4. Removes urls as they can introduce security vulnerabilities & formatting issues.
    5. Removes image markdowns, which are unnecessary for this task.
    """
    
    if not isinstance(text, str):  
        text = str(text)  
    # Remove non-printable characters and excessive whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove image markdowns
    text = re.sub(r'https?://\S+', '', text)  # Remove URLs
    
    return text.strip()


def clean_issues_data(issues):
    """
    Clean the issues data to ensure proper encoding and formatting.
    1. Converts data to strings and strips any leading or trailing whitespace.
    2. Ensures the comments field is an integer, avoiding issues with non-integer data.
    3. Cleans up the body and title fields using the clean_text function.
    """
    cleaned_issues = []
    for issue in issues:
        cleaned_issue = {}

        # Extract and clean metadata
        cleaned_issue["user"] = {
            "login": str(issue.get("user", {}).get("login", "")).strip()
        }
        cleaned_issue["comments"] = int(issue.get("comments", 0))
        cleaned_issue["body"] = str(issue.get("body", "")).strip()
        cleaned_issue["labels"] = [str(label).strip() for label in issue.get("labels", [])]
        cleaned_issue["created_at"] = str(issue.get("created_at", "")).strip()

        # Clean title and body
        cleaned_issue["title"] = str(issue.get("title", "")).strip()
        cleaned_issue["body"] = clean_text(issue.get("body", ""))

        cleaned_issues.append(cleaned_issue)
    # Add logging
    logging.info(f"Cleaned issues")
    
    return cleaned_issues