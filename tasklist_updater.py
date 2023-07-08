# import pandas as pd
from Google import Create_Service, convert_to_RFC_datetime

CLIENT_SECRET_FILE = 'client_secret_file.json'
API_NAME = 'tasks'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/tasks']

#print(CLIENT_SECRET_FILE)

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

#print(service)

mainTasklistId = 'ZHBMcEhtSlRLSnNWcWpJcQ'



"""
Insert Method
"""

title = ''
notes = ''
due = ''
status = 'needsAction'
deleted = False
response = ''


def post_notes(item):
    response = service.tasks().insert(
        tasklist=mainTasklistId,
        body=construct_request_body(item)
    ).execute()
    print(response)

    

def construct_request_body(title, notes=None, due=None, status='needsAction', deleted=False):
    try:
        request_body = {
        'title': title,
        'notes': notes,
        'due': due,
        'deleted': deleted,
        'status': status
        }
        return request_body
    except Exception:
        return None