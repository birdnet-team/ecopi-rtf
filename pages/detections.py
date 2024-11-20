from dash import html, dcc
import dash_bootstrap_components as dbc
from utils import data_processor as dp
import json
import config as cfg

def detections_page_content():
    # Fetch the last 24 detections
    last_detections = dp.get_last_n_detections(n=24)
    cards = []
    datalist = []

    for idx, (species, data) in enumerate(last_detections.items()):
        datalist.append(data)
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
                                    id={"type": "detections-play-icon", "index": idx},
                                ),
                                className="play-icon-overlay",
                            ),
                            html.A(
                                html.I(className="bi bi-bar-chart-fill"),
                                href=f"{cfg.SITE_ROOT}/species/{species}",
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
                                id={"type": "detections-output-placeholder", "index": idx}
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

    data = html.Data(id="audio-data-list", value=json.dumps(datalist))

    return html.Div(
        [
            dbc.Container(
                [
                    html.H3("Recent detections", className="mt-2 mb-2"),
                    html.P("This list shows species detections from the last 12 hours sorted by confidence score. Click the 'Play' button to listen to the recorded sounds or click the 'Chart' icon to see more stats about this species.", className="text-muted"),
                    dbc.Row(cards),
                    data
                ],
                fluid=True,
            ),
        ],
        className="main-content"  # Apply the main-content class for styling
    )