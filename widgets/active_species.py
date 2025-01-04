from dash import html, dcc
import dash_bootstrap_components as dbc

from utils import data_processor as dp
from utils import plots
from utils.strings import Strings

def active_species(locale, n=8, hours=7*24, recorder_list=[], show_hint=True):
    species_data = dp.get_most_active_species(n=n, min_conf=0.5, hours=hours, recorder_list=recorder_list, locale=locale)
    plot_rows = []

    strings = Strings(locale)

    try:
        max_detections = max(data['total_detections'] for data in species_data.values())
    except:
        max_detections = 1

    for index, (species, data) in enumerate(species_data.items()):
        plot_sun_moon = True if index == 0 else False
        plot = plots.get_hourly_detections_plot(data['detections'], plot_sun_moon)
        detection_fraction = data['total_detections'] / max_detections * 100
        
        plot_row = dbc.Row(
            [
                dbc.Col(
                    html.Img(src=data['image_url'], className="species-image"),
                    xs=4,
                    sm="auto",
                    md="auto",
                    lg=1,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(f"{data['common_name']} ({data['total_detections']})", className="small-text"),
                                        html.Div(
                                            className="total-detections-bar",
                                            children=[
                                                html.Div(
                                                    className="total-detections-bar-fill",
                                                    style={"width": f"{detection_fraction}%"}
                                                )
                                            ]
                                        )
                                    ],
                                    sm=12,
                                    md=5,
                                    className="species-info"
                                ),
                                dbc.Col(
                                    dcc.Graph(figure=plot, config={"displayModeBar": False, "staticPlot": True}, style={"height": "50px"}),
                                    sm=12,
                                    md=7,
                                    className="species-plot"
                                )
                            ],
                        )
                    ],
                    xs=8,
                    sm=9,
                    md=10,
                    lg=11,
                )
            ],
            className="species-row mb-2",
        )
        
        plot_rows.append(plot_row)

    if not plot_rows:
        placeholder = html.P(string.gest('widget_error_no_data'), 
                             className="text-muted",
                             style={"text-align": "center", "width": "100%"})
    else:
        placeholder = None
        
        # Append a sentence on what the chart shows
        if show_hint:
            plot_rows.append(
                dbc.Row(
                    dbc.Col([
                        html.P(),
                        html.Div(strings.get('widget_active_species_description'),
                            className="text-muted",
                            style={"text-align": "center", "width": "100%"}),
                        ],
                        className="m-2"
                    )
                )
            )

    return plot_rows, placeholder

def active_species_simple(locale, n=8, hours=7*24, recorder_list=[]):
    species_data = dp.get_most_active_species(n=n, min_conf=0.5, hours=hours, recorder_list=recorder_list, locale=locale)
    plot_rows = []

    strings = Strings(locale)
    
    try:
        max_detections = max(data['total_detections'] for data in species_data.values())
    except:
        max_detections = 1
    
    for index, (species, data) in enumerate(species_data.items()):
        detection_fraction = data['total_detections'] / max_detections * 100
    
        # Create a 2x4 grid (1x8 on small screens) with each cell containing two columns: one for the species image and one for the bar with species name
        plot_row = dbc.Col(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(src=data['image_url'], className="species-image"),
                        xs=2,
                        sm=3,
                        md=3,
                        lg=2
                    ),
                    dbc.Col(
                        [
                            html.Div(f"{data['common_name']} ({data['total_detections']})", className="small-text"),
                            html.Div(
                                className="total-detections-bar",
                                children=[
                                    html.Div(
                                        className="total-detections-bar-fill",
                                        style={"width": f"{detection_fraction}%"}
                                    )
                                ]
                            )
                        ],
                        xs=10,
                        sm=9,
                        md=9,
                        lg=10
                    )
                ],
                className="species-cell"
            ),
            xs=12,
            sm=6,
            md=6,
            lg=4,
            className="species-col mb-2"
        )
        
        plot_rows.append(plot_row) 
    
    if not plot_rows:
        placeholder = html.P(strings.get('widget_error_no_data'), 
                             className="text-muted",
                             style={"text-align": "center", "width": "100%"})
    else:
        placeholder = None
        
    return dbc.Row(plot_rows, className="species-grid"), placeholder