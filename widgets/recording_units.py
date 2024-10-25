from dash import html, dcc
import dash_bootstrap_components as dbc

from utils import data_processor as dp
from utils import plots

def recording_units():
    try:
        recorder_data = dp.get_recorder_data()
        map_figure = plots.get_recorder_map(recorder_data)
        
        map_component = html.Div(
            [
                html.Div("Recorder map", className="text-center small-text mb-2"),
                dcc.Graph(figure=map_figure, config={"staticPlot": True}, id="map-container", className="mb-2")
            ]
        )
        
        recorder_stats = []
        
        recorder_stats.append(
            dbc.Row(
                [
                    dbc.Col(html.Div("Detections | Species (24h)", className="small-text text-center mb-2"), width=12)
                ],
                className="recorder-stats-heading"
            )
        )
        
        for r in recorder_data:
            recorder_stats.append(
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Link(
                                    html.Div(f"#{r}", className="small-text"),
                                    href=f"/recorder/{r}"
                                ),
                                width=2
                            ),
                            dbc.Col(
                                dcc.Link(
                                    html.Div(f"{recorder_data[r]['detections']} | {len(recorder_data[r]['species_counts'])}", className="small-text"),
                                    href=f"/recorder/{r}"
                                ),
                                width=8
                            ),
                            dbc.Col(
                                dcc.Link(
                                    html.Div(html.I(className="bi bi-graph-up"), className="small-text"),
                                    href=f"/recorder/{r}"
                                ),
                                width=2
                            ),
                        ],
                        className="recorder-info",
                    ),
                    width=12,
                )        
            )
            
        children = [
            dbc.Row(
                [
                    dbc.Col(map_component, 
                            md=9,
                            xs=12
                        ),
                    dbc.Col(recorder_stats, 
                            md=3,
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