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
        
        recorder_stats = []
        
        # For each recorder, create a card with the recorder ID, current status, habitat, CPU temp, voltage, and last update
        for recorder_id, data in recorder_data.items():
            status_color = data.get('status_color', '#36824b')
            
            recorder_stats.append(
                dbc.Col(
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Span(
                                            className="status-circle",
                                            style={"backgroundColor": status_color, "borderRadius": "50%", "display": "inline-block", "width": "10px", "height": "10px", "marginRight": "10px"}
                                        ),
                                        f"Recorder #{recorder_id}",
                                        html.I(className="bi bi-bar-chart-fill", style={"float": "right"})
                                    ],
                                    className="small-text"
                                ),
                                dbc.CardBody(
                                    [
                                        html.H6([html.B("Status: "), f"{data['current_status']}"], className="very-small-text"),
                                        html.H6([html.B("Habitat: "), f"{cfg.RECORDERS[recorder_id]['habitat']}"], className="very-small-text"),
                                        html.H6([html.B("CPU Temp: "), f"{data['cpu_temp']} °C"], className="very-small-text"),
                                        html.H6([html.B("Voltage: "), f"{data['voltage'] if data['voltage'] is not None else 'N/A'} V"], className="very-small-text"),
                                        html.H6([html.B("Last Update: "), f"{data['last_update']}"], className="very-small-text")
                                    ]
                                )
                            ],
                            className="mt-3"  # Add top margin to each card
                        ),
                        href=f"{cfg.SITE_ROOT}/recorder/{recorder_id}",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    lg=4,
                    md=4,
                    sm=6,
                    xs=12
                )
            )        
                    
        children = [
            dbc.Row(
                [
                    dbc.Col(map_component, 
                            md=12,
                            xs=12
                        )
                ]
            ),
            dbc.Row(
                recorder_stats
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