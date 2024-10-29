from dash import html, dcc

def popup_player():
    return html.Div(
        [
            html.Div(id="popup-backdrop", className="d-none"),
            html.Div(id='popup', className='d-flex flex-column justify-content-between', children=[
                html.Div(id='popup-content'),
                html.Div(id='popup-footer', className="d-flex justify-content-center",children=[
                html.Button('Close', id='close-popup-button')]),
            ])
        ]
    )