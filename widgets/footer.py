from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

import config as cfg

# Define the footer content
def footer_content():
    return html.Footer(
        [
            html.Div(html.Img(src=cfg.SITE_ROOT + "/assets/logo_img/clo_yangcenterconservationbioacoustics_horizontal_white.png", className="footer-logo")),
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H6("Site Links", className="small-text bold-text"),
                                html.Ul(
                                    [
                                        html.Li(html.A("Home", href=f"{cfg.SITE_ROOT}/", className="footer-link small-text")),
                                        html.Li(html.A("Detections", href=f"{cfg.SITE_ROOT}/detections", className="footer-link small-text")),
                                        html.Li(html.A("Recording units", href=f"{cfg.SITE_ROOT}/recorder/1", className="footer-link small-text")),
                                        html.Li(html.A("About the project", href=f"{cfg.SITE_ROOT}/about", className="footer-link small-text")),
                                    ],
                                    className="list-unstyled"
                                )
                            ],
                            width=6,
                            md=4,
                            lg=2,
                            className="mb-4 text-left"
                        ),
                        dbc.Col(
                            [
                                html.H5("Yang Center", className="small-text bold-text"),
                                html.Ul(
                                    [
                                        html.Li(html.A("Our values", href="https://www.birds.cornell.edu/ccb/our-values/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Research", href="https://www.birds.cornell.edu/ccb/research/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Technology", href="https://www.birds.cornell.edu/ccb/technology/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Education", href="https://www.birds.cornell.edu/ccb/education/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Publications", href="https://www.birds.cornell.edu/ccb/publications/", className="footer-link small-text", target="_blank")),
                                    ],
                                    className="list-unstyled"
                                )
                            ],
                            width=6,
                            md=4,
                            lg=2,
                            className="mb-4 text-left"
                        ),
                        dbc.Col(
                            [
                                html.H5("Explore More", className="small-text bold-text"),
                                html.Ul(
                                    [
                                        html.Li(html.A("Bird Cams", href="https://www.allaboutbirds.org/cams/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Birds of the World", href="https://birdsoftheworld.org/bow/home", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("eBird Status and Trends", href="https://science.ebird.org/status-and-trends", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Our Youtube Videos", href="https://www.youtube.com/labofornithology", className="footer-link small-text", target="_blank")),
                                    ],
                                    className="list-unstyled"
                                )
                            ],
                            width=6,
                            md=4,
                            lg=2,
                            className="mb-4 text-left"
                        ),
                        dbc.Col(
                            [
                                html.H5("Lifelong Learning", className="small-text bold-text"),
                                html.Ul(
                                    [
                                        html.Li(html.A("Online Courses", href="https://academy.allaboutbirds.org/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Bird Walks & Events", href="https://www.birds.cornell.edu/home/visit/events/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Spring Field Ornithology", href="https://academy.allaboutbirds.org/product/spring-field-ornithology-northeast/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("K–12 Education", href="https://www.birds.cornell.edu/k12", className="footer-link small-text", target="_blank")),
                                    ],
                                    className="list-unstyled"
                                )
                            ],
                            width=6,
                            md=4,
                            lg=2,
                            className="mb-4 text-left"
                        ),
                        dbc.Col(
                            [
                                html.H5("Support Our Cause", className="small-text bold-text"),
                                html.Ul(
                                    [
                                        html.Li(html.A("Join the Lab", href="https://join.birds.cornell.edu/page/150611/donate/1?ea.tracking.id=WXXXXX14C", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Donate", href="https://give.birds.cornell.edu/page/132162/donate/1?ea.tracking.id=ENR", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Monthly Giving", href="https://give.birds.cornell.edu/page/99134/donate/1?ea.tracking.id=BCF", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Membership Services", href="https://www.birds.cornell.edu/home/members/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Shop for Our Cause", href="https://www.birds.cornell.edu/home/shop-for-our-cause/", className="footer-link small-text", target="_blank")),
                                    ],
                                    className="list-unstyled"
                                )
                            ],
                            width=6,
                            md=4,
                            lg=2,
                            className="mb-4 text-left"
                        ),
                        dbc.Col(
                            [
                                html.H5("About", className="small-text bold-text"),
                                html.Ul(
                                    [
                                        html.Li(html.A("Cornell Lab of Ornithology", href="http://birds.cornell.edu/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Web Accessibility Assistance", href="https://www.birds.cornell.edu/home/web-accessibility-assistance/", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Privacy Policy", href="https://privacy.cornell.edu/information-use-cornell", className="footer-link small-text", target="_blank")),
                                        html.Li(html.A("Terms of Use", href="https://www.birds.cornell.edu/home/terms-of-use/", className="footer-link small-text", target="_blank")),
                                    ],
                                    className="list-unstyled"
                                )
                            ],
                            width=6,
                            md=4,
                            lg=2,
                            className="mb-4 text-left"
                        ),
                    ],
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