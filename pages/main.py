from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import random

from utils import data_processor as dp
from utils import plots
from utils.strings import Strings

from widgets.popup_player import popup_player
from widgets.livestream_popup_player import livestream_popup_player
from widgets.stats_bar import stats_bar
from widgets.active_species import active_species
from widgets.recent_detections import recent_detections
from widgets.recording_units import recording_units

import config as cfg

def main_page_content(locale):
    
    strings = Strings(locale, project=cfg.PROJECT_ID)
    
    return html.Div(
        [
            html.Div(
                [
                    html.Img(src=cfg.SITE_ROOT + f"/assets/header_img/{random.choice(cfg.MAIN_HEADER_IMG_LIST)}", className="header-graphic"),
                    html.Div(
                        [
                            html.H1(cfg.PROJECT_ACRONYM + ': ' + strings.get('project_main_title')),
                            html.H2(strings.get('project_subtitle')),
                        ],
                        className="header-overlay"
                    ),
                    html.Button(
                        [html.I(className="bi bi-volume-up-fill"), f" {strings.get('main_listen_live')}"],
                        id="listen-live-button",
                        className="listen-live-button" if len(cfg.LIVE_STREAM_URL) > 0 else "d-none",
                    ),
                    html.Data(id="livestream-output-placeholder", value=""),
                ],
                style={"position": "relative"}
            ),
            stats_bar(locale),
            html.Div(className="h-spacer"),
            dbc.Container(
                [
                    html.Div(
                        [
                            html.H1(cfg.PROJECT_ACRONYM + ': ' + strings.get('project_main_title')),
                        ],
                        className="header-text"
                    ),
                    html.H5(strings.get('project_subtitle_desc'), 
                            className="text-center d-lg-block mb-4"),
                    html.Div(
                        dbc.Button(
                            strings.get('species_learn_more'),
                            href=f"{cfg.SITE_ROOT}/about",
                            className="btn-href btn-primary d-block d-lg-none mb-4"
                        ),
                        className="d-flex justify-content-center",  # Center the button
                    ),
                    html.Div(className="divider-container", children=[
                        html.Div(className="divider-line"),
                        html.H5(strings.get('main_most_active_species'), className="divider-heading"),
                        html.Div(className="divider-line")
                    ]),
                    dbc.Row(id="most-active-species", className="mt-4"),
                    dbc.Spinner(html.Div(id="no-active-species-placeholder", className="spinner"), color=cfg.PRIMARY_COLOR),
                    html.Div(className="divider-container", children=[
                        html.Div(className="divider-line"),
                        html.H5(strings.get('main_recent_detections'), className="divider-heading"),
                        html.Div(className="divider-line")
                    ]),
                    dbc.Row(id="last-detections", className="mt-4"),
                    html.Div(id="last-detections-data-container", className="d-none"),
                    dbc.Spinner(html.Div(id="no-detections-placeholder", className="spinner"), color=cfg.PRIMARY_COLOR),
                    html.Div(className="divider-container", children=[
                        html.Div(className="divider-line"),
                        html.H5(strings.get('main_recording_units'), className="divider-heading"),
                        html.Div(className="divider-line")
                    ]),
                    dbc.Row(id="recorder-stats", className="mt-4"),
                    dbc.Spinner(html.Div(id="no-recorder-stats-placeholder", className="spinner"), color=cfg.PRIMARY_COLOR),
                    html.Div(className="divider-container", children=[
                        html.Div(className="divider-line"),
                        html.H5(strings.get('main_diy_backyard_monitoring'), className="divider-heading"),
                        html.Div(className="divider-line")
                    ]),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H5(strings.get('main_haikubox'), className="text-center"),
                                    html.Img(src=cfg.SITE_ROOT + "/assets/content_img/haikubox_teaser.png", className="img-fluid"),
                                    html.P(strings.get('main_haikubox_description'), className="text-justify mt-4"),
                                    html.Div(
                                        html.A(strings.get('main_visit_haikubox_website'), href="https://www.haikubox.com", target="_blank", className="btn btn-href mt-4"),
                                        className="d-flex justify-content-center mb-4"
                                    ),
                                ],
                                md=6,
                                sm=12
                            ),
                            dbc.Col(
                                [
                                    html.H5(strings.get('main_birdweather'), className="text-center"),
                                    html.Img(src=cfg.SITE_ROOT + "/assets/content_img/birdweather_teaser.png", className="img-fluid"),
                                    html.P(strings.get('main_birdweather_description'), className="text-justify mt-4"),
                                    html.Div(
                                        html.A(strings.get('main_visit_birdweather_website'), href="https://www.birdweather.com", target="_blank", className="btn btn-href mt-4"),
                                        className="d-flex justify-content-center mb-4"
                                    ),
                                ],
                                md=6,
                                sm=12
                            )
                        ],
                        className="mt-4"
                    ),
                    html.Div(
                        html.A(
                            [
                                html.I(className="bi bi-arrow-up-circle"),
                                " " + strings.get('misc_back_to_top'),
                            ],
                            href="#",
                            className="back-to-top-link"
                        ),
                        id="back-to-top-link",  # Assign an ID to the "Back to top" link
                        className="d-flex justify-content-end p-4",
                    ),
                ],
                fluid=True,
                className="main-content",
            ),
            
            popup_player(),
            livestream_popup_player(),
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
        total_audio = dp.get_total_audio_duration()

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
        [Input("url", "pathname"), Input("locale-store", "data")]
    )
    def update_last_detections(pathname, locale):
        return recent_detections(locale=locale)

    @app.callback(
        [
            Output("most-active-species", "children"),
            Output("no-active-species-placeholder", "children")
        ],
        [Input("url", "pathname"), Input("locale-store", "data")]
    )
    def update_most_active_species(pathname, locale):
        return active_species(locale)

    @app.callback(
        [Output('recorder-stats', 'children'),
         Output('no-recorder-stats-placeholder', 'children')],
        [Input('url', 'pathname'), Input("locale-store", "data")]
    )
    def update_recorder_stats(pathname, locale):
        return recording_units(locale)
    
    # Client-side callback for opening the livestream popup
    app.clientside_callback(
        "function(n_clicks) {openLivestream('" + cfg.LIVE_STREAM_URL + "');}",
        Output("livestream-output-placeholder", "value"),
        [Input("listen-live-button", "n_clicks")],
        prevent_initial_call=True,
    )