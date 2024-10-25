from dash import html, dcc
import dash_bootstrap_components as dbc

def recorder_page_content(recorder_id):
    return html.Div(
        [
            dbc.Container(
                [
                    html.H1(f"Recorder {recorder_id}", className="mt-0"),
                    html.P(f"This is the content for Recorder {recorder_id}."),
                ],
                fluid=True,
            ),
        ]
    )