from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import json

from utils import data_processor as dp

def recent_detections():
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
                                    id={"type": "recent-detections-play-icon", "index": idx},
                                ),
                                className="play-icon-overlay",
                            ),
                            #html.A(
                            #    html.I(className="bi bi-info-circle-fill"),
                            #    href=data["ebird_url"],
                            #    target="_blank",
                            #    className="info-icon-overlay",
                            #),
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
                            html.Data(
                                id={"type": "recent-detections-audio-data", "index": idx},
                                value=json.dumps(data),
                            )
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

def register_recent_detections_callbacks(app):
    # Client-side callback for playing audio when play icon is clicked
    app.clientside_callback(
        """
        function(n_clicks, audio_id) {
            const dataElements = document.querySelectorAll("data");
            let dataElement = null;

            for (let i = 0; i < dataElements.length; i++) {
                const elementId = JSON.parse(dataElements[i].id);
                if (elementId.type === 'recent-detections-audio-data' && elementId.index === audio_id["index"]) {
                    dataElement = dataElements[i];
                }
            }
            
            if (dataElement) {
                data = JSON.parse(dataElement.value);

                openPlayer(data);
                return dataElement.value;
            } else {
                throw new Error("Audio element not found: " + audio_id);
            }
        }
        """,
        Output({"type": "recent-detections-audio-data", "index": MATCH}, "value"),
        [Input({"type": "recent-detections-play-icon", "index": MATCH}, "n_clicks")],
        [State({"type": "recent-detections-audio-data", "index": MATCH}, "id")],
        prevent_initial_call=True,
    )