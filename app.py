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
from pages.recorder import recorder_page_content
from pages.species import species_page_content, register_species_callbacks
from pages.about import about_page_content

# Import callback registration function for recent detections
from widgets.recent_detections import register_recent_detections_callbacks

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        # "/assets/custom.css", # Not required
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css",
    ],
    suppress_callback_exceptions=True,  # Suppress the warning for dynamic callbacks
    title="SWAMP",
    update_title=None,
    #requests_pathname_prefix="/swamp/",
    #routes_pathname_prefix="/swamp/",
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
                            dbc.Col(html.Img(src="/assets/clo-logo-bird.png", className="header-logo"), width="auto"),
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
                                        href="/",
                                        className="nav-link",
                                        id="nav-home"
                                    )
                                ),
                                dbc.NavItem(dcc.Link("Dashboard", href="/dashboard", className="nav-link", id="nav-dashboard")),
                                dbc.DropdownMenu(
                                    label="Recorders",
                                    children=[
                                        dbc.DropdownMenuItem(
                                            dcc.Link(f"Recorder {recorder_id}", href=f"/recorder/{recorder_id}", className="dropdown-item")
                                        ) for recorder_id in cfg.RECORDERS.keys()
                                    ],
                                    nav=True,
                                ),
                                dbc.NavItem(dcc.Link("About", href="/about", className="nav-link", id="nav-about")),
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
            # Top Logo
            html.Div(html.Img(src="/assets/cornell-lab-logo-full-white.png", className="footer-logo")),
            # Two-column content, responsive to single column on narrow screens
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
                                        "BirdNET is an advanced AI for bird call identification. BirdNET is supported by Jake Holshuh (Cornell class of '69) and the Arthur Vining Davis Foundation. Our work at the K. Lisa Yang Center for Conservation Bioacoustics is made possible by the generosity of K. Lisa Yang to advance innovative conservation technologies to inspire and inform wildlife and habitat conservation.",
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
            # Bottom Logo
            html.Div(html.Img(src="/assets/cornell-logo-white.png", className="footer-logo")),
            # Copyright text
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
     Output("nav-about", "className")],
    [Input("url", "pathname")]
)
def update_active_nav(pathname):
    home_class = "nav-link active-nav" if pathname == "/" else "nav-link"
    dashboard_class = "nav-link active-nav" if pathname == "/dashboard" else "nav-link"
    about_class = "nav-link active-nav" if pathname == "/about" else "nav-link"
    return home_class, dashboard_class, about_class

# Callback to update the page content based on the URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return main_page_content()
    elif pathname == "/dashboard":
        return dashboard_page_content()
    elif pathname.startswith("/recorder/"):
        recorder_id = pathname.split("/")[-1]
        return recorder_page_content(recorder_id)
    elif pathname.startswith("/species/"):
        species_id = pathname.split("/")[-1]
        return species_page_content(species_id)
    elif pathname == "/about":
        return about_page_content()
    else:
        return "404 Page Not Found"

# Layout of the Dash app
app.layout = app_layout()

# Register callbacks from main.py
register_main_callbacks(app)

# Register callbacks from recent_detections.py
register_recent_detections_callbacks(app)

# Register callbacks from species.py
register_species_callbacks(app)

# App server
server = app.server

# Run the app on the local server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)