from dash import html
import dash_bootstrap_components as dbc

def stats_bar():
    return html.Div(
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
    )