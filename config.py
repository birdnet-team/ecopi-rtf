import json
import os

from dotenv import load_dotenv

load_dotenv()

def load_species_data(project='amic'):
    # Get the absolute path to the JSON file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'assets', project + '_species_info.json')
    
    with open(file_path) as f:
        data = json.load(f)
        return data

API_TOKEN = os.getenv('API_TOKEN')
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')
API_BASE_URL = 'https://api.ecopi.de/api/v0.1/'
SITE_ROOT = '' # '' for dev and '/swamp' for production

# AMiC project configuration
"""
PROJECT_NAME = 'pam_in_chemnitz' #'099_swamp'#
SPECIES_DATA = load_species_data(project='amic')
DEPLOYMENT_LAT = 50.832
DEPLOYMENT_LON = 12.924
TIMEZONE = 'Europe/Berlin'
RECORDERS = {
    1: {'id': '0271', 'lat': 42.479723, 'lon': -76.451566},
    2: {'id': '0829', 'lat': 42.479005, 'lon': -76.454030},
    3: {'id': '0269', 'lat': 42.476863, 'lon': -76.445881},
    4: {'id': '0270', 'lat': 42.479265, 'lon': -76.442721}
}
"""

# SWAMP project configuration
PROJECT_NAME = '099_swamp'
SPECIES_DATA = load_species_data(project='swamp')
DEPLOYMENT_LAT = 42.479723
DEPLOYMENT_LON = -76.451566
TIMEZONE = 'America/New_York'
RECORDERS = {
    1: {'id': '0271', 'lat': 42.479723, 'lon': -76.451566},
    2: {'id': '0829', 'lat': 42.479005, 'lon': -76.454030},
    3: {'id': '0269', 'lat': 42.476863, 'lon': -76.445881},
    4: {'id': '0270', 'lat': 42.479265, 'lon': -76.442721},
    5: {'id': '0272', 'lat': 42.479723, 'lon': -76.451566},
    6: {'id': '0273', 'lat': 42.479005, 'lon': -76.454030},
    7: {'id': '0274', 'lat': 42.476863, 'lon': -76.445881},
    8: {'id': '0275', 'lat': 42.479265, 'lon': -76.442721},
    9: {'id': '0276', 'lat': 42.479723, 'lon': -76.451566},
}
