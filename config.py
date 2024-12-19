import json
import os
import yaml

from dotenv import load_dotenv

load_dotenv()

def load_species_data(project='amic'):
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
PROJECT_NAME = config['project_name']
RECORDER_GROUP = config['recorder_group']
SPECIES_DATA = load_species_data(project=config['species_data'])
DEPLOYMENT_LAT = config['deployment_lat']
DEPLOYMENT_LON = config['deployment_lon']
TIMEZONE = config['timezone']
TIME_FORMAT = config['time_format']
RECORDERS = config['recorders']
MAP_ZOOM_LEVEL = config['map_zoom_level']
MAIN_HEADER_IMG_LIST = config['main_header_img_list']
ABOUT_HEADER_IMG_LIST = config['about_header_img_list']
LIVE_STREAM_URL = config['live_stream_url']
DONATION_URL = config['donation_url']
PROJECT_ACRONYM = config['project_acronym']
PROJECT_MAIN_TITLE = config['project_main_title']
PROJECT_SUBTITLE = config['project_subtitle']
PROJECT_SUBTITLE_DESC = config['project_subtitle_desc']
PROJECT_GOAL = config['project_goal']
PRIMARY_COLOR = config['primary_color']
SECONDARY_COLOR = config['secondary_color']
PLOT_PRIMARY_COLOR = config['plot_primary_color']
BUTTON_COLOR = config['button_color']
LOGO_MOBILE = config['logo_mobile']
LOGO_DESKTOP = config['logo_desktop']
LEARN_MORE_BASE_URL = config['learn_more_base_url']
FOOTER_LINKS = config['footer_links']
COPYRIGHT_HOLDERS = config['copyright_holders']
FOOTER_TOP_LOGO = config['footer_top_logo']
FOOTER_BOTTOM_LOGOS = config['footer_bottom_logos']
TEAM_MEMBERS = config['team_members']