from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import json

from widgets.popup_player import popup_player
from utils import data_processor as dp

def species_page_content(species_id):
    species_data = dp.get_species_data(species_id)
    species_stats = dp.get_species_stats(species_id)
    
    total_detections = len(species_stats)
    most_recent_detection = species_stats[0]['datetime'] if species_stats else 'N/A'
    
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
    
    return html.Div(
        [
            dcc.Store(id="species-id-store", data=species_id),  # Store the species_id
            html.Div(
                [
                    html.Img(src=species_data["image_url_highres"], className="species-header-image"),
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H4(f"{species_data['common_name']}", className="species-overlay-text"),
                                        html.H6(f"{species_data['scientific_name']}", className="species-overlay-text"),
                                    ],
                                    width=9,
                                    xs=7
                                ),
                            ],
                            className="species-overlay-row"
                        ),
                        className="species-overlay",
                    ),
                    html.Data(
                        className="species-data",
                        id={"type": "species-data", "index": 0},
                        value=json.dumps(species_data),
                    )
                ],
                className="species-header",
            ),
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H6(f"{total_detections} detections (24h)"),
                                    html.H6(
                                        [
                                            html.I(className="bi bi-clock"),  # Clock icon
                                            f" {most_recent_detection}"
                                        ], className="small-text"
                                    ),
                                ],
                                width=9,
                                xs=7
                            ),
                            dbc.Col(
                                html.A("Learn more", href=species_data["ebird_url"], target="_blank", className="btn btn-href learn-more-btn"),
                                width=3,
                                xs=5,
                                className="d-flex align-items-start justify-content-end"
                            ),
                        ],
                        className="species-info-row"
                    ),
                    html.H5("Recent detections:", className="recent-detections-heading"),
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Date", id="date-header", n_clicks=0),
                                        html.Th("Score", id="score-header", n_clicks=0),
                                        html.Th("Recorder", id="recorder-header", n_clicks=0),
                                        html.Th("Audio"),
                                    ]
                                )
                            ),
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
            ),
            popup_player(),
        ],
        className="species-page-content"
    )

def register_species_callbacks(app):
    @app.callback(
        Output("detections-table-body", "children"),
        [Input("date-header", "n_clicks"),
         Input("score-header", "n_clicks"),
         Input("recorder-header", "n_clicks")],
        [State("date-header", "n_clicks_timestamp"),
         State("score-header", "n_clicks_timestamp"),
         State("recorder-header", "n_clicks_timestamp"),
         State("species-id-store", "data")]
    )
    def update_table(date_clicks, score_clicks, recorder_clicks, date_ts, score_ts, recorder_ts, species_id):
        species_stats = dp.get_species_stats(species_id)
        
        # Initialize timestamps to 0 if they are None
        date_ts = date_ts or 0
        score_ts = score_ts or 0
        recorder_ts = recorder_ts or 0
        
        if date_ts > score_ts and date_ts > recorder_ts:
            species_stats = sorted(species_stats, key=lambda x: x["datetime"], reverse=date_clicks % 2 == 1)
        elif score_ts > date_ts and score_ts > recorder_ts:
            species_stats = sorted(species_stats, key=lambda x: x["confidence"], reverse=score_clicks % 2 == 1)
        elif recorder_ts > date_ts and recorder_ts > score_ts:
            species_stats = sorted(species_stats, key=lambda x: x["recorder_field_id"], reverse=recorder_clicks % 2 == 1)
        
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
        
        rows = [
            html.Tr(
                [
                    html.Td(detection["datetime"]),
                    html.Td(
                        [
                            html.Span(
                                className="confidence-dot",
                                style={"backgroundColor": get_confidence_color(detection["confidence"] * 10)}
                            ),
                            f" {detection['confidence']}"
                        ]
                    ),
                    html.Td(detection["recorder_field_id"]),
                    html.Td(
                        [
                            html.A(
                                html.I(className="bi bi-play-circle-fill"),
                                # href=detection["url_media"],
                                target="_blank",
                                className="play-button",
                                id={"type": "species-play-icon", "index": idx}
                            ),
                            html.Data(
                                id={"type": "species-audio-data", "index": idx},
                                value=json.dumps(detection),
                            )
                        ],
                        className="text-center"
                    ),
                ]
            ) for idx, detection in enumerate(species_stats)
        ]
        
        return rows

    # Client-side callback for playing audio when play icon is clicked
    app.clientside_callback(
        """
        function(n_clicks, audio_id) {
            const dataElements = document.querySelectorAll("data");
            let dataElement = null;

            for (let i = 0; i < dataElements.length; i++) {
                const elementId = JSON.parse(dataElements[i].id);
                if (elementId.type === 'species-audio-data' && elementId.index === audio_id["index"]) {
                    dataElement = dataElements[i];
                }
            }
            
            if (dataElement) {
                let speciesDataElement = document.querySelector(".species-data");
                let speciesData = JSON.parse(speciesDataElement.value);
                let data = JSON.parse(dataElement.value);
                data.common_name = speciesData.common_name;
                data.scientific_name = speciesData.scientific_name;
                data.confidence *= 10;
                
                openPlayer(data);
                return dataElement.value;
            } else {
                throw new Error("Audio element not found: " + audio_id);
            }
        }
        """,
        Output({"type": "species-audio-data", "index": MATCH}, "value"),
        [Input({"type": "species-play-icon", "index": MATCH}, "n_clicks")],
        [State({"type": "species-audio-data", "index": MATCH}, "id")],
        prevent_initial_call=True,
    )