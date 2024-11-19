from dash import html, dcc
import dash_bootstrap_components as dbc


def livestream_popup_player():
    return html.Div(
        [
            html.Div(id="livestream-popup-backdrop", className="d-none"),
            html.Div(
                id="livestream-popup",
                className="d-flex flex-column justify-content-between",
                children=[
                    html.Div(
                        id="livestream-popup-content",
                        children=[
                            dbc.Row(
                                [
                                    dbc.Col(  
                                        html.H5("Livestream", className="card-title"),
                                    ),

                                    dbc.Col(
                                        [
                                            html.A(
                                                html.I(className="bi bi-x-lg"),
                                                id="close-livestream-popup-button",
                                            )
                                        ],
                                        class_name="d-flex justify-content-end",
                                    ),
                                ]
                            ),
                            dbc.Row(children=[html.Canvas(id="livestream-spectrogram")], className="mt-3"),
                        ],
                    ),
                    html.Div(
                        id="livestream-popup-footer",
                        className="d-flex justify-content-evenly mt-3",
                        children=[
                            html.A(html.H4(className="bi bi-pause-fill"), id='livestream-popup-play-button'),],
                    ),
                ],
            ),
        ]
    )
