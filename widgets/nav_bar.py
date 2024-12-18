from dash import html, dcc
import dash_bootstrap_components as dbc

import config as cfg

def nav_bar():    
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
                                        html.Span("Home", className="home-text")
                                    ],
                                    href=cfg.SITE_ROOT + "/",
                                    className="nav-link",
                                    id="nav-home"
                                )
                            ),
                            dbc.NavItem(dbc.NavLink("Dashboard", href=cfg.SITE_ROOT + "/dashboard", className="nav-link", id="nav-dashboard")),
                            dbc.NavItem(dbc.NavLink("Detections", href=cfg.SITE_ROOT + "/detections", className="nav-link", id="nav-detections")),
                            dbc.DropdownMenu(
                                label="Recorders",
                                children=[
                                    dbc.DropdownMenuItem(
                                        dbc.NavLink(f"Recorder #{recorder_id}", href=f"{cfg.SITE_ROOT}/recorder/{recorder_id}", className="dropdown-item", id=f"nav-recorder-{recorder_id}")
                                    ) for recorder_id in cfg.RECORDERS.keys()
                                ],
                                nav=True,
                            ),
                            dbc.NavItem(dbc.NavLink("About", href=cfg.SITE_ROOT + "/about", className="nav-link", id="nav-about")),
                            dbc.NavItem(html.A("Donate", href=cfg.DONATION_URL, className="nav-link nav-donate" if cfg.DONATION_URL else "d-none", id="nav-donate", target="_blank")),
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