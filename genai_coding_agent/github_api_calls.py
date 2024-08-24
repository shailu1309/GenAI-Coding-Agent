import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document
import re
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#private imports
from text_preprocessing import clean_issues_data, clean_text

load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')



def fetch_github(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {github_token}"
        }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        logging.info(f"Error fetching data from Github: {response.status_code}")
        return []


def load_issues(issues):
    docs = []
    for issue_num in range(len(issues)):
        metadata = {
            "author": issues[issue_num]["user"]["login"],
            "comments": issues[issue_num]["comments"],
            "body": issues[issue_num]["body"],
            "labels": issues[issue_num]["labels"],
            "created_at": issues[issue_num]["created_at"]
        }
        data = issues[issue_num]["title"] 
        if issues[issue_num]["body"]:
            data += issues[issue_num]["body"]
            
        # Decode the data to ensure consistency and avoid encoding issues
        data = data.encode('utf-8').decode('utf-8')
        
        doc = Document(page_content=data, metadata=metadata)
        docs.append(doc)
             
    return docs
    

def clean_and_load_issues(owner, repo):
    issues = fetch_github(owner, repo, "issues")
    cleaned_issues = clean_issues_data(issues)
    docs = load_issues(cleaned_issues)
    logging.info(f"Loaded {len(docs)} issues")
    return docs
    
    
if __name__ == "__main__":
    x = clean_and_load_issues("techwithtim", "Flask-Web-App-Tutorial")