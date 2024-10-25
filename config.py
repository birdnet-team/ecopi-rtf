import json
import os

from dotenv import load_dotenv

load_dotenv()

def load_species_data():
    with open('assets/amic_species_info.json') as f:
        data = json.load(f)
        return data

API_TOKEN = os.getenv('API_TOKEN')
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')
API_BASE_URL = 'https://api.ecopi.de/api/v0.1/' #https://api.ecopi.de/api/v0.1/meta/project/{project_name}/detections/recorderspeciescounts/
PROJECT_NAME = 'pam_in_chemnitz'
SPECIES_DATA = load_species_data()
DEPLOYMENT_LAT = 50.832
DEPLOYMENT_LON = 12.924
TIMEZONE = 'Europe/Berlin'

RECORDERS = {
    1: {'id': '0271', 'lat': 42.479723, 'lon': -76.451566},
    2: {'id': '0829', 'lat': 42.479005, 'lon': -76.454030},
    3: {'id': '0269', 'lat': 42.476863, 'lon': -76.445881},
    4: {'id': '0270', 'lat': 42.479265, 'lon': -76.442721}
}