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
PROJECT_NAME = 'pam_in_chemnitz'
RECORDER_GROUP = 39
SPECIES_DATA = load_species_data(project='amic')
DEPLOYMENT_LAT = 50.832
DEPLOYMENT_LON = 12.924
TIMEZONE = 'Europe/Berlin'
TIME_FORMAT = '24h'
RECORDERS = {
    1: {'id': '0271', 'lat': 42.479723, 'lon': -76.451566, 'habitat': 'Urban'},
    2: {'id': '0829', 'lat': 42.479005, 'lon': -76.454030, 'habitat': 'Urban'},
    3: {'id': '0269', 'lat': 42.476863, 'lon': -76.445881, 'habitat': 'Urban'},
    4: {'id': '0270', 'lat': 42.479265, 'lon': -76.442721, 'habitat': 'Forest'},
}
"""

# SWAMP project configuration
PROJECT_NAME = '099_swamp'
RECORDER_GROUP = 99
SPECIES_DATA = load_species_data(project='swamp')
DEPLOYMENT_LAT = 42.479723
DEPLOYMENT_LON = -76.451566
TIMEZONE = 'America/New_York'
TIME_FORMAT = '12h'
RECORDERS = {
    1: {'id': '0271', 'lat': 42.475, 'lon': -76.445, 'habitat': 'Forest', 'img': 'dummy_recorder.jpg'},
    2: {'id': '0829', 'lat': 42.478, 'lon': -76.451, 'habitat': 'Grassland', 'img': 'dummy_recorder.jpg'},
    3: {'id': '0269', 'lat': 42.469, 'lon': -76.449, 'habitat': 'Wetland', 'img': 'dummy_recorder.jpg'},
    4: {'id': '0270', 'lat': 42.480, 'lon': -76.453, 'habitat': 'Forest', 'img': 'dummy_recorder.jpg'},
    5: {'id': '0272', 'lat': 42.4796, 'lon': -76.4514, 'habitat': 'Pond', 'img': 'swamp_unit_5.jpg'},
    7: {'id': '0274', 'lat': 42.472, 'lon': -76.446, 'habitat': 'Grassland', 'img': 'dummy_recorder.jpg'},
    8: {'id': '0275', 'lat': 42.480, 'lon': -76.457, 'habitat': 'Grassland', 'img': 'dummy_recorder.jpg'},
    9: {'id': '0276', 'lat': 42.476, 'lon': -76.451, 'habitat': 'Urban', 'img': 'dummy_recorder.jpg'},
    10: {'id': '0277', 'lat': 42.4742, 'lon': -76.4488, 'habitat': 'Shrubs and pond', 'img': 'swamp_unit_10.jpg'},

}
