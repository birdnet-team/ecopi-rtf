from dash import html, dcc
import dash_bootstrap_components as dbc

import config as cfg

# Define the footer content
def footer_content():
    return html.Footer(
        [
            html.Div(html.Img(src=cfg.SITE_ROOT + "/assets/cornell-lab-logo-full-white.png", className="footer-logo")),
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("K. Lisa Yang Center for Conservation Bioacoustics"),
                                    html.P(
                                        "We collect and interpret sounds in nature by developing, applying, and sharing innovative conservation technologies across relevant scales to inform and advance the conservation of wildlife and habitats.",
                                        style={"textAlign": "justify"},
                                    ),
                                    html.H5("SWAMP"),
                                    html.P(
                                        "The Sapsucker Woods Acoustic Monitoring Project (SWAMP) is an effort to study bird biodiversity in Sapsucker Woods through acoustic monitoring and advanced AI models for bird call identification. SWAMP is a collaboration between Cornell University, Chemnitz University of Technology and OekoFor GbR.",
                                        style={"textAlign": "justify"},
                                    ),
                                ],
                                style={"paddingRight": "5px"},
                            ),
                            width=12,
                            md=6,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("BirdNET - Bird Sound Identification"),
                                    html.P(
                                        "BirdNET is an advanced AI for bird call identification and poweres this project. BirdNET is supported by Jake Holshuh (Cornell class of '69) and the Arthur Vining Davis Foundation. Our work at the K. Lisa Yang Center for Conservation Bioacoustics is made possible by the generosity of K. Lisa Yang to advance innovative conservation technologies to inspire and inform wildlife and habitat conservation.",
                                        style={"textAlign": "justify"},
                                    ),
                                    html.P(
                                        "The German Federal Ministry of Education and Research is funding the development of BirdNET through the project 'BirdNET+' (FKZ 01|S22072). Additionally, the German Federal Ministry of Environment, Nature Conservation and Nuclear Safety is funding the development of BirdNET through the project 'DeepBirdDetect' (FKZ 67KI31040E).",
                                        style={"textAlign": "justify"},
                                    ),
                                ],
                                style={"paddingLeft": "5px"},
                            ),
                            width=12,
                            md=6,
                        ),
                    ]
                ),
                fluid=True,
                className="footer-content",
            ),
            html.Div(html.Img(src=cfg.SITE_ROOT + "/assets/cornell-logo-white.png", className="footer-logo")),
            html.P("© 2024 Cornell University"),
        ],
        className="footer",
    )