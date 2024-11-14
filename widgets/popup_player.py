from dash import html, dcc
import dash_bootstrap_components as dbc

def popup_player():
    return html.Div(
        [
            html.Div(id="popup-backdrop", className="d-none"),
            html.Div(id='popup', className='d-flex flex-column justify-content-between', children=[
                html.Div(id='popup-content', children=[ 
                    html.H5("common_name", className="card-title", id="popup-com-name"),
                    html.P("scientific_name", className="card-subtitle mb-2 text-muted", id="popup-sci-name"),
                    html.Div(id="popup-audio-container"),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div("Date:", className="very-small-text", id="popup-date"),
                                    html.Div("Recorder:", className="very-small-text", id="popup-recorder"),
                                ],
                                width=9,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Div(
                                            "confidence",
                                            id="popup-confidence-text",
                                            className="confidence-score-text"
                                        ),
                                        html.Div(
                                            id="popup-confidence-bar",
                                            className="confidence-score-bar",
                                        ),
                                    ],
                                    className="confidence-score-container"
                                ),
                                width=3,
                                className="d-flex align-items-center justify-content-center",
                            ),
                        ],
                        className="align-items-end mt-3",
                    ),
                ]),
                html.Div(id='popup-footer', className="d-flex justify-content-center mt-3",children=[
                html.Button('Close', id='close-popup-button')]),
            ])
        ]
    )