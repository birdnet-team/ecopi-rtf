from dash import html, dcc
import dash_bootstrap_components as dbc

# Import widgets
from widgets.recent_detections import recent_detections
from widgets.popup_player import popup_player

from utils.strings import Strings

def detections_page_content(locale):
    # Use the recent_detections widget to get the cards, placeholder, and data
    cards, placeholder, data = recent_detections(num_cards=24, hours=72, locale=locale)

    strings = Strings(locale)

    return html.Div(
        [
            dbc.Container(
                [
                    html.H3(strings.get('det_recent_detections'), className="mt-2 mb-2"),
                    html.P(strings.get('det_description'), className="text-muted"),
                    dbc.Row(cards),
                    data
                ],
                fluid=True,
            ),
            popup_player(),
        ],
        className="main-content"  # Apply the main-content class for styling
    )