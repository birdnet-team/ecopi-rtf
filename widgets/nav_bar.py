from dash import html, dcc
import dash_bootstrap_components as dbc

from utils.strings import Strings

import config as cfg

def nav_bar(locale):  
    
    strings = Strings(locale)
      
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo, Divider, and Title in a single row
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Link(
                                html.Img(
                                    src=cfg.SITE_ROOT + f"/assets/logo_img/{cfg.LOGO_MOBILE}",
                                    className="header-logo header-logo-short",
                                    id="nav-logo-short"
                                ),
                                href=cfg.SITE_ROOT + "/"
                            ),
                            width="auto"
                        ),
                        dbc.Col(
                            dcc.Link(
                                html.Img(
                                    src=cfg.SITE_ROOT + f"/assets/logo_img/{cfg.LOGO_DESKTOP}",
                                    className="header-logo header-logo-long",
                                    id="nav-logo-long"
                                ),
                                href=cfg.SITE_ROOT + "/"
                            ),
                            width="auto"
                        ),
                    ],
                    align="center",
                    className="light",
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink(
                                    [
                                        html.I(className="bi bi-house-door-fill home-icon"),
                                        html.Span(strings.get('nav_home'), className="home-text")
                                    ],
                                    href=cfg.SITE_ROOT + "/",
                                    className="nav-link",
                                    id="nav-home"
                                )
                            ),
                            dbc.NavItem(dbc.NavLink(strings.get('nav_dashboard'), href=cfg.SITE_ROOT + "/dashboard", className="nav-link", id="nav-dashboard")),
                            dbc.NavItem(dbc.NavLink(strings.get('nav_detections'), href=cfg.SITE_ROOT + "/detections", className="nav-link", id="nav-detections")),
                            dbc.DropdownMenu(
                                label=strings.get('nav_recorder_top'),
                                children=[
                                    dbc.DropdownMenuItem(
                                        dbc.NavLink(f"{strings.get('nav_recorder')} #{recorder_id}", href=f"{cfg.SITE_ROOT}/recorder/{recorder_id}", className="dropdown-item", id=f"nav-recorder-{recorder_id}")
                                    ) for recorder_id in cfg.RECORDERS.keys()
                                ],
                                nav=True,
                            ),
                            dbc.NavItem(dbc.NavLink(strings.get('nav_about'), href=cfg.SITE_ROOT + "/about", className="nav-link", id="nav-about")),
                            dbc.DropdownMenu(
                                label=[
                                    html.I(className="bi bi-globe"),
                                    html.Span(id="locale-label", children=f" {locale.upper()}")
                                ],
                                children=[
                                    dbc.DropdownMenuItem(
                                        language, href="#", className="dropdown-item", id={"type": "nav-locale", "index": locale}
                                    ) for language, locale in cfg.SUPPORTED_SITE_LOCALES.items()
                                ],
                                nav=True,
                                in_navbar=True,
                                right=True,
                                id="locale-dropdown-menu"
                            ),
                            dbc.NavItem(html.A(strings.get('nav_donate'), href=cfg.DONATION_URL, className="nav-link nav-donate" if cfg.DONATION_URL else "d-none", id="nav-donate", target="_blank")),
                        ],
                        className="ml-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color="light",
        dark=False,
        className="mb-0 navbar-border",
        sticky="top",
    )