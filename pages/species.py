from dash import html, dcc
import dash_bootstrap_components as dbc

from utils import data_processor as dp

def species_page_content(species_id):
    species_data = dp.get_species_data(species_id)
    return html.Div(
        [
            dbc.Container(
                [
                    html.H1(f"Species: {species_data['common_name']}"),
                    html.Img(src=species_data["image_url"], className="img-fluid"),
                    html.P(f"Scientific Name: {species_data['scientific_name']}"),
                    html.A("More Info", href=species_data["ebird_url"], target="_blank", className="btn btn-href mt-4"),
                ],
                fluid=True,
                className="main-content",
            ),
        ]
    )