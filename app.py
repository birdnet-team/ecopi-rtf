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
from widgets.footer import footer_content
from widgets.nav_bar import nav_bar

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
    
# Callback to toggle the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks"),
     Input("nav-home", "n_clicks"),
     Input("nav-dashboard", "n_clicks"),
     Input("nav-detections", "n_clicks"),
     Input("nav-about", "n_clicks"),
     Input("nav-donate", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n_toggler, n_home, n_dashboard, n_detections, n_about, n_donate, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "navbar-toggler":
            return not is_open
        else:
            return False

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