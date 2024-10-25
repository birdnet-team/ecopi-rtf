from dash import html, dcc
import dash_bootstrap_components as dbc

def about_page_content():
    return html.Div(
        [
            dbc.Container(
                [
                    html.H1("About SWAMP", className="mt-0"),
                    html.P("This is the about page content."),
                ],
                fluid=True,
            ),
        ]
    )