from dash import html, dcc
from utils import plots
import config as cfg
from utils import data_processor as dp
from utils.strings import Strings

def get_site_activity_map(species_id, locale):
    recorder_data = {}
    site_detections = dp.get_total_detections(species_list=[species_id], days=90, min_count=0)['species_counts'][species_id]['recorders']
    for recorder_id in cfg.RECORDERS:
        recorder_data[recorder_id] = dp.get_recorder_state(recorder_id, locale)
        recorder_data[recorder_id]['detections'] = site_detections.get(recorder_id, 0)

    site_activity_map = plots.get_leaflet_map(recorder_data)
    
    strings = Strings(locale)
    return html.Div([
        html.H5(f"{strings.get('species_site_activity')}:", className="recent-detections-heading"),
        html.Div(site_activity_map, id="site-activity-map", className="mt-4"),
        html.H6(strings.get('species_site_activity_desc'), className="mt-2 mb-4 small-text")
    ],
        className="main-content")