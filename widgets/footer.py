from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

import config as cfg

# Define the footer content
def footer_content():
    footer_columns = []
    for section, links in cfg.FOOTER_LINKS.items():
        footer_columns.append(
            dbc.Col(
                [
                    html.H5(section, className="small-text bold-text"),
                    html.Ul(
                        [
                            html.Li(html.A(link["name"], href=link["href"], className="footer-link small-text", target=link.get("target", "_self")))
                            for link in links
                        ],
                        className="list-unstyled"
                    )
                ],
                width=6,
                md=4,
                lg=2,
                className="mb-4 text-left"
            )
        )

    return html.Footer(
        [
            html.Div(html.Img(src=cfg.SITE_ROOT + "/assets/logo_img/clo_yangcenterconservationbioacoustics_horizontal_white.png", className="footer-logo")),
            dbc.Container(
                dbc.Row(
                    footer_columns,
                    className="justify-content-center"
                ),
                fluid=True,
                className="footer-content",
            ),
            html.Div(html.Img(src=cfg.SITE_ROOT + "/assets/logo_img/cornell-logo-white.png", className="footer-logo")),
            html.P(f"© {datetime.now().strftime('%Y')} Cornell University"),
        ],
        className="footer",
    )