from dash import html, dcc
import dash_bootstrap_components as dbc

from utils import data_processor as dp
from utils import plots

import config as cfg

def recording_units():
    try:
        recorder_data = {}
        for recorder_id in cfg.RECORDERS:
            recorder_data[recorder_id] = dp.get_recorder_state(recorder_id)
            
        leaflet_map = plots.get_leaflet_map(recorder_data)
        
        map_component = html.Div(
            [
                #html.Div("Recorder map", className="text-center small-text mb-2"),
                leaflet_map
            ]
        )
                    
        children = [
            dbc.Row(
                [
                    dbc.Col(map_component, 
                            md=12,
                            xs=12
                        )
                ]
            )
        ]
        
        placeholder = None
    except Exception as e:
        print(e.with_traceback())
        children = []
        placeholder = html.P("Uuups...something went wrong. Please try to reload.", 
                             className="text-muted",
                             style={"text-align": "center", "width": "100%"})
    
    return children, placeholder