from dash import html, dcc
import dash_bootstrap_components as dbc

from utils import data_processor as dp
from utils import plots
from utils.strings import Strings

import config as cfg

# Mapping of weather descriptions to Bootstrap icons
weather_icons = {
    "clear": "bi bi-sun",
    "clear sky": "bi bi-sun",
    "few clouds": "bi bi-cloud-sun",
    "scattered clouds": "bi bi-cloud",
    "broken clouds": "bi bi-clouds",
    "clouds": "bi bi-clouds",
    "shower rain": "bi bi-cloud-rain",
    "rain": "bi bi-cloud-drizzle",
    "thunderstorm": "bi bi-cloud-lightning",
    "snow": "bi bi-cloud-snow",
    "mist": "bi bi-cloud-fog",
    "fog": "bi bi-cloud-fog",
    "overcast clouds": "bi bi-clouds"
}

# Mapping of weather descriptions to translation keys
weather_translation_keys = {
    "clear": "weather_clear_sky",
    "clear sky": "weather_clear_sky",
    "few clouds": "weather_few_clouds",
    "scattered clouds": "weather_scattered_clouds",
    "broken clouds": "weather_broken_clouds",
    "clouds": "weather_clouds",
    "shower rain": "weather_shower_rain",
    "rain": "weather_rain",
    "thunderstorm": "weather_thunderstorm",
    "snow": "weather_snow",
    "mist": "weather_mist",
    "fog": "weather_fog",
    "overcast clouds": "weather_overcast_clouds"
}

def recording_units(locale):
    strings = Strings(locale)
    try:
        recorder_data = {}
        for recorder_id in cfg.RECORDERS:
            recorder_data[recorder_id] = dp.get_recorder_state(recorder_id, locale)
            
        leaflet_map = plots.get_leaflet_map(recorder_data)
        
        map_component = html.Div(
            [
                leaflet_map
            ],
            className="full-width"  # Ensure the map component takes full width
        )
        
        # Weather data
        weather_data = dp.get_weather_data()    
        weather_icon_class = weather_icons.get(weather_data["weather"].lower(), "bi bi-question-circle")
        weather_translation_key = weather_translation_keys.get(weather_data["weather"].lower(), weather_data["weather"])
        translated_weather = strings.get(weather_translation_key)
        local_time = dp.get_local_time(time_format=cfg.TIME_FORMAT)
        
        weather_row = dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.I(className="bi bi-clock", style={"marginRight": "5px"}),
                            html.Span(local_time)
                        ],
                        className="weather-info d-none d-md-block"
                    ),
                    md=2
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.I(className=weather_icon_class, style={"marginRight": "5px"}),
                            html.Span(translated_weather)
                        ],
                        className="weather-info"
                    ),
                    md=2,
                    sm=3,
                    xs=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.I(className="bi bi-thermometer-half", style={"marginRight": "5px"}),
                            html.Span(f"{weather_data['temperature']} °C")
                        ],
                        className="weather-info"
                    ),
                    md=2,
                    sm=3,
                    xs=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.I(className="bi bi-wind", style={"marginRight": "5px"}),
                            html.Span(f"{weather_data['wind_speed']} m/s")
                        ],
                        className="weather-info"
                    ),
                    md=2,
                    sm=3,
                    xs=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.I(className="bi bi-droplet", style={"marginRight": "5px"}),
                            html.Span(f"{weather_data['humidity']} %")
                        ],
                        className="weather-info"
                    ),
                    md=2,
                    sm=3,
                    xs=6
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.I(className="bi bi-speedometer2", style={"marginRight": "5px"}),
                            html.Span(f"{weather_data['pressure']} hPa")
                        ],
                        className="weather-info d-none d-md-block"
                    ),
                    md=2
                )
            ],
            className="weather-row full-width"
        )
        
        recorder_stats = []
        
        # For each recorder, create a card with the recorder ID, current status, habitat, CPU temp, voltage, and last update
        for recorder_id, data in recorder_data.items():
            status_color = data.get('status_color', '#36824b')
            
            recorder_stats.append(
                dbc.Col(
                    dcc.Link(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Span(
                                            className="status-circle",
                                            style={"backgroundColor": status_color, "borderRadius": "50%", "display": "inline-block", "width": "10px", "height": "10px", "marginRight": "10px"}
                                        ),
                                        f"{strings.get('nav_recorder')} #{recorder_id}",
                                        html.I(className="bi bi-bar-chart-fill", style={"float": "right"})
                                    ],
                                    className="small-text"
                                ),
                                dbc.CardBody(
                                    [
                                        html.H6([html.B(f"{strings.get('widget_units_status')}: "), f"{data['current_status']}"], className="very-small-text"),
                                        html.H6([html.B(f"{strings.get('widget_units_habitat')}: "), f"{strings.get(cfg.RECORDERS[recorder_id]['habitat'])}"], className="very-small-text"),
                                        html.H6([html.B(f"{strings.get('widget_units_cpu_temp')}: "), f"{data['cpu_temp']} °C"], className="very-small-text"),
                                        html.H6([html.B(f"{strings.get('widget_units_battery')}: "), f"{data['battery'] if data['battery'] is not None else 'N/A'} %"], className="very-small-text"),
                                        html.H6([html.B(f"{strings.get('widget_units_last_update')}: "), f"{data['last_update']}"], className="very-small-text")
                                    ]
                                )
                            ],
                            className="mt-3"  # Add top margin to each card
                        ),
                        href=f"{cfg.SITE_ROOT}/recorder/{recorder_id}",
                        style={"textDecoration": "none", "color": "inherit"}
                    ),
                    lg=4,
                    md=4,
                    sm=4,
                    xs=6
                )
            )        
                    
        children = [
            dbc.Row(
                [
                    dbc.Col(map_component, 
                            width=12  # Ensure the map column takes full width
                        )
                ],
                className="full-width"  # Ensure the row takes full width
            ),
            weather_row,
            dbc.Row(
                recorder_stats,
                className="full-width"  # Ensure the row takes full width
            )            
        ]
        
        placeholder = None
    except Exception as e:
        print(e.with_traceback())
        children = []
        placeholder = html.P("Uuups...something went wrong. Please try to reload.", 
                             className="text-muted",
                             style={"text-align": "center", "width": "100%"})
    
    return children, placeholder