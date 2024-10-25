from dash import html, dcc
import dash_bootstrap_components as dbc

from utils import data_processor as dp

def species_page_content(species_id):
    species_data = dp.get_species_data(species_id)
    return html.Div(
        [
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
                                dbc.Col(
                                    html.A("Learn more", href=species_data["ebird_url"], target="_blank", className="btn btn-href learn-more-btn"),
                                    width=3,
                                    xs=5,
                                    className="d-flex align-items-center justify-content-center"
                                ),
                            ],
                            className="species-overlay-row"
                        ),
                        className="species-overlay",
                    ),
                ],
                className="species-header",
            ),
            dbc.Container(
                fluid=True,
                className="main-content",
            ),
        ],
        className="species-page-content"
    )