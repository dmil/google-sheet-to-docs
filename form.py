import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import io
import os
from reportlab.pdfgen import canvas
import logging
logging.getLogger().setLevel(logging.DEBUG)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"
from pprint import pprint

# Set the Google Form ID and the output directory
FORM_ID = '16qRuI8Tw9NdpQE48i3lk0gAAU7E3by35hzdF-mZ7LUk'
output_dir = 'output'

# Authenticate with Google APIs
creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/drive'])
service = build('forms', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

# Get the form responses
response = service.forms().get(formId=FORM_ID).execute()
form_title = response['info']['title']
questions_list = response['items']

response_list = service.forms().responses().list(formId=FORM_ID).execute()


question_texts = {q['questionItem']['question']['questionId']:q['title'] for q in questions_list}


for response in reversed(response_list['responses']):
    md = [] # markdown lines
    answers = response['answers']
    name = answers[questions_list[8]['questionItem']['question']['questionId']]['textAnswers']['answers'][0]['value']
    email = response['respondentEmail']
    md.append(f"#{name} ({email})")
    for question in questions_list:
        question_id = question['questionItem']['question']['questionId']
        md += ["\n", f"## {question['title']}"]

        if answers.get(question_id):
            md.append(answers[question_id]['textAnswers']['answers'][0]['value'])
    
    markdown = "\n".join(md)
    filepath = f"output/{name}.md"
    if os.path.exists(filepath):
        filepath = filepath.replace(".md", "_2.md")
        print(f"ERROR: File already exists {filepath}")

    with open(filepath, "w") as f:
        f.write(markdown)
    print("========================")
    