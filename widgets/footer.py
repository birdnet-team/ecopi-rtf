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

    footer_bottom_logos = []
    num_logos = len(cfg.FOOTER_BOTTOM_LOGOS)
    for logo in cfg.FOOTER_BOTTOM_LOGOS:
        footer_bottom_logos.append(
            dbc.Col(
                html.Div(html.Img(src=cfg.SITE_ROOT + f"/assets/logo_img/{logo}", className="footer-logo"), className="footer-logo-container"),
                width=12,
                md=6,
                lg=int(12 / num_logos),
                className="text-center"
            )
        )

    return html.Footer(
        [
            html.Div(html.Img(src=cfg.SITE_ROOT + f"/assets/logo_img/{cfg.FOOTER_TOP_LOGO}", className="footer-logo")),
            dbc.Container(
                dbc.Row(
                    footer_columns,
                    className="justify-content-center"
                ),
                fluid=True,
                className="footer-content",
            ),
            dbc.Container(
                dbc.Row(
                    footer_bottom_logos,
                    className="justify-content-center"
                ),
                fluid=True,
                className="footer-bottom-logos",
            ),
            html.P(f"© {datetime.now().strftime('%Y')} {cfg.COPYRIGHT_HOLDERS}" if len(cfg.COPYRIGHT_HOLDERS) > 0 else ""),
        ],
        className="footer",
    )