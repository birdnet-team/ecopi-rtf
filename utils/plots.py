import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import pytz
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import config as cfg
import numpy as np

def compute_sunrise_sunset(lat, lon, date=None):
    if date is None:
        date = datetime.now()
    
    # Define the timezone for the location
    timezone = pytz.timezone(cfg.TIMEZONE) 
    
    # Localize the date to the specified timezone
    localized_date = timezone.localize(date)
    
    location = LocationInfo(latitude=lat, longitude=lon)
    s = sun(location.observer, date=localized_date)
    
    # Get the sunrise and sunset times in the localized timezone
    sunrise_hour = s['sunrise'].astimezone(timezone).hour
    sunset_hour = s['sunset'].astimezone(timezone).hour
    
    return sunrise_hour, sunset_hour

def utc_to_local(detections):
    
    timezone = pytz.timezone(cfg.TIMEZONE)
    offset = timezone.utcoffset(datetime.now()).total_seconds() / 3600
    offset = int(offset) - 1 
    detections = np.roll(detections, offset)
    
    return detections    

def get_hourly_detections_plot(detections, plot_sun_moon=False):
    
    sunrise_hour, sunset_hour = compute_sunrise_sunset(cfg.DEPLOYMENT_LAT, cfg.DEPLOYMENT_LON, date=datetime.now())
    
    # Normalize the detections
    max_val = max(detections)
    normalized_detections = [val / max_val for val in detections]
    
    # Apply log function to the normalized detections
    log_detections = [np.log1p(val) for val in normalized_detections]  # np.log1p is used to avoid log(0)
    
    # Convert UTC detections to local time
    log_detections = utc_to_local(log_detections)
    
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
        marker_color='#385B75',
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
        sun_color = "white" if log_detections[sunrise_hour] > 0.6 else "#385B75"
        moon_color = "white" if log_detections[sunset_hour] > 0.6 else "#385B75"
        
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

def get_recorder_map(data):
    
    # Convert the nested dictionary to a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Normalize species values to fall between 0 and 1 for color mapping
    species_min = df['species'].min()
    species_max = df['species'].max()
    df['normalized_species'] = (df['species'] - species_min) / (species_max - species_min)
    
    # Calculate the bounding box for the recorder locations
    min_lat = df['lat'].min()
    max_lat = df['lat'].max()
    min_lon = df['lon'].min()
    max_lon = df['lon'].max()
    
    # Calculate the center of the bounding box
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    
    # Define a custom colorscale with three points: low, mid, high
    custom_colorscale_red = [
        [0.00, '#FFA380'],
        [0.33, '#FF672E'],
        [0.66, '#DF1E12'],
        [1.00, '#B31B1B']
    ]
    
    custom_colorscale_blue_to_red = [
        [0.00, '#385B75'],
        [0.25, '#69A0C2'],
        [0.5, '#F5F3E9'],
        [0.75, '#FF672E'],
        [1.00, '#B31B1B']
    ]
    
    # Create a single trace with all points to apply the colorscale consistently
    fig = go.Figure(go.Scattermapbox(
        lat=df['lat'],
        lon=df['lon'],
        mode='markers+text',
        marker=go.scattermapbox.Marker(
            size=np.log1p(df['detections']) * 10, 
            color=df['detections'],
            colorscale=custom_colorscale_blue_to_red,
            #cmin=0,
            #cmax=1,
            showscale=True,
            opacity=0.7
        ),
        text=["#" + str(id) for id in df['id']],   # Display recorder ID above the circle
        textposition="middle center"
    ))
    
    # Update the layout to set the center and zoom level
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",  # Use Mapbox monochrome theme
            center=dict(lat=center_lat, lon=center_lon),
            zoom=14,  # Adjust the zoom level as needed
            accesstoken=cfg.MAPBOX_TOKEN
        ),
        margin={"r":0,"t":0,"l":0,"b":0},  # Remove margins
        showlegend=False  # Hide legend
    )
    
    return fig

