import json

def load_api_token():
    with open('auth.json') as f:
        data = json.load(f)
        return data['api-token'] 

def load_species_data():
    with open('assets/amic_species_info.json') as f:
        data = json.load(f)
        return data

API_TOKEN = load_api_token()
API_BASE_URL = 'https://api.ecopi.de/api/v0.1/' #https://api.ecopi.de/api/v0.1/meta/project/{project_name}/detections/recorderspeciescounts/
PROJECT_NAME = 'pam_in_chemnitz'
SPECIES_DATA = load_species_data()

RECORDERS = {
    '1': '0271',
    '2': '0829',
    '3': '0269',
    '4': '0270'
}