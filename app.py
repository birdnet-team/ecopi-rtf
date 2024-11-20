import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
from flask_cors import CORS

from utils import data_processor as dp
from utils import plots

import config as cfg

# Import page content functions
from pages.main import main_page_content, register_main_callbacks
from pages.dashboard import dashboard_page_content
from pages.recorder import display_recorder_page, register_recorder_callbacks
from pages.species import register_species_callbacks, display_species_page
from pages.detections import detections_page_content
from pages.about import about_page_content

# Import callback registration function for recent detections
from widgets.recent_detections import register_recent_detections_callbacks

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css",
    ],
    external_scripts=[
        "https://d3js.org/d3.v6.min.js",
        "https://d3js.org/d3-scale-chromatic.v1.min.js"
    ],
    suppress_callback_exceptions=True,
    title="SWAMP",
    update_title=None,
    requests_pathname_prefix="/" if cfg.SITE_ROOT == "" else cfg.SITE_ROOT + "/",
)

# Enable CORS
CORS(app.server)

# Define overall layout
def app_layout():
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),  # Track the URL
            dcc.Store(id="audio-store"),  # Store for audio URLs
            dcc.Store(id="play-audio-store"),  # Store for the audio to be played
            dcc.Store(id="species-stats-store"),  # Store for species stats
            dcc.Store(id="species-data-store"),   # Store for species data
            dcc.Store(id="recorder-stats-store"),  # Store for recorder stats
            dcc.Store(id="recorder-data-store"),   # Store for recorder data
            
            # Header Section with Logo and Navigation Bar
            nav_bar(),
            
            # Content will be rendered here based on the URL
            html.Div(id="page-content"),
            
            # Footer Section
            footer_content(),
        ]
    )

# Define nav bar
def nav_bar():    
    return dbc.Navbar(
            dbc.Container(
                [
                    # Logo, Divider, and Title in a single row
                    dbc.Row(
                        [
                            dbc.Col(dcc.Link(html.Img(src=cfg.SITE_ROOT + "/assets/clo-logo-bird.png", className="header-logo"), href=cfg.SITE_ROOT + "/"), width="auto"),
                            dbc.Col(html.Div(className="divider"), width="auto"),
                            dbc.Col(dbc.NavbarBrand("SWAMP", className="ml-0"), width="auto"),
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

# Callback to toggle the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    return not is_open if n else is_open

# Callback to update the active nav link based on the URL
@app.callback(
    [Output("nav-home", "className"),
     Output("nav-dashboard", "className"),
     Output("nav-detections", "className"),
     Output("nav-about", "className")],
    [Input("url", "pathname")]
)
def update_active_nav(pathname):
    home_class = "nav-link active-nav" if pathname == cfg.SITE_ROOT + "/" else "nav-link"
    dashboard_class = "nav-link active-nav" if pathname == cfg.SITE_ROOT + "/dashboard" else "nav-link"
    detections_class = "nav-link active-nav" if pathname == cfg.SITE_ROOT + "/detections" else "nav-link"
    about_class = "nav-link active-nav" if pathname == cfg.SITE_ROOT + "/about" else "nav-link"
    return home_class, dashboard_class, detections_class, about_class

# Callback to update the page content based on the URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == cfg.SITE_ROOT + "/":
        return main_page_content()
    elif pathname == cfg.SITE_ROOT + "/dashboard":
        return dashboard_page_content()
    elif pathname.startswith(cfg.SITE_ROOT + "/recorder/"):
        recorder_id = pathname.split("/")[-1]
        return display_recorder_page(recorder_id)
    elif pathname.startswith(cfg.SITE_ROOT + "/species/"):
        species_id = pathname.split("/")[-1]
        return display_species_page(species_id)
    elif pathname == cfg.SITE_ROOT + "/detections":
        return detections_page_content()
    elif pathname == cfg.SITE_ROOT + "/about":
        return about_page_content()
    else:
        print(f"404 Page Not Found: {pathname}")
        return "404 Page Not Found"

# Layout of the Dash app
app.layout = app_layout()

# Register callbacks
register_main_callbacks(app)
register_recent_detections_callbacks(app)
register_species_callbacks(app)
register_recorder_callbacks(app)

# App server
server = app.server

# Run the app on the local server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)