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
                            dbc.Col(dcc.Link(html.Img(src=cfg.SITE_ROOT + "/assets/clo_swamp_short_horizontal_black.png", className="header-logo"), href=cfg.SITE_ROOT + "/"), width="auto"),
                            #dbc.Col(html.Div(className="divider"), width="auto"),
                            #dbc.Col(dbc.NavbarBrand("SWAMP", className="ml-0"), width="auto"),
                        ],
                        align="center",
                        className="light",
                    ),
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                                dbc.NavItem(
                                    dcc.Link(
                                        [
                                            html.I(className="bi bi-house-door-fill home-icon"),
                                            html.Span("Home", className="home-text")
                                        ],
                                        href=cfg.SITE_ROOT + "/",
                                        className="nav-link",
                                        id="nav-home"
                                    )
                                ),
                                dbc.NavItem(dcc.Link("Dashboard", href=cfg.SITE_ROOT + "/dashboard", className="nav-link", id="nav-dashboard")),
                                dbc.NavItem(dcc.Link("Detections", href=cfg.SITE_ROOT + "/detections", className="nav-link", id="nav-detections")),
                                dbc.DropdownMenu(
                                    label="Recorders",
                                    children=[
                                        dbc.DropdownMenuItem(
                                            dcc.Link(f"Recorder #{recorder_id}", href=f"{cfg.SITE_ROOT}/recorder/{recorder_id}", className="dropdown-item")
                                        ) for recorder_id in cfg.RECORDERS.keys()
                                    ],
                                    nav=True,
                                ),
                                dbc.NavItem(dcc.Link("About", href=cfg.SITE_ROOT + "/about", className="nav-link", id="nav-about")),
                                dbc.NavItem(html.A("Donate", href="https://give.birds.cornell.edu/page/132162/donate/1?ea.tracking.id=ENR", className="nav-link", id="nav-donate", target="_blank")),
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