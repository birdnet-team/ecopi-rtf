from dash import html
import dash_bootstrap_components as dbc

from utils.strings import Strings

def stats_bar(locale):
    
    strings = Strings(locale)
    
    return html.Div(
        dbc.Row(
            [
                dbc.Col(
                    html.Div([html.Div(f"{strings.get('stats_bar_detections_24h')}:", className='stats-bar-headline'), html.H4(id="detections-24h", children="0")]),
                    className="stat-column",
                    width=6,
                    md=3,
                ),
                dbc.Col(
                    html.Div([html.Div(f"{strings.get('stats_bar_species_24h')}:", className='stats-bar-headline'), html.H4(id="species-24h", children="0")]),
                    className="stat-column",
                    width=6,
                    md=3,
                ),
                dbc.Col(
                    html.Div([html.Div(f"{strings.get('stats_bar_detections_total')}:", className='stats-bar-headline'), html.H4(id="total-detections", children="0")]),
                    className="stat-column",
                    width=6,
                    md=3,
                ),
                dbc.Col(
                    html.Div([html.Div(f"{strings.get('stats_bar_audio_total')}:", className='stats-bar-headline'), html.H4(id="total-audio", children="0")]),
                    className="stat-column",
                    width=6,
                    md=3,
                ),
            ],
            className="stat-row-container",
        ),
        className="stat-row",
    )