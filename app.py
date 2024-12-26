import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from flask_cors import CORS
from flask import request

import json

from utils import data_processor as dp
from utils import plots

import config as cfg
from utils.stats import increment_site_views

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

# Set dynamic CSS colors
with open(f"assets/style/{cfg.PROJECT_ACRONYM.lower()}_colors.css", 'w') as file:
    file.write(
        f""":root {{\n\t--primary-color: {cfg.PRIMARY_COLOR};\n\t--secondary-color: {cfg.SECONDARY_COLOR};\n\t--button-color: {cfg.BUTTON_COLOR};\n\t--plot-primary-color: {cfg.PLOT_PRIMARY_COLOR};\n}}"""
        )

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
    title=cfg.PAGE_TITLE,
    update_title=None,
    requests_pathname_prefix="/" if cfg.SITE_ROOT == "" else cfg.SITE_ROOT + "/",
)

# Enable CORS
CORS(app.server)

# Define custom index string to include custom favicon and CSS
app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        <link rel="icon" type="image/x-icon" href="{cfg.SITE_ROOT}/assets/{cfg.FAVICON}">
        {{%css%}}
        <link rel="stylesheet" href="{cfg.SITE_ROOT}/assets/style/{cfg.PROJECT_ACRONYM.lower()}_colors.css">
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

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
            dcc.Store(id="locale-store"),  # Store for selected locale
            html.Div(id="dummy-output"),  # Dummy output for page reload
            
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
     Input("nav-logo-short", "n_clicks"),
     Input("nav-logo-long", "n_clicks"),
     Input("nav-home", "n_clicks"),
     Input("nav-dashboard", "n_clicks"),
     Input("nav-detections", "n_clicks"),
     Input("nav-about", "n_clicks"),
     Input("nav-donate", "n_clicks"),
     Input({"type": "nav-recorder", "index": ALL}, "n_clicks"),
     Input({"type": "nav-locale", "index": ALL}, "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n_toggler, n_logo_short, n_logo_long, n_home, n_dashboard, n_detections, n_about, n_donate, n_recorders, n_locales, is_open):
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
    user_agent = request.headers.get('User-Agent')
    if pathname == cfg.SITE_ROOT + "/":
        increment_site_views('main page', user_agent)
        return main_page_content()
    elif pathname == cfg.SITE_ROOT + "/dashboard":
        increment_site_views('dashboard', user_agent)
        return dashboard_page_content()
    elif pathname.startswith(cfg.SITE_ROOT + "/recorder/"):
        recorder_id = pathname.split("/")[-1]
        increment_site_views(f'recorder {recorder_id}', user_agent)
        return display_recorder_page(recorder_id)
    elif pathname.startswith(cfg.SITE_ROOT + "/species/"):
        species_id = pathname.split("/")[-1]
        increment_site_views(f'species {species_id}', user_agent)
        return display_species_page(species_id)
    elif pathname == cfg.SITE_ROOT + "/detections":
        increment_site_views('detections', user_agent)
        return detections_page_content()
    elif pathname == cfg.SITE_ROOT + "/about":
        increment_site_views('about', user_agent)
        return about_page_content()
    else:
        print(f"404 Page Not Found: {pathname}")
        return "404 Page Not Found"

# Callback to update the site locale based on the selected language
@app.callback(
    [Output("locale-store", "data"), Output("locale-label", "children")],
    [Input({"type": "nav-locale", "index": ALL}, "n_clicks")],
    [State("url", "href")]
)
def update_locale(n_clicks, href):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", f" {cfg.SITE_LOCALE.upper()}"
    else:
        locale = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index']
        cfg.SITE_LOCALE = locale
        return locale, f" {locale.upper()}"

# Callback to reload the page when the locale is updated
@app.callback(
    Output("dummy-output", "children"),
    [Input("locale-store", "data")]
)
def reload_page(locale):
    if locale:
        return dcc.Location(href=cfg.SITE_ROOT + "/", id="dummy-location")
    return ""

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
    app.run(debug=True, host='0.0.0.0', port=cfg.PORT)