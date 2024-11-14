from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH

from utils import data_processor as dp

def detections_table(species_code):
    
    stats = dp.get_species_stats(species_code)
    
    # sample stats data
    # [{'species_code': 'eurrob1', 'has_audio': True, 'datetime': '2024/04/11 - 07:06', 'url_media': 'https://api.ecopi.de/api/v0.1/detections/media/97375c36-4e64-4cd5-ba1a-4fb39f93c1d2/', 'confidence': 7.0, 'recorder_field_id': 1}, {'species_code': 'eurrob1', 'has_audio': True, 'datetime': '2024/04/11 - 09:01', 'url_media': 'https://api.ecopi.de/api/v0.1/detections/media/e0c689fc-41f9-4cc3-a0e6-7a3ad806c153/', 'confidence': 8.6, 'recorder_field_id': 2}, {'species_code': 'eurrob1', 'has_audio': True, 'datetime': '2024/04/11 - 08:01', 'url_media': 'https://api.ecopi.de/api/v0.1/detections/media/3f2f0225-92db-427f-97f7-73a959827d8c/', 'confidence': 5.8, 'recorder_field_id': 2}, {'species_code': 'eurrob1', 'has_audio': True, 'datetime': '2024/04/11 - 09:11', 'url_media': 'https://api.ecopi.de/api/v0.1/detections/media/f09132c6-368d-4474-9ca3-2b5ff1e3ca1d/', 'confidence': 7.4, 'recorder_field_id': 2}, {'species_code': 'eurrob1', 'has_audio': True, 'datetime': '2024/04/11 - 09:01', 'url_media': 'https://api.ecopi.de/api/v0.1/detections/media/a6061200-983b-4178-aa89-414480445bd9/', 'confidence': 7.7, 'recorder_field_id': 2}, {'species_code': 'eurrob1', 'has_audio': True, 'datetime': '2024/04/11 - 11:01', 'url_media': 'https://.....