from dash import html, dcc, callback_context, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH

from widgets.popup_player import popup_player
from utils import data_processor as dp
import config as cfg
import json

def get_confidence_color(confidence):
    if confidence < 33:
        return "#B31B1B"
    elif confidence < 50:
        return "#FF672E"
    elif confidence < 75:
        return "#FFBC10"
    elif confidence < 85:
        return "#D9EB6F"
    elif confidence < 90:
        return "#A3BC09"
    else:
        return "#296239"

def create_recorder_table_headers(locale):
    return html.Thead(
        html.Tr([
            html.Th([
                html.Div([
                    "Date",
                    html.I(className="bi bi-arrow-down-up")
                ], className="sortable-header")
            ], id="recorder-date-header", n_clicks=0),
            html.Th([
                html.Div([
                    "Score",
                    html.I(className="bi bi-arrow-down-up")
                ], className="sortable-header")
            ], id="recorder-score-header", n_clicks=0),
            html.Th([
                html.Div([
                    "Species",
                    html.I(className="bi bi-arrow-down-up")
                ], className="sortable-header")
            ], id="recorder-species-header", n_clicks=0, className="species-column-header"),
            html.Th("Audio"),
        ])
    )

def recorder_page_header(recorder_id, locale):
    return html.Div(
        [
            html.Img(src=cfg.SITE_ROOT + "/assets/recorder_img/" + cfg.RECORDERS[int(recorder_id)]['img'], className="species-header-image"),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(f"Recorder #{recorder_id}", className="species-overlay-text"),
                                html.H5("Habitat type: " + cfg.RECORDERS[int(recorder_id)]['habitat'], className="species-overlay-text"),
                            ],
                            width=12,
                        ),
                    ],
                    className="species-overlay-row"
                ),
                className="species-overlay",
            ),
        ],
        className="species-header",
    )

def display_recorder_page(recorder_id, locale):
    return html.Div([
        dcc.Store(id="recorder-id-store", data=recorder_id),
        recorder_page_header(recorder_id, locale),
        html.Div(
            dbc.Spinner(color=cfg.PRIMARY_COLOR),
            id="recorder-loading-container",
        ),
        html.Div([
            dbc.Container(
                [
                    html.Div(id="recorder-info-row"),
                    html.H5("Recent detections:", className="recent-detections-heading"),
                    dbc.Table(
                        [
                            create_recorder_table_headers(locale),
                            html.Tbody(id="recorder-detections-table-body")
                        ],
                        bordered=True,
                        hover=True,
                        responsive=True,
                        striped=True,
                        className="detections-table"
                    )
                ],
                fluid=True,
                className="species-main-content",
            )
        ], id="recorder-main-content", style={"display": "none"}),
        html.Div(id="recorder-detections-data-container"),
        popup_player(),
    ], className="species-page-content")

def register_recorder_callbacks(app):
    @app.callback(
        [
            Output("recorder-info-row", "children"),
            Output("recorder-loading-container", "children"),
            Output("recorder-detections-table-body", "children"),
            Output("recorder-detections-data-container", "children"),
            Output("recorder-main-content", "style"),
            Output("recorder-loading-container", "style"),
            Output("recorder-stats-store", "data"),
            Output("recorder-data-store", "data")
        ],
        [Input("recorder-id-store", "data")],
        [State("locale-store", "data")],
        prevent_initial_call=False
    )
    def update_recorder_content(recorder_id, locale):
        if not recorder_id:
            raise PreventUpdate

        # Load recorder data
        recorder_id = int(recorder_id)
        recorder_info = dp.get_recorder_state(recorder_id, locale)
        total_detections = dp.get_total_detections(recorder_list=[recorder_id], days=-1, min_count=0)['total_detections']
        recorder_stats = dp.get_species_stats(recorder_id=recorder_id, max_results=25)
        
        # Get additional species info for each detection
        for detection in recorder_stats:
            species_data = dp.get_species_data(detection["species_code"], locale)
            detection["common_name"] = species_data["common_name"]
            detection["scientific_name"] = species_data["scientific_name"]
            detection["species_thumbnail"] = species_data["thumbnail_url"]
        
        # Create info row
        info_row = dbc.Row([
            dbc.Col([
                html.H5(f"{total_detections:,} total detections"),
                html.H6([
                    html.I(className="bi bi-clock"),
                    f" {recorder_info['last_update'] if recorder_info else 'N/A'}"
                ], className="small-text"),
            ], width=6),
            dbc.Col([
                html.H5(f"Status: {recorder_info['current_status'].split(' | ')[-1] if recorder_info else 'N/A'}"),
                html.H6([f"Battery: {recorder_info['battery'] if recorder_info else 'N/A'} %"], className="small-text"),
                html.H6([f"CPU Temp: {recorder_info['cpu_temp'] if recorder_info else 'N/A'} °C"], className="small-text"),
            ], width=6, className="text-right"),
        ], className="species-info-row")

        # Sort recorder stats by date
        recorder_stats = sorted(recorder_stats, key=lambda x: x["confidence"], reverse=True)

        # Create table rows
        rows = []
        data_list = []
        for idx, detection in enumerate(recorder_stats):
            rows.append(html.Tr([
                html.Td(detection["datetime"]),
                html.Td([
                    html.Span(
                        className="confidence-dot",
                        style={"backgroundColor": get_confidence_color(detection["confidence"] * 10)}
                    ),
                    f" {int(detection['confidence'] * 10) / 10.0}"
                ]),
                html.Td([
                    html.A(
                        html.Div([
                            html.Img(
                                src=detection["species_thumbnail"],
                                className="species-thumbnail hide-on-small-screens"
                            ),
                            html.Span(
                                detection["common_name"],
                                className="species-name"
                            ),
                            html.Span(
                                html.I(className="bi bi-bar-chart-fill hide-on-small-screens"),
                                style={"marginLeft": "auto"}
                            )
                        ], className="species-column"),
                        href=f"{cfg.SITE_ROOT}/species/{detection['species_code']}",
                        style={"cursor": "pointer", "textDecoration": "none", "color": "inherit"}
                    )
                ]),
                html.Td([
                    html.A(
                        html.I(className="bi bi-play-circle-fill"),
                        target="_blank",
                        className="play-button",
                        id={"type": "recorder-play-icon", "index": idx}
                    ),
                    html.Data(id={"type": "recorder-output-placeholder", "index": idx})
                ], className="text-center"),
            ]))
            
            # Create new data_list with sorted order
            detection_data = detection.copy()
            detection_data["common_name"] = detection["common_name"]
            detection_data["scientific_name"] = detection["scientific_name"]
            detection_data["confidence"] = detection["confidence"] * 10
            data_list.append(detection_data)

        stored_data = {
            "recorder_info": recorder_info,
            "recorder_detections": total_detections,
            "data_list": data_list
        }

        return (
            info_row, 
            None,
            rows, 
            html.Data(id="audio-data-list", value=json.dumps(data_list)),
            {"opacity": "1"},
            {"height": "0px"},
            recorder_stats,
            stored_data
        )

    @app.callback(
        [
            Output("recorder-detections-table-body", "children", allow_duplicate=True),
            Output("recorder-detections-data-container", "children", allow_duplicate=True)
        ],
        [
            Input("recorder-date-header", "n_clicks"),
            Input("recorder-score-header", "n_clicks"),
            Input("recorder-species-header", "n_clicks")
        ],
        [
            State("recorder-stats-store", "data"),
            State("recorder-data-store", "data")
        ],
        prevent_initial_call=True
    )
    def sort_table(date_clicks, score_clicks, species_clicks, recorder_stats, recorder_data):
        if not recorder_stats:
            raise PreventUpdate

        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "recorder-date-header":
            recorder_stats = sorted(recorder_stats, key=lambda x: x["datetime"], 
                                 reverse=date_clicks % 2 == 0)
        elif trigger_id == "recorder-score-header":
            recorder_stats = sorted(recorder_stats, key=lambda x: x["confidence"], 
                                 reverse=score_clicks % 2 == 0)
        elif trigger_id == "recorder-species-header":
            recorder_stats = sorted(recorder_stats, key=lambda x: x["species_code"], 
                                 reverse=species_clicks % 2 == 0)

        rows = []
        data_list = []
        for idx, detection in enumerate(recorder_stats):
            rows.append(html.Tr([
                html.Td(detection["datetime"]),
                html.Td([
                    html.Span(
                        className="confidence-dot",
                        style={"backgroundColor": get_confidence_color(detection["confidence"] * 10)}
                    ),
                    f" {int(detection['confidence'] * 10) / 10.0}"
                ]),
                html.Td([
                    html.A(
                        html.Div([
                            html.Img(
                                src=detection["species_thumbnail"],
                                className="species-thumbnail hide-on-small-screens"
                            ),
                            html.Span(
                                detection["common_name"],
                                className="species-name"
                            ),
                            html.Span(
                                html.I(className="bi bi-bar-chart-fill hide-on-small-screens"),
                                style={"marginLeft": "auto"}
                            )
                        ], className="species-column"),
                        href=f"{cfg.SITE_ROOT}/species/{detection['species_code']}",
                        style={"cursor": "pointer", "textDecoration": "none", "color": "inherit"}
                    )
                ]),
                html.Td([
                    html.A(
                        html.I(className="bi bi-play-circle-fill"),
                        target="_blank",
                        className="play-button",
                        id={"type": "recorder-play-icon", "index": idx}
                    ),
                    html.Data(id={"type": "recorder-output-placeholder", "index": idx})
                ], className="text-center"),
            ]))
            
            detection['confidence'] = detection['confidence'] * 10
            data_list.append(detection)

        return [
            rows,
            html.Data(id="audio-data-list", value=json.dumps(data_list))
        ]

    app.clientside_callback(
        """
        function(n_clicks, audio_id) {
            openPlayer(audio_id["index"]);
        }
        """,
        Output({"type": "recorder-output-placeholder", "index": MATCH}, "value"),
        [Input({"type": "recorder-play-icon", "index": MATCH}, "n_clicks")],
        [State({"type": "recorder-play-icon", "index": MATCH}, "id")],
        prevent_initial_call=True,
    )