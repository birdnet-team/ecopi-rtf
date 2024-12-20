import json
import os
import yaml

from dotenv import load_dotenv

load_dotenv()

def load_species_data(project='swamp'):
    # Get the absolute path to the JSON file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'assets', project + '_species_info.json')
    
    with open(file_path) as f:
        data = json.load(f)
        return data
    
def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

API_TOKEN = os.getenv('API_TOKEN')
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')
API_BASE_URL = 'https://api.ecopi.de/api/v0.1/'
SITE_ROOT = '' # '' for dev and '/swamp' for production
SITE_VIEWS_LOG = 'site_views.csv'

# Load the chosen configuration file
config_file = os.getenv('CONFIG_FILE', 'configs/swamp_config.yaml')
config = load_config(config_file)

# Load project configuration from yaml
PROJECT_NAME = config['PROJECT_NAME']
RECORDER_GROUP = config['RECORDER_GROUP']
SPECIES_DATA = load_species_data(project=config['SPECIES_DATA'])
DEPLOYMENT_LAT = config['DEPLOYMENT_LAT']
DEPLOYMENT_LON = config['DEPLOYMENT_LON']
TIMEZONE = config['TIMEZONE']
TIME_FORMAT = config['TIME_FORMAT']
RECORDERS = config['RECORDERS']
MAP_ZOOM_LEVEL = config['MAP_ZOOM_LEVEL']
MAIN_HEADER_IMG_LIST = config['MAIN_HEADER_IMG_LIST']
ABOUT_HEADER_IMG_LIST = config['ABOUT_HEADER_IMG_LIST']
LIVE_STREAM_URL = config['LIVE_STREAM_URL']
DONATION_URL = config['DONATION_URL']
PROJECT_ACRONYM = config['PROJECT_ACRONYM']
PROJECT_MAIN_TITLE = config['PROJECT_MAIN_TITLE']
PROJECT_SUBTITLE = config['PROJECT_SUBTITLE']
PROJECT_SUBTITLE_DESC = config['PROJECT_SUBTITLE_DESC']
PROJECT_GOAL = config['PROJECT_GOAL']
PRIMARY_COLOR = config['PRIMARY_COLOR']
SECONDARY_COLOR = config['SECONDARY_COLOR']
PLOT_PRIMARY_COLOR = config['PLOT_PRIMARY_COLOR']
BUTTON_COLOR = config['BUTTON_COLOR']
LOGO_MOBILE = config['LOGO_MOBILE']
LOGO_DESKTOP = config['LOGO_DESKTOP']
LEARN_MORE_BASE_URL = config['LEARN_MORE_BASE_URL']
FOOTER_LINKS = config['FOOTER_LINKS']
COPYRIGHT_HOLDERS = config['COPYRIGHT_HOLDERS']
FOOTER_TOP_LOGO = config['FOOTER_TOP_LOGO']
FOOTER_BOTTOM_LOGOS = config['FOOTER_BOTTOM_LOGOS']
TEAM_MEMBERS = config['TEAM_MEMBERS']