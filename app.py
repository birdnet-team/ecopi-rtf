import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import data_processor as dp
import plots

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "/assets/custom.css",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.1/font/bootstrap-icons.min.css",
    ],
    suppress_callback_exceptions=True,  # Suppress the warning for dynamic callbacks
    title="SWAMP",
    update_title=None,
)

# Layout of the Dash app
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),  # Track the URL
        dcc.Store(id="audio-store"),  # Store for audio URLs
        dcc.Store(id="play-audio-store"),  # Store for the audio to be played
        
        # Header Section with Logo and Navigation Bar
        dbc.Navbar(
            dbc.Container(
                [
                    # Logo, Divider, and Title in a single row
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="/assets/clo-logo-bird.png", className="header-logo"), width="auto"),
                            # Vertical Divider
                            dbc.Col(html.Div(className="divider"), width="auto"),
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
                                        dbc.DropdownMenuItem(
                                            dcc.Link("Recorder 1", href="/recorder/1", className="dropdown-item")
                                        ),
                                        dbc.DropdownMenuItem(
                                            dcc.Link("Recorder 2", href="/recorder/2", className="dropdown-item")
                                        ),
                                        dbc.DropdownMenuItem(
                                            dcc.Link("Recorder 3", href="/recorder/3", className="dropdown-item")
                                        ),
                                        dbc.DropdownMenuItem(
                                            dcc.Link("Recorder 4", href="/recorder/4", className="dropdown-item")
                                        ),
                                        dbc.DropdownMenuItem(
                                            dcc.Link("Recorder 5", href="/recorder/5", className="dropdown-item")
                                        ),
                                        dbc.DropdownMenuItem(
                                            dcc.Link("Recorder 6", href="/recorder/6", className="dropdown-item")
                                        ),
                                        dbc.DropdownMenuItem(
                                            dcc.Link("Recorder 7", href="/recorder/7", className="dropdown-item")
                                        ),
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
        html.Div(id="page-content"),
    ]
)

# Define the content for the main page
main_page_content = html.Div(
    [
        # Full-width Header Image (below the navbar)
        html.Div(
            [
                html.Img(src="/assets/swamp_header.jpg", className="header-graphic"),
                html.Div(
                    [
                        html.H1("SWAMP: Sapsucker Woods Acoustic Monitoring Project"),
                        html.H2("AI-powered acoustic monitoring"),
                    ],
                    className="header-overlay"
                ),
                html.Button(
                    [html.I(className="bi bi-volume-up-fill"), " Listen live"],
                    className="listen-live-button"
                ),
            ],
            style={"position": "relative"}  # Ensure the button is positioned relative to the image
        ),
        
        
        # Dark gray row with four columns, responsive to 2x2 on narrow screens
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div([html.Div("Detections (24h):"), html.H4(id="detections-24h", children="0")]),
                        className="stat-column",
                        width=6,
                        md=3,
                    ),
                    dbc.Col(
                        html.Div([html.Div("Species (24h):"), html.H4(id="species-24h", children="0")]),
                        className="stat-column",
                        width=6,
                        md=3,
                    ),
                    dbc.Col(
                        html.Div([html.Div("Detections (total):"), html.H4(id="total-detections", children="0")]),
                        className="stat-column",
                        width=6,
                        md=3,
                    ),
                    dbc.Col(
                        html.Div([html.Div("Audio (total):"), html.H4(id="total-audio", children="0")]),
                        className="stat-column",
                        width=6,
                        md=3,
                    ),
                ],
                className="stat-row-container",
            ),
            className="stat-row",
        ),
        # Spacer between the statistics and the main content
        html.Div(className="h-spacer"),
        # Main Content Section
        dbc.Container(
            [
                # Heading on small screens
                html.Div(
                    [
                        html.H1("SWAMP: Sapsucker Woods Acoustic Monitoring Project"),
                        #html.H2("AI-powered acoustic monitoring"),
                    ],
                    className="header-text"
                ),
                
                #html.P("This is where the content of your page goes."),
                #html.P("You can add graphs, charts, or any other interactive components here."),
                html.H5("We listen to the sounds of the animals in Sapsucker Woods and track species diversity over large spatio-temporal scales.", 
                        className="text-center d-none d-lg-block"),
                
                # Most active species
                html.Div(className="divider-container", children=[
                    html.Div(className="divider-line"),
                    html.H5("Most active species (24h)", className="divider-heading"),
                    html.Div(className="divider-line")
                ]),
                dbc.Row(id="most-active-species", className="mt-4"),
                dbc.Spinner(html.Div(id="no-active-species-placeholder", className="spinner"), color="#b31b1b"),

                # Recent detections
                html.Div(className="divider-container", children=[
                    html.Div(className="divider-line"),
                    html.H5("Recent detections", className="divider-heading"),
                    html.Div(className="divider-line")
                ]),
                dbc.Row(id="last-detections", className="mt-4"),
                dbc.Spinner(html.Div(id="no-detections-placeholder", className="spinner"), color="#b31b1b"),
            ],
            fluid=True,  # Make the content container fluid (adjusts to screen size)
            className="main-content",
        ),
    ]
)


# Define the content for the recorder subpages
def recorder_page_content(recorder_id):
    return html.Div(
        [
            # Main Content Section
            dbc.Container(
                [
                    html.H1(f"Recorder {recorder_id}", className="mt-0"),
                    html.P(f"This is the content for Recorder {recorder_id}."),
                    # Add more components or visualizations as needed
                ],
                fluid=True,  # Make the content container fluid (adjusts to screen size)
            ),
        ]
    )


# Define the content for the about page
about_page_content = html.Div(
    [
        # Main Content Section
        dbc.Container(
            [
                html.H1("About SWAMP", className="mt-0"),
                html.P("This is the about page content."),
                # Add more components or visualizations as needed
            ],
            fluid=True,  # Make the content container fluid (adjusts to screen size)
        ),
    ]
)

# Define the footer content
footer_content = html.Footer(
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
    [dash.dependencies.State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    return not is_open if n else is_open


# Callback to update the page content based on the URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return [main_page_content, footer_content]
    elif pathname.startswith("/recorder/"):
        recorder_id = pathname.split("/")[-1]
        return [recorder_page_content(recorder_id), footer_content]
    elif pathname == "/about":
        return [about_page_content, footer_content]
    else:
        return [html.H1("404: Not found"), footer_content]


# Callback to update the statistics
@app.callback(
    [
        Output("total-detections", "children"),
        Output("detections-24h", "children"),
        Output("species-24h", "children"),
        Output("total-audio", "children"),
    ],
    [Input("url", "pathname")],
)
def update_statistics(pathname):
    total_detections = dp.get_total_detections()
    detections_24h = dp.get_total_detections(days=1)
    species_24h = len(detections_24h["species_counts"])
    total_audio = total_detections["total_detections"] * 5  # Assuming 5 seconds of audio per detection

    # Format the numbers with commas as thousand separators
    total_detections_formatted = f"{total_detections['total_detections']:,}"
    detections_24h_formatted = f"{detections_24h['total_detections']:,}"
    species_24h_formatted = f"{species_24h:,}"
    total_audio_formatted = f"{total_audio // 86400}d {total_audio % 86400 // 3600}h {total_audio % 3600 // 60}m"

    return total_detections_formatted, detections_24h_formatted, species_24h_formatted, total_audio_formatted


# Callback to load recent detections and populate the cards
@app.callback(
    [
        Output("last-detections", "children"), 
        Output("no-detections-placeholder", "children")
    ], 
    [Input("url", "pathname")]
)
def update_last_detections(pathname):
    last_detections = dp.get_last_n_detections()
    cards = []

    for idx, (species, data) in enumerate(last_detections.items()):
        confidence_score = data['confidence'] * 10
        card = dbc.Col(
            dbc.Card(
                [
                    html.Div(
                        [
                            dbc.CardImg(src=data["image_url"], top=True, className="card-img-top"),
                            html.Div(
                                # Wrapping the play icon inside a clickable Div
                                html.Div(
                                    [html.I(className="bi bi-play-circle-fill", id=f"play-icon-{idx}")],
                                    id={"type": "play-icon", "index": idx},
                                ),
                                className="play-icon-overlay",
                            ),
                            html.A(
                                # Wrapping the info icon inside an <a> tag
                                html.I(className="bi bi-info-circle-fill"),
                                href=data["ebird_url"],
                                target="_blank",
                                className="info-icon-overlay",
                            ),
                            html.Div(
                                f"Photo: {data['image_author']}",
                                className="photo-author-overlay",
                            ),
                        ],
                        style={"position": "relative"},  # Ensure the overlay is positioned relative to the image
                    ),
                    dbc.CardBody(
                        [
                            html.H5(data["common_name"], className="card-title"),
                            html.P(data["scientific_name"], className="card-subtitle mb-2 text-muted"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(f"Date: {data['datetime']}", className="very-small-text"),
                                            html.Div(f"Recorder: #{data['recorder_field_id']}", className="very-small-text"),
                                        ],
                                        width=9,
                                    ),
                                    dbc.Col(
                                        html.Div(
                                            [
                                                html.Div(
                                                    f"{data['confidence'] / 10.0:.1f}",
                                                    className="confidence-score-text"
                                                ),
                                                html.Div(
                                                    className="confidence-score-bar",
                                                    style={
                                                        "--value": data['confidence'],
                                                        "--color": (
                                                            "#B31B1B" if data['confidence'] < 33 else
                                                            "#FF672E" if data['confidence'] < 50 else
                                                            "#FFBC10" if data['confidence'] < 75 else
                                                            "#D9EB6F" if data['confidence'] < 85 else
                                                            "#A3BC09" if data['confidence'] < 90 else
                                                            "#296239"
                                                        )
                                                    }
                                                ),
                                            ],
                                            className="confidence-score-container"
                                        ),
                                        width=3,
                                        className="d-flex align-items-center justify-content-center",
                                    ),
                                ],
                                className="align-items-end",  # Align items to the bottom
                            ),
                            # Hidden audio element for each card with a unique string-based id
                            html.Audio(
                                id={"type": "audio", "index": idx},
                                src=data["url_media"],
                                controls=True,
                                className="d-none",
                            ),
                        ]
                    ),
                ],
                className="mb-4",
                style={"width": "100%", "position": "relative"},  # Set card width to 100%
            ),
            width=12,
            sm=6,
            md=6,
            lg=4,
            xl=3,
        )
        cards.append(card)
        #cards = []

    if not cards:
        placeholder = html.P("Uuups...something went wrong. Please try to reload.", 
                             className="text-muted",
                             style={"text-align": "center", "width": "100%"})
    else:
        placeholder = None #TODO: We want to fully remove the parent div

    return cards, placeholder

# Callback to update the plot for "Most active species"
@app.callback(
    [
        Output("most-active-species", "children"),
        Output("no-active-species-placeholder", "children")
    ],
    [Input("url", "pathname")]
)

def update_most_active_species(pathname):
    # get plots for all species and create a row for each plot
    species_data = dp.get_most_active_species(n=8, min_conf=0.5)
    plot_rows = []

    max_detections = max(data['total_detections'] for data in species_data.values())

    for index, (species, data) in enumerate(species_data.items()):
        plot_sun_moon = True if index == 0 else False
        plot = plots.get_hourly_detections_plot(data['detections'], plot_sun_moon)
        detection_fraction = data['total_detections'] / max_detections * 100
        
        plot_row = dbc.Row(
            [
                dbc.Col(
                    html.Img(src=data['image_url'], className="species-image"),
                    xs=4,
                    sm="auto",
                    md="auto",
                    lg=1,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(f"{data['common_name']} ({data['total_detections']})", className="small-text"),
                                        html.Div(
                                            className="total-detections-bar",
                                            children=[
                                                html.Div(
                                                    className="total-detections-bar-fill",
                                                    style={"width": f"{detection_fraction}%"}
                                                )
                                            ]
                                        )
                                    ],
                                    sm=12,
                                    md=4,
                                    className="species-info"
                                ),
                                dbc.Col(
                                    dcc.Graph(figure=plot, config={"displayModeBar": False, "staticPlot": True}, style={"height": "50px"}),
                                    sm=12,
                                    md=8,
                                    className="species-plot"
                                )
                            ],
                        )
                    ],
                    xs=8,
                    sm=9,
                    md=10,
                    lg=11,
                )
            ],
            className="species-row mb-2",
        )
        
        plot_rows.append(plot_row)
        #plot_rows = []

    # Adjust placeholder
    if not plot_rows:
        placeholder = html.P("Uuups...something went wrong. Please try to reload.", 
                             className="text-muted",
                             style={"text-align": "center", "width": "100%"})
    else:
        placeholder = None #TODO: We want to fully remove the parent div

    # Return the plot wrapped in a Div
    return plot_rows, placeholder

# Client-side callback for playing audio when play icon is clicked
app.clientside_callback(
    """
    function(n_clicks, audio_id) {
        const audioElements = document.querySelectorAll("audio");
        let audioElement = null;
        let iconElement = null;

        for (let i = 0; i < audioElements.length; i++) {
            const elementId = JSON.parse(audioElements[i].id).index;
            if (elementId === audio_id["index"]) {
                audioElement = audioElements[i];
                iconElement = document.getElementById(`play-icon-${elementId}`);
            } else {
                audioElements[i].pause();
                document.getElementById(`play-icon-${elementId}`).className = "bi bi-play-circle-fill";
            }
        }
        
        if (audioElement) {
            if (audioElement.paused) {
                audioElement.currentTime = 0;
                audioElement.play();
                iconElement.className = "bi bi-pause-circle-fill";
            } else {
                audioElement.pause();
                iconElement.className = "bi bi-play-circle-fill";
            }

            return audioElement.src;
        } else {
            throw new Error("Audio element not found: " + audio_id);
        }
    }
    """,
    Output({"type": "audio", "index": MATCH}, "src"),
    [Input({"type": "play-icon", "index": MATCH}, "n_clicks")],
    [State({"type": "audio", "index": MATCH}, "id")],
    prevent_initial_call=True,
)

# Run the app on the local server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
