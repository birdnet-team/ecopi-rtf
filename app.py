import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the Dash app
app.layout = html.Div([
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
                            dbc.NavItem(dbc.NavLink("Dashboard", href="#")),
                            dbc.DropdownMenu(
                                label="Recorders",
                                children=[
                                    dbc.DropdownMenuItem("Recorder 1", href="#"),
                                    dbc.DropdownMenuItem("Recorder 2", href="#"),
                                    dbc.DropdownMenuItem("Recorder 3", href="#"),
                                    dbc.DropdownMenuItem("Recorder 4", href="#"),
                                    dbc.DropdownMenuItem("Recorder 5", href="#"),
                                    dbc.DropdownMenuItem("Recorder 6", href="#"),
                                    dbc.DropdownMenuItem("Recorder 7", href="#"),
                                ],
                                nav=True,
                            ),
                            dbc.NavItem(dbc.NavLink("About", href="#")),
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
        className="mb-0",  # Add bottom margin
    ),

    # Full-width Header Image (below the navbar)
    html.Div(
        html.Img(src='/assets/swamp_header.jpg', className="header-graphic"),
        style={'padding-bottom': '40px'}  # Add padding between the header and content
    ),

    # Main Content Section
    dbc.Container(
        [
            html.H1("Sapsucker Woods Acoustic Monitoring Project", className="mt-0"),
            html.P("This is where the content of your page goes."),
            html.P("You can add graphs, charts, or any other interactive components here."),
            # Add more components or visualizations as needed
        ],
        fluid=True,  # Make the content container fluid (adjusts to screen size)
        style={'padding-left': '20px', 'padding-right': '20px'}  # Add padding to the sides
    ),

    # Footer Section
    html.Footer(
        [
            # Top Logo
            html.Div(
                html.Img(src='/assets/cornell-lab-logo-full-white.png', className="footer-logo"),
                style={'textAlign': 'center', 'margin-bottom': '20px'}
            ),
            
            # Two-column content
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("K. Lisa Yang Center for Conservation Bioacoustics"),
                                    html.P("We collect and interpret sounds in nature by developing, applying, and sharing innovative conservation technologies across relevant scales to inform and advance the conservation of wildlife and habitats.", style={'textAlign': 'justify'}),
                                    html.H5("SWAMP"),
                                    html.P("The Sapsucker Woods Acoustic Monitoring Project (SWAMP) is an effort to study the biodiversity of birds in Sapsucker Woods through acoustic monitoring and advances AI models for bird sound ID.", style={'textAlign': 'justify'}),
                                ]
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("BirdNET - Bird Sound Identification"),
                                    html.P("This project is supported by Jake Holshuh (Cornell class of '69) and The Arthur Vining Davis Foundations. Our work in the K. Lisa Yang Center for Conservation Bioacoustics is made possible by the generosity of K. Lisa Yang to advance innovative conservation technologies to inspire and inform the conservation of wildlife and habitats.", style={'textAlign': 'justify'}),
                                    html.P("The German Federal Ministry of Education and Research is funding the development of BirdNET through the project 'BirdNET+' (FKZ 01|S22072). Additionally, the German Federal Ministry of Environment, Nature Conservation and Nuclear Safety is funding the development of BirdNET through the project 'DeepBirdDetect' (FKZ 67KI31040E).", style={'textAlign': 'justify'}),
                                ]
                            ),
                            width=6,
                        ),
                    ]
                ),
                fluid=True,
                style={'padding': '20px'}
            ),
            
            # Bottom Logo
            html.Div(
                html.Img(src='/assets/cornell-logo-white.png', className="footer-logo"),
                style={'textAlign': 'center', 'margin-top': '20px'}
            ),
            
            # Copyright text
            html.P("© 2024 Cornell University", style={'margin-top': 20, 'textAlign': 'center', 'fontSize': '10px'}),
        ],
        style={'backgroundColor': '#2e261f', 'padding': '20px', 'color': 'white'}
    )
])

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

# Run the app on the local server
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)