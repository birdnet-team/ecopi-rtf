from dash import html, dcc
import dash_bootstrap_components as dbc

def dashboard_page_content():
    return html.Div(
        [
            dbc.Container(
                [
                    html.H1("Dashboard", className="mt-0"),
                    html.P("This is the content for the Dashboard page."),
                ],
                fluid=True,
            ),
        ]
    )