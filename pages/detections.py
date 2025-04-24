from dash import html, dcc, no_update
import dash_bootstrap_components as dbc

# Import widgets
from widgets.recent_detections import recent_detections
from widgets.popup_player import popup_player

from utils.strings import Strings
import config as cfg

def detections_page_content(locale):
    strings = Strings(locale)

    return html.Div(
        [
            dbc.Container(
                [
                    html.H3(strings.get('det_recent_detections'), className="mt-2 mb-2"),
                    html.P(strings.get('det_description'), className="text-muted"),
                    
                    # Container with default height and spinner
                    html.Div(
                        [
                            dbc.Spinner(
                                color=cfg.PRIMARY_COLOR,
                                type="border",
                                size="lg",
                            ),
                        ],
                        id="detections-loading-container",
                        className="d-flex justify-content-center align-items-center",
                        style={"height": "300px", "width": "100%"}
                    ),
                    
                    # This will be populated by the callback
                    html.Div(id="detections-content", style={"display": "none"}),
                ],
                fluid=True,
            ),
            html.Div(
                html.A(
                    [
                        html.I(className="bi bi-arrow-up-circle"),
                        " " + strings.get('misc_back_to_top'),
                    ],
                    href="#",
                    className="back-to-top-link"
                ),
                id="back-to-top-link",
                className="d-flex justify-content-end p-4",
            ),
            popup_player(),
        ],
        className="main-content"
    )

def register_detections_callbacks(app):
    from dash.dependencies import Input, Output, State
    
    @app.callback(
        [Output("detections-content", "children"),
         Output("detections-content", "style"),
         Output("detections-loading-container", "children"),  # Return empty list to remove spinner
         Output("detections-loading-container", "style")],
        [Input("url", "pathname"), Input("locale-store", "data")]
    )
    def update_detections_content(pathname, locale):
        if not pathname or not pathname.endswith("/detections"):
            # Don't run the callback if we're not on the detections page
            return [], {"display": "none"}, no_update, {"height": "300px", "width": "100%", "display": "flex"}
        
        # Get detection cards
        cards, placeholder, data = recent_detections(num_cards=40, hours=72, locale=locale)
        
        content = [
            dbc.Row(cards),
            data
        ]
        
        # Show content, completely remove spinner
        return content, {"display": "block", "opacity": "1"}, [], {"display": "none", "height": "0"}