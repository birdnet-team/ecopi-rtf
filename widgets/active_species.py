from dash import html, dcc
import dash_bootstrap_components as dbc

from utils import data_processor as dp
from utils import plots

def active_species(locale):
    species_data = dp.get_most_active_species(n=8, min_conf=0.5, hours=7*24, locale=locale)
    plot_rows = []

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
                                    md=4,
                                    className="species-info"
                                ),
                                dbc.Col(
                                    dcc.Graph(figure=plot, config={"displayModeBar": False, "staticPlot": True}, style={"height": "50px"}),
                                    sm=12,
                                    md=8,
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
        
    # Append a sentence on what the chart shows
    plot_rows.append(
        dbc.Row(
            dbc.Col([
                html.P(),
                html.Div("Dark blue bars show hourly detections; light blue marks nighttime, light yellow marks daytime, and numbers denote detections.",
                       className="text-muted",
                       style={"text-align": "center", "width": "100%"}),
                ],
                className="m-2"
            )
        )
    )

    if not plot_rows:
        placeholder = html.P("Uuups...something went wrong. Please try to reload.", 
                             className="text-muted",
                             style={"text-align": "center", "width": "100%"})
    else:
        placeholder = None

    return plot_rows, placeholder