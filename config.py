import json
import os
import yaml
import time
import argparse

from utils.strings import Strings

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
    # Get the absolute path to the YAML file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(base_dir, config_file)
    
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)
    
def make_cache_dir(cache_dir):    
    # Get the absolute path to the cache directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cache_dir = os.path.join(base_dir, cache_dir)
    
    # Create the cache directory if it doesn't exist
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        
    return cache_dir

def make_pwa_manifest(file_path, locale='en'):
    
    strings = Strings(locale, project=PROJECT_ID)
    
    # Get the absolute path to the JSON file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, file_path)
    
    manifest = {
        "name": strings.get('project_main_title'),
        "short_name": PAGE_TITLE,
        "start_url": f"{SITE_ROOT}/",
        "display": "standalone",
        "icons": [
            {
                "src": f"{SITE_ROOT}/assets/icons/{PROJECT_ACRONYM.lower()}_pwa_icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": f"{SITE_ROOT}/assets/icons/{PROJECT_ACRONYM.lower()}_pwa_icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
    } 
    
    # Save the manifest to the file
    with open(file_path, 'w') as f:
        json.dump(manifest, f, indent=4)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Launch the ecoPi-RTF app with specified configuration.')
parser.add_argument('--config_file', type=str, default=os.getenv('CONFIG_FILE', 'configs/swamp_config.yaml'), help='Path to the configuration YAML file.')
parser.add_argument('--site_root', type=str, default=os.getenv('SITE_ROOT', ''), help='Site root for the application.')
parser.add_argument('--port', type=int, default=int(os.getenv('PORT', 8050)), help='Port to run the server on.')
args, unknown = parser.parse_known_args()

# Load the chosen configuration file
config = load_config(args.config_file)

# Load project configuration from yaml
PROJECT_ID = config['PROJECT_ID']
PROJECT_NAME = config['PROJECT_NAME']
PROJECT_START_DATE = config['PROJECT_START_DATE']
RECORDER_GROUP = config['RECORDER_GROUP']
SPECIES_DATA = load_species_data(project=config['SPECIES_DATA'])
DEPLOYMENT_LAT = config['DEPLOYMENT_LAT']
DEPLOYMENT_LON = config['DEPLOYMENT_LON']
TIMEZONE = config['TIMEZONE']
TIME_FORMAT = config['TIME_FORMAT']
DATE_FORMAT = config['DATE_FORMAT']
DEFAULT_SITE_LOCALE = config['DEFAULT_SITE_LOCALE']
RECORDERS = config['RECORDERS']
MAP_ZOOM_LEVEL = config['MAP_ZOOM_LEVEL']
MAIN_HEADER_IMG_LIST = config['MAIN_HEADER_IMG_LIST']
ABOUT_HEADER_IMG_LIST = config['ABOUT_HEADER_IMG_LIST']
LIVE_STREAM_URL = config['LIVE_STREAM_URL']
DONATION_URL = config['DONATION_URL']
PROJECT_ACRONYM = config['PROJECT_ACRONYM']
PRIMARY_COLOR = config['PRIMARY_COLOR']
SECONDARY_COLOR = config['SECONDARY_COLOR']
PLOT_PRIMARY_COLOR = config['PLOT_PRIMARY_COLOR']
BUTTON_COLOR = config['BUTTON_COLOR']
FAVICON = config['FAVICON']
PAGE_TITLE = config['PAGE_TITLE']
LOGO_MOBILE = config['LOGO_MOBILE']
LOGO_DESKTOP = config['LOGO_DESKTOP']
LEARN_MORE_BASE_URL = config['LEARN_MORE_BASE_URL']
PARTNER_STATEMENT = config['PARTNER_STATEMENT']
PARTNER_LOGOS = config['PARTNER_LOGOS']
FOOTER_LINKS = config['FOOTER_LINKS']
COPYRIGHT_HOLDERS = config['COPYRIGHT_HOLDERS']
FOOTER_TOP_LOGO = config['FOOTER_TOP_LOGO']
FOOTER_BOTTOM_LOGOS = config['FOOTER_BOTTOM_LOGOS']
TEAM_MEMBERS = config['TEAM_MEMBERS']
PWA_MANIFEST = config['PWA_MANIFEST']

# Set site root and port from arguments
SITE_ROOT = args.site_root
PORT = args.port

API_TOKEN = os.getenv('API_TOKEN')
OWM_API_KEY = os.getenv('OWM_API_KEY')
API_BASE_URL = 'https://api.ecopi.de/api/v0.1/'
SITE_VIEWS_LOG = 'site_views.csv'
SUPPORTED_SITE_LOCALES = {'English': 'en', 'Deutsch': 'de', 'Italiano': 'it', 'Français': 'fr', 'Čeština': 'cs', 'Spanish': 'es'}
CACHE_DIR = 'cache'