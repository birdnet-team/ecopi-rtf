from dash import html, dcc, callback_context, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import json

import config as cfg

from widgets.popup_player import popup_player
from utils import data_processor as dp
from utils import plots

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

def create_table_headers():
    return html.Thead(
        html.Tr([
            html.Th([
                html.Div([
                    "Date",
                    html.I(className="bi bi-arrow-down-up")
                ], className="sortable-header")
            ], id="date-header", n_clicks=0),
            html.Th([
                html.Div([
                    "Score",
                    html.I(className="bi bi-arrow-down-up")
                ], className="sortable-header")
            ], id="score-header", n_clicks=0),
            html.Th([
                html.Div([
                    "Recorder",
                    html.I(className="bi bi-arrow-down-up")
                ], className="sortable-header")
            ], id="recorder-header", n_clicks=0),
            html.Th("Audio"),
        ])
    )

def species_page_header(species_data):
    return html.Div(
        [
            html.Img(src=species_data["image_url_highres"], className="species-header-image"),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(f"{species_data['common_name']}", className="species-overlay-text"),
                                html.H5(f"{species_data['scientific_name']}", className="species-overlay-text"),
                            ],
                            width=9,
                        ),
                        dbc.Col(
                            html.H6(f"Photo: {species_data['image_author']}", className="very-small-text species-overlay-text"),
                            width=3,
                            className="d-flex align-items-end justify-content-end"
                        ),
                    ],
                    className="species-overlay-row"
                ),
                className="species-overlay",
            ),
        ],
        className="species-header",
    )

def display_species_page(species_id):
    species_data = dp.get_species_data(species_id)
    
    return html.Div([
        dcc.Store(id="species-id-store", data=species_id),
        species_page_header(species_data),
        html.Div(
            dbc.Spinner(color="#b31b1b"),
            id="species-loading-container",
        ),
        # Hide initial content
        html.Div([
            dbc.Container(
                [
                    html.Div(id="species-info-row"),
                    html.H5("Daily activity (past week):", className="recent-detections-heading"),
                    html.Div(id="species-activity-plot"),
                    html.H5("Recent detections:", className="recent-detections-heading"),
                    dbc.Table(
                        [
                            create_table_headers(),
                            html.Tbody(id="detections-table-body")
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
        ], id="species-main-content", style={"display": "none"}),  # Hide initially
        html.Div(id="detections-data-container"),
        popup_player(),
    ], className="species-page-content")

def register_species_callbacks(app):
    @app.callback(
        [
            Output("species-info-row", "children"),
            Output("species-activity-plot", "children"),
            Output("species-loading-container", "children"),
            Output("detections-table-body", "children"),
            Output("detections-data-container", "children"),
            Output("species-main-content", "style"),
            Output("species-loading-container", "style"),
            Output("species-stats-store", "data"),
            Output("species-data-store", "data")
        ],
        [Input("species-id-store", "data")],
        prevent_initial_call=False
    )
    def update_species_content(species_id):
        if not species_id:
            raise PreventUpdate

        # Load all required data
        species_data = dp.get_species_data(species_id)
        species_stats = dp.get_species_stats(species_id)
        total_detections = dp.get_total_detections(species_list=[species_id], days=-1, min_count=0)['total_detections']
        activity_data = dp.get_most_active_species(n=1, min_conf=0.5, hours=24*7, species_list=[species_id], min_count=0)
        
        # Create info row
        info_row = dbc.Row([
            dbc.Col([
                html.H5(f"{total_detections:,} total detections"),
                html.H6([
                    html.I(className="bi bi-clock"),
                    f" {species_stats[0]['datetime'] if species_stats else 'N/A'}"
                ], className="small-text"),
            ], width=9, xs=7),
            dbc.Col(
                html.A("Learn more", href=species_data["ebird_url"], 
                      target="_blank", className="btn btn-href learn-more-btn"),
                width=3, xs=5,
                className="d-flex align-items-start justify-content-end"
            ),
        ], className="species-info-row")

        # Create activity plot
        hourly_plot = plots.get_hourly_detections_plot(activity_data[species_id]['detections'], plot_sun_moon=True)
        plot = dcc.Graph(
            figure=hourly_plot,
            config={"displayModeBar": False, "staticPlot": True},
            className="species-daily-activity-plot"
        )
        
        # Sort species stats by score
        species_stats = sorted(species_stats, key=lambda x: x["confidence"], reverse=True)

        # Create table rows
        rows = []
        data_list = []
        for idx, detection in enumerate(species_stats):
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
                        html.Div(
                            f"#{detection['recorder_field_id']}",
                            className="recorder-cell"
                        ),
                        href=f"{cfg.SITE_ROOT}/recorder/{detection['recorder_field_id']}",
                        style={"cursor": "pointer", "textDecoration": "none", "color": "inherit", "display": "block"}
                    )
                ]),
                html.Td([
                    html.A(
                        html.I(className="bi bi-play-circle-fill"),
                        target="_blank",
                        className="play-button",
                        id={"type": "species-play-icon", "index": idx}
                    ),
                    html.Data(id={"type": "species-output-placeholder", "index": idx})
                ], className="text-center"),
            ]))
            
            detection_data = detection.copy()
            detection_data["common_name"] = species_data["common_name"]
            detection_data["scientific_name"] = species_data["scientific_name"]
            detection_data["confidence"] = detection_data["confidence"] * 10
            data_list.append(detection_data)      

        # Store data for later use (moved after data_list creation)
        stored_data = {
            "species_stats": species_stats,
            "species_data": species_data,
            "data_list": data_list
        }

        return (
            info_row, 
            plot, 
            None,
            rows, 
            html.Data(id="audio-data-list", value=json.dumps(data_list)),
            {"opacity": "1"},
            {"height": "0px"},
            species_stats,    # Store stats
            species_data     # Store data
        )

    @app.callback(
        [
            Output("detections-table-body", "children", allow_duplicate=True),
            Output("detections-data-container", "children", allow_duplicate=True)
        ],
        [
            Input("date-header", "n_clicks"),
            Input("score-header", "n_clicks"),
            Input("recorder-header", "n_clicks")
        ],
        [
            State("species-stats-store", "data"),
            State("species-data-store", "data")
        ],
        prevent_initial_call=True
    )
    def sort_table(date_clicks, score_clicks, recorder_clicks, species_stats, species_data):
        if not species_stats:
            raise PreventUpdate

        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "date-header":
            species_stats = sorted(species_stats, key=lambda x: x["datetime"], 
                                reverse=date_clicks % 2 == 0)
        elif trigger_id == "score-header":
            species_stats = sorted(species_stats, key=lambda x: x["confidence"], 
                                reverse=score_clicks % 2 == 0)
        elif trigger_id == "recorder-header":
            species_stats = sorted(species_stats, key=lambda x: x["recorder_field_id"], 
                                reverse=recorder_clicks % 2 == 0)
        
        rows = []
        data_list = []
        for idx, detection in enumerate(species_stats):
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
                        html.Div(
                            f"#{detection['recorder_field_id']}",
                            className="recorder-cell"
                        ),
                        href=f"{cfg.SITE_ROOT}/recorder/{detection['recorder_field_id']}",
                        style={"cursor": "pointer", "textDecoration": "none", "color": "inherit", "display": "block"}
                    )
                ]),
                html.Td([
                    html.A(
                        html.I(className="bi bi-play-circle-fill"),
                        target="_blank",
                        className="play-button",
                        id={"type": "species-play-icon", "index": idx}
                    ),
                    html.Data(id={"type": "species-output-placeholder", "index": idx})
                ], className="text-center"),
            ]))
            
            # Create new data_list with sorted order
            detection_data = detection.copy()
            detection_data["common_name"] = species_data["common_name"]
            detection_data["scientific_name"] = species_data["scientific_name"]
            detection_data["confidence"] = detection_data["confidence"] * 10
            data_list.append(detection_data)

        # Return both rows and updated audio data list
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
        Output({"type": "species-output-placeholder", "index": MATCH}, "value"),
        [Input({"type": "species-play-icon", "index": MATCH}, "n_clicks")],
        [State({"type": "species-play-icon", "index": MATCH}, "id")],
        prevent_initial_call=True,
    )