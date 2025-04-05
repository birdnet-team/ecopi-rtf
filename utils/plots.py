import pandas as pd

import plotly.graph_objs as go
import plotly.express as px

from dash import html, dcc
import dash_leaflet as dl

import pytz
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime

import config as cfg
import numpy as np
from utils.strings import Strings

def compute_sunrise_sunset(lat, lon, date=None):
    if date is None:
        date = datetime.utcnow()
    
    # Define the timezone for the location
    timezone = pytz.timezone(cfg.TIMEZONE) 
    
    # Localize the date to the specified timezone
    localized_date = timezone.localize(date)
    
    location = LocationInfo(latitude=lat, longitude=lon)
    s = sun(location.observer, date=localized_date)
    
    # Get the sunrise and sunset times in the localized timezone
    sunrise_hour = s['dawn'].astimezone(timezone).hour + 1 if s['dawn'].astimezone(timezone).minute > 30 else s['dawn'].astimezone(timezone).hour
    sunset_hour = s['dusk'].astimezone(timezone).hour + 1 if s['dusk'].astimezone(timezone).minute > 30 else s['dusk'].astimezone(timezone).hour
    
    return sunrise_hour, sunset_hour

def utc_to_local(detections):
    
    timezone = pytz.timezone(cfg.TIMEZONE)
    offset = timezone.utcoffset(datetime.utcnow()).total_seconds() / 3600
    offset = int(offset) - 1 
    detections = np.roll(detections, offset)
    
    return detections    

def get_hourly_detections_plot(detections, plot_sun_moon=False):
    
    sunrise_hour, sunset_hour = compute_sunrise_sunset(cfg.DEPLOYMENT_LAT, cfg.DEPLOYMENT_LON, date=datetime.utcnow())
    
    # Normalize the detections
    max_val = max(detections)
    normalized_detections = [val / max_val for val in detections]
    
    # Apply log function to the normalized detections
    log_detections = [np.log1p(val) for val in normalized_detections]  # np.log1p is used to avoid log(0)
    
    # Convert UTC detections to local time
    #log_detections = utc_to_local(log_detections)
    
    # Create two sets of bars: one for blue and one for gray
    blue_bars = [val if val != 0 else 0 for val in log_detections]
    
    # Create bars for night and day, split into top and bottom halves
    night_bars_top = [0.5 if val == 0 and (hour < sunrise_hour or hour >= sunset_hour) else (1 - val) / 2 if val != 0 and (hour < sunrise_hour or hour >= sunset_hour) else 0 for hour, val in enumerate(log_detections)]
    night_bars_bottom = [0.5 if val == 0 and (hour < sunrise_hour or hour >= sunset_hour) else (1 - val) / 2 if val != 0 and (hour < sunrise_hour or hour >= sunset_hour) else 0 for hour, val in enumerate(log_detections)]
    
    day_bars_top = [0.5 if val == 0 and (sunrise_hour <= hour < sunset_hour) else (1 - val) / 2 if val != 0 and (sunrise_hour <= hour < sunset_hour) else 0 for hour, val in enumerate(log_detections)]
    day_bars_bottom = [0.5 if val == 0 and (sunrise_hour <= hour < sunset_hour) else (1 - val) / 2 if val != 0 and (sunrise_hour <= hour < sunset_hour) else 0 for hour, val in enumerate(log_detections)]
    
    fig = go.Figure()
    
    # Add night bars (bottom)
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=night_bars_bottom,
        marker_color='#D0DDDB',
        showlegend=False
    ))
    
    # Add day bars (bottom)
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=day_bars_bottom,
        marker_color='#F5F3E9',
        showlegend=False
    ))
    
    # Add blue bars
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=blue_bars,
        marker_color=cfg.PLOT_PRIMARY_COLOR,
        showlegend=False
    ))
    
    # Add night bars (top)
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=night_bars_top,
        marker_color='#D0DDDB',
        showlegend=False
    ))
    
    # Add day bars (top)
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=day_bars_top,
        marker_color='#F5F3E9',
        showlegend=False
    ))
    
    if plot_sun_moon:
        # Add sun and moon icons as shapes
        sun_icon = "☼"  # Unicode for sun: ☼, 🌣, ☀
        moon_icon = "☽"  # Unicode for moon
        
        # Determine the color based on the detection value at sunrise and sunset hours
        sun_color = "white" if log_detections[sunrise_hour] > 0.6 else cfg.PLOT_PRIMARY_COLOR
        moon_color = "white" if log_detections[sunset_hour] > 0.6 else cfg.PLOT_PRIMARY_COLOR
        
        fig.add_annotation(
            x=sunrise_hour,
            y=0.85,
            text=sun_icon,
            showarrow=False,
            font=dict(size=14, color=sun_color),
            xanchor='center',
            yanchor='middle'
        )
        
        fig.add_annotation(
            x=sunset_hour,
            y=0.85,
            text=moon_icon,
            showarrow=False,
            font=dict(size=14, color=moon_color),
            xanchor='center',
            yanchor='middle'
        )
        
    fig.update_layout(
        barmode='stack',
        template='plotly_white',
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showline=False),
        margin=dict(l=0, r=0, t=0, b=0),  # Remove margins
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
    )
    
    return fig

def get_weekly_detections_plot(detections, locale='en', log_strength=0.99):
    
    strings = Strings(locale)

    detections_data = detections['detections']
    frequencies_data = detections['frequencies']
    current_week = detections['current_week']

     # Apply adjustable log scale to the detections (only for values > -1)
    log_detections = [np.log1p(val) if val > -1 else -1 for val in detections_data]
    adjusted_detections = [
        (1 - log_strength) * val + log_strength * log_val if val > -1 else -1
        for val, log_val in zip(detections_data, log_detections)
    ]

    # Normalize the adjusted detections
    max_adjusted_detections = max([val for val in adjusted_detections if val != -1], default=1)
    if max_adjusted_detections == 0:
        max_adjusted_detections = 1  # Prevent division by zero
    normalized_adjusted_detections = [
        val / max_adjusted_detections if val != -1 else -1 for val in adjusted_detections
    ]

    # Create the gray bars to stack
    gray_bars = [1 - val if val != -1 else 0 for val in normalized_adjusted_detections]

    fig = go.Figure()

    # Add the light gray bars for no data
    fig.add_trace(go.Bar(
        x=[i for i, val in enumerate(normalized_adjusted_detections, 1) if val == -1],
        y=[1 for val in normalized_adjusted_detections if val == -1],
        marker_color='#F0F0F0',
        name=strings.get('species_wd_no_data'),
    ))

    # Add the primary color bars
    fig.add_trace(go.Bar(
        x=list(range(1, 49)),
        y=[val if val != -1 else 0 for val in normalized_adjusted_detections],
        marker_color=cfg.PLOT_PRIMARY_COLOR,
        name=strings.get('species_wd_weekly_detections'),
    ))

    # Add the gray bars
    fig.add_trace(go.Bar(
        x=list(range(1, 49)),
        y=gray_bars,
        marker_color='#D0DDDB',
        name='Remaining',
        showlegend=False
    ))

    # Add the frequencies line plot
    fig.add_trace(go.Scatter(
        x=list(range(1, 49)),
        y=frequencies_data,
        mode='lines',
        line=dict(dash='dash', color='black'),
        name=strings.get('species_wd_frequency'),
    ))

    # Calculate the offset for the current weekday (UTC)
    current_weekday = datetime.utcnow().weekday()  # Monday is 0 and Sunday is 6
    weekday_offset = (current_weekday - 3) / 7

    # Add the vertical line for the current week
    fig.add_shape(
        type="line",
        x0=current_week + weekday_offset,
        y0=0,
        x1=current_week + weekday_offset,
        y1=1,
        line=dict(color="#DF1E12", width=2),
    )

    # Add the "Today" label without the arrow
    fig.add_annotation(
        x=current_week + weekday_offset,
        y=1.1,
        text=strings.get('species_wd_today'),
        showarrow=False,
        font=dict(size=10, color="#DF1E12"),
        align="center"
    )

    fig.update_layout(
        barmode='stack',
        template='plotly_white',
        xaxis=dict(
            tickvals=[1] + list(range(4, 49, 4)),  # Ensure 1, 4, 8, ..., 48 are labeled
            ticktext=[1] + [str(i) for i in range(4, 49, 4)],
            showgrid=False
        ),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, showline=False),
        margin=dict(l=0, r=0, t=0, b=20),  # Adjust bottom margin to move x-axis label up
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot area
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )

    return fig

def get_leaflet_tile_url(tile_url):
    return f"{cfg.SITE_ROOT}/tile?url={tile_url}"

def get_leaflet_map(data, height='500px'):
    # Convert the nested dictionary to a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Add recorder IDs to the DataFrame
    df['id'] = df.index
    
    # Add coordinates from cfg.RECORDERS to the DataFrame
    df['lat'] = df['id'].apply(lambda x: cfg.RECORDERS[x]['lat'])
    df['lon'] = df['id'].apply(lambda x: cfg.RECORDERS[x]['lon'])
    
    # Normalize and apply log scale to detections
    if 'detections' not in df.columns:
        df['normalized_detections'] = 2  # Default value if no detections are available
    else:    
        # np.log1p is used to avoid log(0)
        # Normalize detections to fall between 1 and 6 for radius mapping
        detections_min = df['detections'].min()
        detections_max = df['detections'].max()
        df['normalized_detections'] = 0.5 + (np.log1p(df['detections']) - np.log1p(detections_min)) * 4.5 / (np.log1p(detections_max) - np.log1p(detections_min))
    
    # Calculate the bounding box for the recorder locations
    min_lat = df['lat'].min()
    max_lat = df['lat'].max()
    min_lon = df['lon'].min()
    max_lon = df['lon'].max()
    
    # Calculate the center of the bounding box
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    
    # Create a list of CircleMarkers for each recorder
    markers = [
        dl.CircleMarker(
            center=[row['lat'], row['lon']],
            radius=row['normalized_detections'] * 6,  # Adjust the multiplier as needed
            color='#69A0C2' if 'detections' in row else row['status_color'],
            fill=True,
            fillOpacity=0.7,
            children=[
                dl.Tooltip(
                    dcc.Link(
                        html.Div([                        
                            html.B(f"#{row['id']} ({row['detections']})") if 'detections' in row else html.B(f"#{row['id']}"),
                        ]),
                        href=f"{cfg.SITE_ROOT}/recorder/{row['id']}",
                        style={'color': 'black'}
                    ),
                    permanent=True, 
                    interactive=True,
                    direction=cfg.RECORDERS[row['id']]['tooltip'] if 'tooltip' in cfg.RECORDERS[row['id']] else 'right'
                )
            ]
        ) for idx, row in df.iterrows()
    ]
    
    # Create the Leaflet map
    leaflet_map = dl.Map(
        id='species-site-map',
        children=[
            dl.TileLayer(url=get_leaflet_tile_url("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")),
            dl.LayerGroup(markers)
        ],
        center=[center_lat, center_lon],
        #zoom=cfg.MAP_ZOOM_LEVEL,  # Initial zoom level
        style={'width': '100%', 'height': height},
        scrollWheelZoom=False,  # Disable scroll wheel zoom
        touchZoom=True,  # Enable touch zoom
        zoomControl=True,  # Enable zoom controls
        bounds=[[min_lat, min_lon], [max_lat, max_lon]]  # Set bounds to fit all markers
    )
    
    return leaflet_map