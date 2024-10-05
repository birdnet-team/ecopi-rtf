import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import data_processor as dp  # Import data_processor as dp

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'])

# Layout of the Dash app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Track the URL

    # Header Section with Logo and Navigation Bar
    dbc.Navbar(
        dbc.Container(
            [
                # Logo, Divider, and Title in a single row
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/clo-logo-bird.png', className="header-logo"), width="auto"),
                        
                        # Vertical Divider
                        dbc.Col(html.Div(className='divider'), width="auto"),
                        
                        # Title of the website
                        dbc.Col(dbc.NavbarBrand("SWAMP", className="ml-0"), width="auto"),
                    ],
                    align="center",
                    className="light",
                ),

                # Navbar Toggler
                dbc.NavbarToggler(id="navbar-toggler"),

                # Navbar menu on the right
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dcc.Link("Dashboard", href="/", className="nav-link")),
                            dbc.DropdownMenu(
                                label="Recorders",
                                children=[
                                    dbc.DropdownMenuItem(dcc.Link("Recorder 1", href="/recorder/1", className="dropdown-item")),
                                    dbc.DropdownMenuItem(dcc.Link("Recorder 2", href="/recorder/2", className="dropdown-item")),
                                    dbc.DropdownMenuItem(dcc.Link("Recorder 3", href="/recorder/3", className="dropdown-item")),
                                    dbc.DropdownMenuItem(dcc.Link("Recorder 4", href="/recorder/4", className="dropdown-item")),
                                    dbc.DropdownMenuItem(dcc.Link("Recorder 5", href="/recorder/5", className="dropdown-item")),
                                    dbc.DropdownMenuItem(dcc.Link("Recorder 6", href="/recorder/6", className="dropdown-item")),
                                    dbc.DropdownMenuItem(dcc.Link("Recorder 7", href="/recorder/7", className="dropdown-item")),
                                ],
                                nav=True,
                            ),
                            dbc.NavItem(dcc.Link("About", href="/about", className="nav-link")),
                        ],
                        className="ml-auto",  # Align items to the right
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
            fluid=True,  # Make the header container fluid
        ),
        color="light",  # Background color
        dark=False,  # White text
        className="mb-0 navbar-border",  # Add bottom margin and custom class
        sticky="top",  # Stick the navbar to the top
    ),

    # Content will be rendered here based on the URL
    html.Div(id='page-content')
])

# Define the content for the main page
main_page_content = html.Div([
    # Full-width Header Image (below the navbar)
    html.Div(
        html.Img(src='/assets/swamp_header.jpg', className="header-graphic")
    ),

    # Dark gray row with four columns, responsive to 2x2 on narrow screens
    dbc.Row(
        [            
            dbc.Col(html.Div([
                html.Div("Detections (24h):"),
                html.H5(id="detections-24h", children="0")
            ]), className="stat-column", width=6, md=3),
            dbc.Col(html.Div([
                html.Div("Species (24h):"),
                html.H5(id="species-24h", children="0")
            ]), className="stat-column", width=6, md=3),
            dbc.Col(html.Div([
                html.Div("Detections (total):"),
                html.H5(id="total-detections", children="0")
            ]), className="stat-column", width=6, md=3),
            dbc.Col(html.Div([
                html.Div("Audio (total):"),
                html.H5(id="total-audio", children="0")
            ]), className="stat-column", width=6, md=3),
        ],
        className="stat-row"
    ),
    
    # Spacer between the statistics and the main content
    html.Div(className="h-spacer"),

    # Main Content Section
    dbc.Container(
        [
            html.H3("Sapsucker Woods Acoustic Monitoring Project", className="mt-1"),
            html.P("This is where the content of your page goes."),
            html.P("You can add graphs, charts, or any other interactive components here."),
            
            # Recent detections
            html.H5("Recent Detections:", className="mt-4"),
            dbc.Row(id='last-detections', className="mt-4"),
            dbc.Spinner(html.Div(id='no-detections-placeholder', className="mt-4"), color="#b31b1b")
            
        ],
        fluid=True,  # Make the content container fluid (adjusts to screen size)
        className="main-content"
    ),
])

# Define the content for the recorder subpages
def recorder_page_content(recorder_id):
    return html.Div([
        # Main Content Section
        dbc.Container(
            [
                html.H1(f"Recorder {recorder_id}", className="mt-0"),
                html.P(f"This is the content for Recorder {recorder_id}."),
                # Add more components or visualizations as needed
            ],
            fluid=True,  # Make the content container fluid (adjusts to screen size)
        ),
    ])

# Define the content for the about page
about_page_content = html.Div([
    # Main Content Section
    dbc.Container(
        [
            html.H1("About SWAMP", className="mt-0"),
            html.P("This is the about page content."),
            # Add more components or visualizations as needed
        ],
        fluid=True,  # Make the content container fluid (adjusts to screen size)
    ),
])

# Define the footer content
footer_content = html.Footer(
    [
        # Top Logo
        html.Div(
            html.Img(src='/assets/cornell-lab-logo-full-white.png', className="footer-logo")
        ),
        
        # Two-column content, responsive to single column on narrow screens
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("K. Lisa Yang Center for Conservation Bioacoustics"),
                                html.P("We collect and interpret sounds in nature by developing, applying, and sharing innovative conservation technologies across relevant scales to inform and advance the conservation of wildlife and habitats.", style={'textAlign': 'justify'}),
                                html.H5("SWAMP"),
                                html.P("The Sapsucker Woods Acoustic Monitoring Project (SWAMP) is an effort to study bird biodiversity in Sapsucker Woods through acoustic monitoring and advanced AI models for bird call identification. SWAMP is a collaboration between Cornell University, Chemnitz University of Technology and OekoFor GbR.", style={'textAlign': 'justify'}),
                            ],
                            style={'padding-right': '5px'}
                        ),
                        width=12, md=6,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("BirdNET - Bird Sound Identification"),
                                html.P("BirdNET is an advanced AI for bird call identification. BirdNET is supported by Jake Holshuh (Cornell class of '69) and the Arthur Vining Davis Foundation. Our work at the K. Lisa Yang Center for Conservation Bioacoustics is made possible by the generosity of K. Lisa Yang to advance innovative conservation technologies to inspire and inform wildlife and habitat conservation.", style={'textAlign': 'justify'}),
                                html.P("The German Federal Ministry of Education and Research is funding the development of BirdNET through the project 'BirdNET+' (FKZ 01|S22072). Additionally, the German Federal Ministry of Environment, Nature Conservation and Nuclear Safety is funding the development of BirdNET through the project 'DeepBirdDetect' (FKZ 67KI31040E).", style={'textAlign': 'justify'}),
                            ],
                            style={'padding-left': '5px'}
                        ),
                        width=12, md=6,
                    ),
                ]
            ),
            fluid=True,
            className="footer-content"
        ),
        
        # Bottom Logo
        html.Div(
            html.Img(src='/assets/cornell-logo-white.png', className="footer-logo")
        ),
        
        # Copyright text
        html.P("© 2024 Cornell University")
    ],
    className="footer"
)

# Callback to toggle the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [dash.dependencies.State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return [main_page_content, footer_content]
    elif pathname.startswith('/recorder/'):
        recorder_id = pathname.split('/')[-1]
        return [recorder_page_content(recorder_id), footer_content]
    elif pathname == '/about':
        return [about_page_content, footer_content]
    else:
        return [html.H1("404: Not found"), footer_content]

# Callback to update the statistics
@app.callback(
    [Output('total-detections', 'children'),
     Output('detections-24h', 'children'),
     Output('species-24h', 'children'),
     Output('total-audio', 'children')],
    [Input('url', 'pathname')]
)
def update_statistics(pathname):
    total_detections = dp.get_total_detections()
    detections_24h = dp.get_total_detections(days=1)
    species_24h = len(detections_24h['species_counts'])
    total_audio = total_detections['total_detections'] * 5  # Assuming 5 seconds of audio per detection
    
    # Format the numbers with commas as thousand separators
    total_detections_formatted = f"{total_detections['total_detections']:,}"
    detections_24h_formatted = f"{detections_24h['total_detections']:,}"
    species_24h_formatted = f"{species_24h:,}"
    # show total ausio as 45d 12h 37m
    total_audio_formatted = f"{total_audio // 86400}d {total_audio % 86400 // 3600}h {total_audio % 3600 // 60}m"
    
    return total_detections_formatted, detections_24h_formatted, species_24h_formatted, total_audio_formatted

# Callback to update the last detections
@app.callback(
    [Output('last-detections', 'children'),
     Output('no-detections-placeholder', 'children')],
    [Input('url', 'pathname')]
)
def update_last_detections(pathname):
    last_detections = dp.get_last_n_detections()
    cards = []
    for species, data in last_detections.items():
        card = dbc.Col(
            dbc.Card(
                [
                    dbc.CardImg(src=data['url_media'], top=True),
                    dbc.CardBody(
                        [
                            html.H5(species, className="card-title"),
                            html.Audio(src=data['url_media'], controls=True, className="w-100")
                        ]
                    ),
                ],
                className="mb-4"
            ),
            width=12, sm=6, md=4  # Adjust the width for different screen sizes
        )
        cards.append(card)
    
    if not cards:
        placeholder = html.P("No recent detections available.", className="text-muted")
    else:
        placeholder = None
    
    return cards, placeholder

# Run the app on the local server
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)