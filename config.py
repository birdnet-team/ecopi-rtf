import json

def load_api_token():
    with open('auth.json') as f:
        data = json.load(f)
        return data['api-token'] 

API_TOKEN = load_api_token()
API_BASE_URL = 'https://api.ecopi.de/api/v0.1/' #https://api.ecopi.de/api/v0.1/meta/project/{project_name}/detections/recorderspeciescounts/
PROJECT_NAME = 'pam_in_chemnitz'