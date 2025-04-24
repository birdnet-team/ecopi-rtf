import os
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from flask_cors import CORS
from flask import request, jsonify, send_file, Response
import requests
from io import BytesIO
import hashlib

import json

from utils import data_processor as dp
from utils import plots

import config as cfg
from utils.stats import increment_site_views
from utils import data_processor as dp

# Import page content functions
from pages.main import main_page_content, register_main_callbacks
from pages.dashboard import dashboard_page_content
from pages.recorder import display_recorder_page, register_recorder_callbacks
from pages.species import register_species_callbacks, display_species_page
from pages.detections import detections_page_content, register_detections_callbacks
from pages.about import about_page_content
from pages.privacy import privacy_page_content
from widgets.footer import footer_content
from widgets.nav_bar import nav_bar

# Import callback registration function for recent detections
from widgets.recent_detections import register_recent_detections_callbacks

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        #dbc.themes.BOOTSTRAP,
    ],
    external_scripts=[
        # None for now
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
        <link rel="manifest" href="{cfg.SITE_ROOT}/{cfg.PWA_MANIFEST}">
        {{%css%}}
        
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
        <script>
            if ('serviceWorker' in navigator) {{
                navigator.serviceWorker.register("{cfg.SITE_ROOT}/assets/service-worker.js")
                .then(function(registration) {{
                    console.log('Service Worker registered with scope:', registration.scope);
                }}).catch(function(error) {{
                    console.log('Service Worker registration failed:', error);
                }});
            }}
        </script>
    </body>
</html>
"""

# Function to determine the locale from the user agent
def get_locale_from_user_agent():
    supported_locales = cfg.SUPPORTED_SITE_LOCALES.values()
    accept_language = request.headers.get('Accept-Language', '')
    for lang in accept_language.split(','):
        lang_code = lang.split(';')[0].strip()
        if lang_code in supported_locales:
            return lang_code
        if lang_code.split('-')[0] in supported_locales:
            return lang_code.split('-')[0]
    return cfg.DEFAULT_SITE_LOCALE

# Define overall layout
def app_layout(initial_locale):
    if initial_locale is None:
        initial_locale = cfg.DEFAULT_SITE_LOCALE
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),  # Track the URL
            dcc.Store(id="audio-store"),  # Store for audio URLs
            dcc.Store(id="play-audio-store"),  # Store for the audio to be played
            dcc.Store(id="species-stats-store"),  # Store for species stats
            dcc.Store(id="species-data-store"),   # Store for species data
            dcc.Store(id="recorder-stats-store"),  # Store for recorder stats
            dcc.Store(id="recorder-data-store"),   # Store for recorder data
            dcc.Store(id="locale-store", data=initial_locale),  # Store for selected locale
            html.Div(id="dummy-output"),  # Dummy output for page reload
            html.Div(id="dynamic-layout")  # Dynamic layout based on locale
        ]
    )

# Callback to update the dynamic layout based on the locale
@app.callback(
    Output("dynamic-layout", "children"),
    [Input("locale-store", "data")]
)
def update_layout(locale):
    if locale is None:
        locale = cfg.DEFAULT_SITE_LOCALE
    return html.Div(
        [
            # Header Section with Logo and Navigation Bar
            nav_bar(locale),
            
            # Content will be rendered here based on the URL
            html.Div(id="page-content"),
            
            # Footer Section
            footer_content(locale),
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
@app.callback(Output("page-content", "children"), [Input("url", "pathname"), Input("locale-store", "data")])
def display_page(pathname, locale):
    headers = request.headers
    path_parts = pathname.strip('/').split('/')
    
    # Check if the last part of the path is a locale
    if path_parts[-1].split('#')[0] in cfg.SUPPORTED_SITE_LOCALES.values():
        locale = path_parts.pop().split('#')[0]
        pathname = '/' + '/'.join(path_parts)
    
    try:
        if pathname == cfg.SITE_ROOT + "/":
            increment_site_views('main page', headers)
            return main_page_content(locale)
        elif pathname == cfg.SITE_ROOT + "/dashboard":
            increment_site_views('dashboard', headers)
            return dashboard_page_content(locale)
        elif pathname.startswith(cfg.SITE_ROOT + "/recorder/"):
            recorder_id = pathname.split("/")[-1]
            increment_site_views(f'recorder {recorder_id}', headers)
            return display_recorder_page(recorder_id, locale)
        elif pathname.startswith(cfg.SITE_ROOT + "/species/"):
            species_id = pathname.split("/")[-1]
            increment_site_views(f'species {species_id}', headers)
            return display_species_page(species_id, locale)
        elif pathname == cfg.SITE_ROOT + "/detections":
            increment_site_views('detections', headers)
            return detections_page_content(locale)
        elif pathname == cfg.SITE_ROOT + "/about":
            increment_site_views('about', headers)
            return about_page_content(locale)
        elif pathname == cfg.SITE_ROOT + "/privacy":
            increment_site_views('privacy', headers)
            return privacy_page_content(locale)
        else:
            print(f"404 Page Not Found: {pathname}")
            return "404 Page Not Found"
    except Exception as e:
        print(f"Error resolving page: {e}")
        return "An error occurred while trying to display the page. Please check the URL and try again."


# Callback to update the site locale based on the selected language
@app.callback(
    Output("locale-store", "data"),
    [Input({"type": "nav-locale", "index": ALL}, "n_clicks"), Input("url", "pathname")],
    [State("locale-store", "data")]
)
def update_locale(n_clicks, pathname, current_locale):
    ctx = dash.callback_context
    path_parts = pathname.strip('/').split('/')
    
    # Check if the last part of the path is a locale
    if path_parts[-1] in cfg.SUPPORTED_SITE_LOCALES.values():
        locale = path_parts[-1]
        if locale != current_locale:
            return locale
        return current_locale
    
    if not ctx.triggered:
        return current_locale
    else:
        try:
            locale = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])['index']
        except (json.JSONDecodeError, KeyError):
            return current_locale
        if locale != current_locale:
            return locale
        return current_locale

# Callback to reload the page when the locale is updated
@app.callback(
    Output("dummy-output", "children"),
    [Input("locale-store", "data")],
    [State("url", "href")]
)
def reload_page(locale, href):
    if locale and href:
        return dcc.Location(href=href, id="dummy-location")
    return ""

# Home page route
@app.server.route("/")
def serve_layout():
    initial_locale = get_locale_from_user_agent()
    return app_layout(initial_locale)

# Ping route
@app.server.route("/ping")
def ping():
    if dp.ping():
        return jsonify(status="ok")
    else:
        return jsonify(status="error")

@app.server.route('/assets/style/custom.css')
def custom_css():
    site_root = cfg.SITE_ROOT
    colors = f"""
    :root {{
        --primary-color: {cfg.PRIMARY_COLOR};
        --secondary-color: {cfg.SECONDARY_COLOR};
        --button-color: {cfg.BUTTON_COLOR};
        --plot-primary-color: {cfg.PLOT_PRIMARY_COLOR};
    }}
    """
    with open('assets/style/custom.css', 'r') as file:
        css_content = file.read()
    css_content = css_content.replace('{{SITE_ROOT}}', site_root)
    css_content = colors + css_content
    return Response(css_content, mimetype='text/css')

@app.server.route('/assets/js/popup.mjs')
def popup_js():
    site_root = cfg.SITE_ROOT
    with open('assets/js/popup.mjs', 'r') as file:
        js_content = file.read()
    js_content = js_content.replace('{{SITE_ROOT}}', site_root)
    return Response(js_content, mimetype='application/javascript')
    
def get_cache_filename(url, cache_dir):
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    return os.path.join(cache_dir, url_hash)

# Proxy route for images
@app.server.route("/image")
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        return send_file(os.path.join('assets', 'species_img', 'dummy_species.jpg'), mimetype='image/jpeg')

    cache_filename = get_cache_filename(image_url, 'cache/img')
    if os.path.exists(cache_filename):
        return send_file(cache_filename, mimetype='image/jpeg')

    response = requests.get(image_url)
    if response.status_code != 200:
        return send_file(os.path.join('assets', 'species_img', 'dummy_species.jpg'), mimetype='image/jpeg')

    os.makedirs('cache/img', exist_ok=True)
    with open(cache_filename, 'wb') as f:
        f.write(response.content)

    return send_file(BytesIO(response.content), mimetype=response.headers['Content-Type'])

# Proxy route for Leaflet/OSM tiles
@app.server.route("/tile")
def proxy_tile():
    tile_url = request.args.get('url')
    if not tile_url:
        return "No tile URL provided", 400

    cache_filename = get_cache_filename(tile_url, 'cache/tiles')
    if os.path.exists(cache_filename):
        return send_file(cache_filename, mimetype='image/png')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.openstreetmap.org/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    response = requests.get(tile_url, headers=headers)
    if response.status_code != 200:
        return "Failed to fetch tile", response.status_code

    os.makedirs('cache/tiles', exist_ok=True)
    with open(cache_filename, 'wb') as f:
        f.write(response.content)

    return send_file(BytesIO(response.content), mimetype=response.headers['Content-Type'])
    
# Cache costly requests
@app.server.route("/cache")
def cache():
    dp.run_cache_costly_requests()
    return jsonify(status="started")

# PWA manifest
cfg.make_pwa_manifest(cfg.PWA_MANIFEST, locale=cfg.DEFAULT_SITE_LOCALE)

# Layout of the Dash app
app.layout = serve_layout

# Register callbacks
register_main_callbacks(app)
register_recent_detections_callbacks(app)
register_species_callbacks(app)
register_recorder_callbacks(app)
register_detections_callbacks(app)

# App server
server = app.server

# Run the app on the local server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=cfg.PORT)