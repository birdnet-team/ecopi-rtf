from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


import data_processor as dp
import plots

def main_page_content():
    return html.Div(
        [
            html.Div(
                [
                    html.Img(src="/assets/swamp_header.jpg", className="header-graphic"),
                    html.Div(
                        [
                            html.H1("SWAMP: Sapsucker Woods Acoustic Monitoring Project"),
                            html.H2("AI-powered acoustic monitoring"),
                        ],
                        className="header-overlay"
                    ),
                    html.Button(
                        [html.I(className="bi bi-volume-up-fill"), " Listen live"],
                        className="listen-live-button"
                    ),
                ],
                style={"position": "relative"}
            ),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div([html.Div("Detections (24h):"), html.H4(id="detections-24h", children="0")]),
                            className="stat-column",
                            width=6,
                            md=3,
                        ),
                        dbc.Col(
                            html.Div([html.Div("Species (24h):"), html.H4(id="species-24h", children="0")]),
                            className="stat-column",
                            width=6,
                            md=3,
                        ),
                        dbc.Col(
                            html.Div([html.Div("Detections (total):"), html.H4(id="total-detections", children="0")]),
                            className="stat-column",
                            width=6,
                            md=3,
                        ),
                        dbc.Col(
                            html.Div([html.Div("Audio (total):"), html.H4(id="total-audio", children="0")]),
                            className="stat-column",
                            width=6,
                            md=3,
                        ),
                    ],
                    className="stat-row-container",
                ),
                className="stat-row",
            ),
            html.Div(className="h-spacer"),
            dbc.Container(
                [
                    html.Div(
                        [
                            html.H1("SWAMP: Sapsucker Woods Acoustic Monitoring Project"),
                        ],
                        className="header-text"
                    ),
                    html.H5("We listen to the sounds of the animals in Sapsucker Woods and track species diversity over large spatio-temporal scales.", 
                            className="text-center d-none d-lg-block"),
                    html.Div(className="divider-container", children=[
                        html.Div(className="divider-line"),
                        html.H5("Most active species (24h)", className="divider-heading"),
                        html.Div(className="divider-line")
                    ]),
                    dbc.Row(id="most-active-species", className="mt-4"),
                    dbc.Spinner(html.Div(id="no-active-species-placeholder", className="spinner"), color="#b31b1b"),
                    html.Div(className="divider-container", children=[
                        html.Div(className="divider-line"),
                        html.H5("Recent detections", className="divider-heading"),
                        html.Div(className="divider-line")
                    ]),
                    dbc.Row(id="last-detections", className="mt-4"),
                    dbc.Spinner(html.Div(id="no-detections-placeholder", className="spinner"), color="#b31b1b"),
                    html.Div(className="divider-container", children=[
                        html.Div(className="divider-line"),
                        html.H5("Recording units", className="divider-heading"),
                        html.Div(className="divider-line")
                    ]),
                    dbc.Row(id="recorder-stats", className="mt-4"),
                    dbc.Spinner(html.Div(id="no-recorder-stats-placeholder", className="spinner"), color="#b31b1b"),
                    html.Div(className="divider-container", children=[
                        html.Div(className="divider-line"),
                        html.H5("DIY backyard monitoring", className="divider-heading"),
                        html.Div(className="divider-line")
                    ]),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H5("Haikubox", className="text-center"),
                                    html.Img(src="/assets/haikubox_teaser.png", className="img-fluid"),
                                    html.P("Haikubox is an innovative tool designed for bird enthusiasts and conservationists who want to keep track of the birds visiting their backyards. Using advanced AI-powered sound recognition, Haikubox listens to bird calls and automatically identifies species in real-time. It's a hands-free solution that provides continuous monitoring, making it ideal for anyone curious about local bird activity without needing to have expert knowledge.", className="text-justify mt-4"),
                                    html.Div(
                                        html.A("Visit the Haikubox website", href="https://www.haikubox.com", target="_blank", className="btn btn-href mt-4"),
                                        className="d-flex justify-content-center mb-4"
                                    ),
                                ],
                                md=6,
                                sm=12
                            ),
                            dbc.Col(
                                [
                                    html.H5("BirdWeather", className="text-center"),
                                    html.Img(src="/assets/birdweather_teaser.png", className="img-fluid"),
                                    html.P("BirdWeather is an advanced bird monitoring platform that connects bird enthusiasts with real-time data about bird species visiting their area. BirdWeather allows users to identify bird species based on their calls, without the need for expert-level birdwatching knowledge. The platform is designed to provide continuous, automated monitoring, making it a perfect solution for those interested in observing bird activity in their backyard.", className="text-justify mt-4"),
                                    html.Div(
                                        html.A("Visit the BirdWeather website", href="https://www.birdweather.com", target="_blank", className="btn btn-href mt-4"),
                                        className="d-flex justify-content-center mb-4"
                                    ),
                                ],
                                md=6,
                                sm=12
                            )
                        ],
                        className="mt-4"
                    ),
                ],
                fluid=True,
                className="main-content",
            ),
        ]
    )

def register_main_callbacks(app):
    @app.callback(
        [
            Output("total-detections", "children"),
            Output("detections-24h", "children"),
            Output("species-24h", "children"),
            Output("total-audio", "children"),
        ],
        [Input("url", "pathname")],
    )
    def update_statistics(pathname):
        total_detections = dp.get_total_detections()
        detections_24h = dp.get_total_detections(days=1)
        species_24h = len(detections_24h["species_counts"])
        total_audio = total_detections["total_detections"] * 5

        total_detections_formatted = f"{total_detections['total_detections']:,}"
        detections_24h_formatted = f"{detections_24h['total_detections']:,}"
        species_24h_formatted = f"{species_24h:,}"
        total_audio_formatted = f"{total_audio // 86400}d {total_audio % 86400 // 3600}h {total_audio % 3600 // 60}m"

        return total_detections_formatted, detections_24h_formatted, species_24h_formatted, total_audio_formatted

    @app.callback(
        [
            Output("last-detections", "children"), 
            Output("no-detections-placeholder", "children")
        ], 
        [Input("url", "pathname")]
    )
    def update_last_detections(pathname):
        last_detections = dp.get_last_n_detections()
        cards = []

        for idx, (species, data) in enumerate(last_detections.items()):
            confidence_score = data['confidence'] * 10
            card = dbc.Col(
                dbc.Card(
                    [
                        html.Div(
                            [
                                dbc.CardImg(src=data["image_url"], top=True, className="card-img-top"),
                                html.Div(
                                    html.Div(
                                        [html.I(className="bi bi-play-circle-fill", id=f"play-icon-{idx}")],
                                        id={"type": "play-icon", "index": idx},
                                    ),
                                    className="play-icon-overlay",
                                ),
                                html.A(
                                    html.I(className="bi bi-info-circle-fill"),
                                    href=data["ebird_url"],
                                    target="_blank",
                                    className="info-icon-overlay",
                                ),
                                html.A(
                                    html.I(className="bi bi-bar-chart-fill"),
                                    href=f"/species/{species}",
                                    className="chart-icon-overlay",
                                ),
                                html.Div(
                                    f"Photo: {data['image_author']}",
                                    className="photo-author-overlay",
                                ),
                            ],
                            style={"position": "relative"},
                        ),
                        dbc.CardBody(
                            [
                                html.H5(data["common_name"], className="card-title"),
                                html.P(data["scientific_name"], className="card-subtitle mb-2 text-muted"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div(f"Date: {data['datetime']}", className="very-small-text"),
                                                html.Div(f"Recorder: #{data['recorder_field_id']}", className="very-small-text"),
                                            ],
                                            width=9,
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Div(
                                                        f"{data['confidence'] / 10.0:.1f}",
                                                        className="confidence-score-text"
                                                    ),
                                                    html.Div(
                                                        className="confidence-score-bar",
                                                        style={
                                                            "--value": data['confidence'],
                                                            "--color": (
                                                                "#B31B1B" if data['confidence'] < 33 else
                                                                "#FF672E" if data['confidence'] < 50 else
                                                                "#FFBC10" if data['confidence'] < 75 else
                                                                "#D9EB6F" if data['confidence'] < 85 else
                                                                "#A3BC09" if data['confidence'] < 90 else
                                                                "#296239"
                                                            )
                                                        }
                                                    ),
                                                ],
                                                className="confidence-score-container"
                                            ),
                                            width=3,
                                            className="d-flex align-items-center justify-content-center",
                                        ),
                                    ],
                                    className="align-items-end",
                                ),
                                html.Audio(
                                    id={"type": "audio", "index": idx},
                                    src=data["url_media"],
                                    controls=True,
                                    className="d-none",
                                ),
                            ]
                        ),
                    ],
                    className="mb-4",
                    style={"width": "100%", "position": "relative"},
                ),
                width=12,
                sm=6,
                md=6,
                lg=4,
                xl=3,
            )
            cards.append(card)

        if not cards:
            placeholder = html.P("Uuups...something went wrong. Please try to reload.", 
                                 className="text-muted",
                                 style={"text-align": "center", "width": "100%"})
        else:
            placeholder = None

        return cards, placeholder

    @app.callback(
        [
            Output("most-active-species", "children"),
            Output("no-active-species-placeholder", "children")
        ],
        [Input("url", "pathname")]
    )
    def update_most_active_species(pathname):
        species_data = dp.get_most_active_species(n=8, min_conf=0.5)
        plot_rows = []

        max_detections = max(data['total_detections'] for data in species_data.values())

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

        if not plot_rows:
            placeholder = html.P("Uuups...something went wrong. Please try to reload.", 
                                 className="text-muted",
                                 style={"text-align": "center", "width": "100%"})
        else:
            placeholder = None

        return plot_rows, placeholder

    @app.callback(
        [Output('recorder-stats', 'children'),
         Output('no-recorder-stats-placeholder', 'children')],
        [Input('url', 'pathname')]
    )
    def update_recorder_stats(pathname):
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