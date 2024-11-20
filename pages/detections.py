from dash import html, dcc
import dash_bootstrap_components as dbc

# Import widgets
from widgets.recent_detections import recent_detections
from widgets.popup_player import popup_player

def detections_page_content():
    # Use the recent_detections widget to get the cards, placeholder, and data
    cards, placeholder, data = recent_detections(num_cards=24, hours=24)

    return html.Div(
        [
            dbc.Container(
                [
                    html.H3("Recent detections", className="mt-2 mb-2"),
                    html.P("This list shows some randomly selected species detections from the last 24 hours sorted by confidence score. Click the 'Play' button to listen to the recorded sounds or click the 'Chart' icon to see more stats about this species.", className="text-muted"),
                    dbc.Row(cards),
                    data
                ],
                fluid=True,
            ),
            popup_player(),
        ],
        className="main-content"  # Apply the main-content class for styling
    )