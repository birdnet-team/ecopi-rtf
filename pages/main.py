from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from utils import data_processor as dp
from utils import plots

from widgets.popup_player import popup_player
from widgets.stats_bar import stats_bar
from widgets.active_species import active_species
from widgets.recent_detections import recent_detections
from widgets.recording_units import recording_units

import config as cfg

def main_page_content():
    return html.Div(
        [
            html.Div(
                [
                    html.Img(src=cfg.SITE_ROOT + "/assets/swamp_header.jpg", className="header-graphic"),
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
            stats_bar(),
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
                    html.Div(id="last-detections-data-container", className="d-none"),
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
                                    html.Img(src=cfg.SITE_ROOT + "/assets/haikubox_teaser.png", className="img-fluid"),
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
                                    html.Img(src=cfg.SITE_ROOT + "/assets/birdweather_teaser.png", className="img-fluid"),
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
            popup_player(),
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
            Output("no-detections-placeholder", "children"),
            Output("last-detections-data-container", "children")
        ], 
        [Input("url", "pathname")]
    )
    def update_last_detections(pathname):
        return recent_detections()

    @app.callback(
        [
            Output("most-active-species", "children"),
            Output("no-active-species-placeholder", "children")
        ],
        [Input("url", "pathname")]
    )
    def update_most_active_species(pathname):
        return active_species()

    @app.callback(
        [Output('recorder-stats', 'children'),
         Output('no-recorder-stats-placeholder', 'children')],
        [Input('url', 'pathname')]
    )
    def update_recorder_stats(pathname):
        return recording_units()