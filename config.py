import json
import os

from dotenv import load_dotenv

load_dotenv()

def load_species_data():
    with open('assets/amic_species_info.json') as f:
        data = json.load(f)
        return data

API_TOKEN = os.getenv('API_TOKEN')
API_BASE_URL = 'https://api.ecopi.de/api/v0.1/' #https://api.ecopi.de/api/v0.1/meta/project/{project_name}/detections/recorderspeciescounts/
PROJECT_NAME = 'pam_in_chemnitz'
SPECIES_DATA = load_species_data()
DEPLOYMENT_LAT = 50.832
DEPLOYMENT_LON = 12.924
TIMEZONE = 'Europe/Berlin'

RECORDERS = {
    '1': '0271',
    '2': '0829',
    '3': '0269',
    '4': '0270'
}