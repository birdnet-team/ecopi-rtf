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
SITE_VIEWS_LOG = 'site_views.csv'

# AMiC project configuration
PROJECT_NAME = 'pam_in_chemnitz'
RECORDER_GROUP = 39
SPECIES_DATA = load_species_data(project='amic')
DEPLOYMENT_LAT = 50.832
DEPLOYMENT_LON = 12.924
TIMEZONE = 'Europe/Berlin'
TIME_FORMAT = '24h'
RECORDERS = {
    1: {'id': '0271', 'lat': 50.850533, 'lon': 12.890730, 'habitat': 'Urban', 'img': 'amic_unit_1.jpg'},
    2: {'id': '0829', 'lat': 50.850231, 'lon': 12.890473, 'habitat': 'Urban', 'img': 'amic_unit_2.jpg'},
    3: {'id': '0269', 'lat': 50.850022, 'lon': 12.890146, 'habitat': 'Urban', 'img': 'amic_unit_3.jpg'},
    4: {'id': '0270', 'lat': 50.849055, 'lon': 12.889994, 'habitat': 'Forest', 'img': 'amic_unit_4.jpg'}
}
MAP_ZOOM_LEVEL = 17
MAIN_HEADER_IMG_LIST = ['amic_main_header_1.jpg']
ABOUT_HEADER_IMG_LIST = ['amic_about_header_1.jpg']
LIVE_STREAM_URL = ''
DONATION_URL = ''
PROJECT_MAIN_TITLE = 'AMiC: Acoustic Monitoring in Chemnitz'
PROJECT_SUBTITLE = 'AI-powered acoustic monitoring'
PROJECT_SUBTITLE_DESC = 'We listen to the sounds of birds and investigate how traffic noise impacts their natural behavior.'
PRIMARY_COLOR = '#385B75'
SECONDARY_COLOR = '#2c3b47'
PLOT_PRIMARY_COLOR = '#385B75'
BUTTON_COLOR = '#385B75'
LOGO_MOBILE = 'amic_logo_short.png'
LOGO_DESKTOP = 'amic_logo_wide.png'
LEARN_MORE_BASE_URL = 'https://ebird.org/species/'
FOOTER_LINKS = {
    "Site Links": [
        {"name": "Home", "href": f"{SITE_ROOT}/"},
        {"name": "Detections", "href": f"{SITE_ROOT}/detections"},
        {"name": "Recording units", "href": f"{SITE_ROOT}/recorder/1"},
        {"name": "About the project", "href": f"{SITE_ROOT}/about"},
        {"name": "Contact", "href": f"{SITE_ROOT}/about#about-contact"},
    ],
    "Botanical Garden Chemnitz": [
        {"name": "About", "href": "https://www.chemnitz.de/en/living-in-chemnitz/leisure-time/botanical-garden", "target": "_blank"},
        {"name": "History", "href": "https://www.chemnitz.de/en/living-in-chemnitz/leisure-time/botanical-garden/history", "target": "_blank"},
        {"name": "School Biology Center", "href": "https://www.chemnitz.de/en/living-in-chemnitz/leisure-time/botanical-garden/school-biology-centre", "target": "_blank"},
        {"name": "Park Map", "href": "https://d2vw8mc5mcb3gm.cloudfront.net/fileadmin/chemnitz/media/leben-in-chemnitz/freizeit/botanischer_garten/botanischer_garten_parkplan.pdf", "target": "_blank"},
        
    ],
    "OekoFor": [
        {"name": "OekoFor", "href": "https://www.oekofor.de/en/", "target": "_blank"},
        {"name": "About us", "href": "https://www.oekofor.de/en/#about", "target": "_blank"},
        {"name": "Services", "href": "https://www.oekofor.de/en/#services", "target": "_blank"},
        {"name": "ecoPi", "href": "https://www.oekofor.de/en/portfolio/erfassungstechnik_en/", "target": "_blank"},
        {"name": "Contact", "href": "https://www.oekofor.de/en/#contact", "target": "_blank"},
        
    ],
    "Yang Center": [
        {"name": "Our values", "href": "https://www.birds.cornell.edu/ccb/our-values/", "target": "_blank"},
        {"name": "Research", "href": "https://www.birds.cornell.edu/ccb/research/", "target": "_blank"},
        {"name": "Technology", "href": "https://www.birds.cornell.edu/ccb/technology/", "target": "_blank"},
        {"name": "Education", "href": "https://www.birds.cornell.edu/ccb/education/", "target": "_blank"},
        {"name": "Publications", "href": "https://www.birds.cornell.edu/ccb/publications/", "target": "_blank"},
    ],
    "TU Chemnitz": [
        {"name": "University", "href": "https://www.tu-chemnitz.de/index.html.en", "target": "_blank"},
        {"name": "Degree programs", "href": "https://www.tu-chemnitz.de/studierendenservice/zsb/studiengaenge/en/", "target": "_blank"},
        {"name": "International Office", "href": "https://www.tu-chemnitz.de/international/index.php.en", "target": "_blank"},
        {"name": "Research", "href": "https://www.tu-chemnitz.de/forschung/index.php.en", "target": "_blank"},
        {"name": "Computer Science", "href": "https://www.tu-chemnitz.de/informatik/index.php.en", "target": "_blank"},
        
    ],
    "About": [
        {"name": "Legal Notice", "href": "https://www.tu-chemnitz.de/tu/impressum.html", "target": "_blank"},
        {"name": "Privacy Policy", "href": "https://www.tu-chemnitz.de/tu/datenschutz.html", "target": "_blank"},
        {"name": "Accessibility", "href": "https://www.tu-chemnitz.de/tu/barrierefreiheit.html", "target": "_blank"},
        {"name": "Media Data", "href": "https://www.tu-chemnitz.de/transfer/fundraising/mediadaten.php", "target": "_blank"},
    ]
}
COPYRIGHT_HOLDERS = "TU Chemnitz"
FOOTER_TOP_LOGO = 'chemnitz_logo_white.png'
FOOTER_BOTTOM_LOGOS = ['oekofor_logo_white.png', 'yang_logo_white.png', 'tuc_logo_white.png']

# Neeracher Ried project configuration
"""
PROJECT_NAME = '017_neerach_ried'
RECORDER_GROUP = 45
SPECIES_DATA = load_species_data(project='neeracherried')
DEPLOYMENT_LAT = 47.500
DEPLOYMENT_LON = 8.4790
TIMEZONE = 'Europe/Berlin'
TIME_FORMAT = '24h'
RECORDERS = {
    1: {'id': '0357', 'lat': 47.50141, 'lon': 8.48344, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'}, 
    2: {'id': '0368', 'lat': 47.50364, 'lon': 8.483333, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'}, 
    3: {'id': '0518', 'lat': 47.50269, 'lon': 8.48399, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    4: {'id': '0517', 'lat': 47.50026, 'lon': 8.48248, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    5: {'id': '0525', 'lat': 47.50249, 'lon': 8.48239, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    6: {'id': '0523', 'lat': 47.50016, 'lon': 8.48449, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    7: {'id': '0516', 'lat': 47.50095, 'lon': 8.48666, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    8: {'id': '0513', 'lat': 47.50006, 'lon': 8.48592, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    9: {'id': '0358', 'lat': 47.50255, 'lon': 8.48767, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    10: {'id': '0526', 'lat': 47.50372, 'lon': 8.48661, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    11: {'id': '0524', 'lat': 47.50464, 'lon': 8.48788, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
    12: {'id': '0378', 'lat': 47.503143, 'lon': 8.488629, 'habitat': 'Raised bog', 'img': 'dummy_recorder.jpg'},
}
MAP_ZOOM_LEVEL = 16
MAIN_HEADER_IMG_LIST = ['blnr_main_header_1.jpg']
ABOUT_HEADER_IMG_LIST = ['blnr_about_header_1.jpg']
LIVE_STREAM_URL = ''
DONATION_URL = 'https://www.birdlife.ch/en/content/donations'
PROJECT_MAIN_TITLE = 'Neeracherried Acoustic Monitoring Project'
PROJECT_SUBTITLE = 'AI-powered acoustic monitoring'
PROJECT_SUBTITLE_DESC = 'We listen to the sounds of the birds in Neeracherried and track species diversity over large spatio-temporal scales.'
PRIMARY_COLOR = '#6cae3d'
SECONDARY_COLOR = '#3b6da8'
PLOT_PRIMARY_COLOR = '#486f9c'
BUTTON_COLOR = '#6cae3d'
LOGO_MOBILE = 'birdlife_ch_logo_bird.png'
LOGO_DESKTOP = 'birdlife_ch_logo_bird.png'
LEARN_MORE_BASE_URL = 'https://ebird.org/species/'
FOOTER_LINKS = {
    "Site Links": [
        {"name": "Home", "href": f"{SITE_ROOT}/"},
        {"name": "Detections", "href": f"{SITE_ROOT}/detections"},
        {"name": "Recording units", "href": f"{SITE_ROOT}/recorder/1"},
        {"name": "About the project", "href": f"{SITE_ROOT}/about"},
        {"name": "Contact", "href": f"{SITE_ROOT}/about#about-contact"},
    ],
    "BirdLife": [
        {"name": "Projects", "href": "https://www.birdlife.ch/en/content/projects", "target": "_blank"},
        {"name": "Visitor centers", "href": "https://www.birdlife.ch/en/content/visitor-centres-0", "target": "_blank"},
        {"name": "Membership", "href": "https://www.birdlife.ch/en/membership", "target": "_blank"},
        {"name": "Support our work", "href": "https://www.birdlife.ch/en/content/support-our-work", "target": "_blank"},
    ],
    "OekoFor": [
        {"name": "About us", "href": "https://www.oekofor.de/en/#about", "target": "_blank"},
        {"name": "Services", "href": "https://www.oekofor.de/en/#services", "target": "_blank"},
        {"name": "ecoPi", "href": "https://www.oekofor.de/en/portfolio/erfassungstechnik_en/", "target": "_blank"},
        {"name": "Contact", "href": "https://www.oekofor.de/en/#contact", "target": "_blank"},
        
    ],
    "Yang Center": [
        {"name": "Our values", "href": "https://www.birds.cornell.edu/ccb/our-values/", "target": "_blank"},
        {"name": "Research", "href": "https://www.birds.cornell.edu/ccb/research/", "target": "_blank"},
        {"name": "Technology", "href": "https://www.birds.cornell.edu/ccb/technology/", "target": "_blank"},
        {"name": "Education", "href": "https://www.birds.cornell.edu/ccb/education/", "target": "_blank"},
        {"name": "Publications", "href": "https://www.birds.cornell.edu/ccb/publications/", "target": "_blank"},
    ],
    "TU Chemnitz": [
        {"name": "University", "href": "https://www.tu-chemnitz.de/index.html.en", "target": "_blank"},
        {"name": "Degree programs", "href": "https://www.tu-chemnitz.de/studierendenservice/zsb/studiengaenge/en/", "target": "_blank"},
        {"name": "International Office", "href": "https://www.tu-chemnitz.de/international/index.php.en", "target": "_blank"},
        {"name": "Research", "href": "https://www.tu-chemnitz.de/forschung/index.php.en", "target": "_blank"},
        {"name": "Computer Science", "href": "https://www.tu-chemnitz.de/informatik/index.php.en", "target": "_blank"},
        
    ],
    "About": [
        {"name": "Legal Notice", "href": "https://www.tu-chemnitz.de/tu/impressum.html", "target": "_blank"},
        {"name": "Privacy Policy", "href": "https://www.tu-chemnitz.de/tu/datenschutz.html", "target": "_blank"},
        {"name": "Accessibility", "href": "https://www.tu-chemnitz.de/tu/barrierefreiheit.html", "target": "_blank"},
    ]
}
COPYRIGHT_HOLDERS = "TU Chemnitz"
FOOTER_TOP_LOGO = 'birdlife_ch_logo_white.png'
FOOTER_BOTTOM_LOGOS = ['oekofor_logo_white.png', 'yang_logo_white.png', 'tuc_logo_white.png']
"""

# SWAMP project configuration
"""
PROJECT_NAME = '099_swamp'
RECORDER_GROUP = 99
SPECIES_DATA = load_species_data(project='swamp')
DEPLOYMENT_LAT = 42.479723
DEPLOYMENT_LON = -76.451566
TIMEZONE = 'America/New_York'
TIME_FORMAT = '12h'
RECORDERS = {
    1: {'id': '0271', 'lat': 42.4786, 'lon': -76.4407, 'habitat': 'Shrubs & trees', 'img': 'swamp_unit_1.jpg'},
    2: {'id': '0829', 'lat': 42.4768, 'lon': -76.4396, 'habitat': 'Shrubs & meadow', 'img': 'swamp_unit_2.jpg'},
    3: {'id': '0269', 'lat': 42.4769, 'lon': -76.4426, 'habitat': 'Shrubs & meadow', 'img': 'swamp_unit_3.jpg'},
    4: {'id': '0270', 'lat': 42.4769, 'lon': -76.4442, 'habitat': 'Shrubs & trees', 'img': 'swamp_unit_4.jpg'},
    5: {'id': '0272', 'lat': 42.4796, 'lon': -76.4514, 'habitat': 'Feeder garden & pond', 'img': 'swamp_unit_5.jpg'},
    7: {'id': '0275', 'lat': 42.4801, 'lon': -76.4543, 'habitat': 'Trees & pond', 'img': 'swamp_unit_7.jpg'},
    8: {'id': '0276', 'lat': 42.4782, 'lon': -76.4547, 'habitat': 'Forest', 'img': 'swamp_unit_8.jpg'},
    9: {'id': '0274', 'lat': 42.4753, 'lon': -76.4451, 'habitat': 'Forest clearing', 'img': 'swamp_unit_9.jpg'},
    10: {'id': '0277', 'lat': 42.4742, 'lon': -76.4488, 'habitat': 'Shrubs and pond', 'img': 'swamp_unit_10.jpg'},

}
MAP_ZOOM_LEVEL = 15
MAIN_HEADER_IMG_LIST = ['ssw_main_header_1.jpg', 'ssw_main_header_2.jpg']
ABOUT_HEADER_IMG_LIST = ['ssw_about_header_1.jpg', 'ssw_about_header_2.jpg', 'ssw_about_header_3.jpg', 'ssw_about_header_4.jpg', 'ssw_about_header_5.jpg']
LIVE_STREAM_URL = 'https://birdnetlive.duckdns.org/ssw'
DONATION_URL = 'https://give.birds.cornell.edu/page/132162/donate/1?ea.tracking.id=ENR'
PROJECT_MAIN_TITLE = 'SWAMP: Sapsucker Woods Acoustic Monitoring Project'
PROJECT_SUBTITLE = 'AI-powered acoustic monitoring'
PROJECT_SUBTITLE_DESC = 'We listen to the sounds of the animals in Sapsucker Woods and track species diversity over large spatio-temporal scales.'
PRIMARY_COLOR = '#b31b1b'
SECONDARY_COLOR = '#2e261f'
PLOT_PRIMARY_COLOR = '#385B75'
BUTTON_COLOR = '#36824b'
LOGO_MOBILE = 'clo_swamp_short_mobile_horizontal_color.png'
LOGO_DESKTOP = 'clo_swamp_short_horizontal_color.png'
LEARN_MORE_BASE_URL = 'https://www.allaboutbirds.org/guide/'
FOOTER_LINKS = {
    "Site Links": [
        {"name": "Home", "href": f"{SITE_ROOT}/"},
        {"name": "Detections", "href": f"{SITE_ROOT}/detections"},
        {"name": "Recording units", "href": f"{SITE_ROOT}/recorder/1"},
        {"name": "About the project", "href": f"{SITE_ROOT}/about"},
        {"name": "Contact", "href": f"{SITE_ROOT}/about#about-contact"},
    ],
    "Yang Center": [
        {"name": "Our values", "href": "https://www.birds.cornell.edu/ccb/our-values/", "target": "_blank"},
        {"name": "Research", "href": "https://www.birds.cornell.edu/ccb/research/", "target": "_blank"},
        {"name": "Technology", "href": "https://www.birds.cornell.edu/ccb/technology/", "target": "_blank"},
        {"name": "Education", "href": "https://www.birds.cornell.edu/ccb/education/", "target": "_blank"},
        {"name": "Publications", "href": "https://www.birds.cornell.edu/ccb/publications/", "target": "_blank"},
    ],
    "Explore More": [
        {"name": "Bird Cams", "href": "https://www.allaboutbirds.org/cams/", "target": "_blank"},
        {"name": "Birds of the World", "href": "https://birdsoftheworld.org/bow/home", "target": "_blank"},
        {"name": "eBird Status and Trends", "href": "https://science.ebird.org/status-and-trends", "target": "_blank"},
        {"name": "Our Youtube Videos", "href": "https://www.youtube.com/labofornithology", "target": "_blank"},
    ],
    "Lifelong Learning": [
        {"name": "Online Courses", "href": "https://academy.allaboutbirds.org/", "target": "_blank"},
        {"name": "Bird Walks & Events", "href": "https://www.birds.cornell.edu/home/visit/events/", "target": "_blank"},
        {"name": "Spring Field Ornithology", "href": "https://academy.allaboutbirds.org/product/spring-field-ornithology-northeast/", "target": "_blank"},
        {"name": "K–12 Education", "href": "https://www.birds.cornell.edu/k12", "target": "_blank"},
    ],
    "Support Our Cause": [
        {"name": "Join the Lab", "href": "https://join.birds.cornell.edu/page/150611/donate/1?ea.tracking.id=WXXXXX14C", "target": "_blank"},
        {"name": "Donate", "href": "https://give.birds.cornell.edu/page/132162/donate/1?ea.tracking.id=ENR", "target": "_blank"},
        {"name": "Monthly Giving", "href": "https://give.birds.cornell.edu/page/99134/donate/1?ea.tracking.id=BCF", "target": "_blank"},
        {"name": "Membership Services", "href": "https://www.birds.cornell.edu/home/members/", "target": "_blank"},
        {"name": "Shop for Our Cause", "href": "https://www.birds.cornell.edu/home/shop-for-our-cause/", "target": "_blank"},
    ],
    "About": [
        {"name": "Cornell Lab of Ornithology", "href": "http://birds.cornell.edu/", "target": "_blank"},
        {"name": "Web Accessibility Assistance", "href": "https://www.birds.cornell.edu/home/web-accessibility-assistance/", "target": "_blank"},
        {"name": "Privacy Policy", "href": "https://privacy.cornell.edu/information-use-cornell", "target": "_blank"},
        {"name": "Terms of Use", "href": "https://www.birds.cornell.edu/home/terms-of-use/", "target": "_blank"},
    ],
}
COPYRIGHT_HOLDERS = "Cornell University"
FOOTER_TOP_LOGO = 'yang_logo_white.png'
FOOTER_BOTTOM_LOGOS = ['cornell-logo-white.png']
"""