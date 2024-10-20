import plotly.graph_objs as go
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
    timezone = pytz.timezone(cfg.TIMEZONE)  # Replace with the appropriate timezone
    
    # Localize the date to the specified timezone
    localized_date = timezone.localize(date)
    
    location = LocationInfo(latitude=lat, longitude=lon)
    s = sun(location.observer, date=localized_date)
    
    # Get the sunrise and sunset times in the localized timezone
    sunrise_hour = s['sunrise'].astimezone(timezone).hour
    sunset_hour = s['sunset'].astimezone(timezone).hour
    
    return sunrise_hour, sunset_hour

def get_hourly_detections_plot(detections, plot_sun_moon=False):
    
    sunrise_hour, sunset_hour = compute_sunrise_sunset(cfg.DEPLOYMENT_LAT, cfg.DEPLOYMENT_LON, date=datetime.now())
    
    # Normalize the detections
    max_val = max(detections)
    normalized_detections = [val / max_val for val in detections]
    
    # Apply log function to the normalized detections
    log_detections = [np.log1p(val) for val in normalized_detections]  # np.log1p is used to avoid log(0)
    
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
            y=0.75,
            text=sun_icon,
            showarrow=False,
            font=dict(size=10, color=sun_color),
            xanchor='center',
            yanchor='middle'
        )
        
        fig.add_annotation(
            x=sunset_hour,
            y=0.75,
            text=moon_icon,
            showarrow=False,
            font=dict(size=10, color=moon_color),
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