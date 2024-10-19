import plotly.graph_objs as go
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
import config as cfg

def compute_sunrise_sunset(lat, lon, date=None):
    if date is None:
        date = datetime.now()
    location = LocationInfo(latitude=lat, longitude=lon)
    s = sun(location.observer, date=date)
    sunrise_hour = s['sunrise'].hour
    sunset_hour = s['sunset'].hour
    
    return sunrise_hour + 1, sunset_hour + 1

def get_hourly_detections_plot(detections):
    
    sunrise_hour, sunset_hour = compute_sunrise_sunset(cfg.DEPLOYMENT_LAT, cfg.DEPLOYMENT_LON, date=datetime.now())
    max_val = max(detections)
    
    # Create two sets of bars: one for blue and one for gray
    blue_bars = [val if val != 0 else 0 for val in detections]
    
    # Create bars for night and day
    night_bars = [max_val if val == 0 and (hour < sunrise_hour or hour >= sunset_hour) else max_val - val if val != 0 and (hour < sunrise_hour or hour >= sunset_hour) else 0 for hour, val in enumerate(detections)]
    day_bars = [max_val if val == 0 and (sunrise_hour <= hour < sunset_hour) else max_val - val if val != 0 and (sunrise_hour <= hour < sunset_hour) else 0 for hour, val in enumerate(detections)]
    
    fig = go.Figure()
    
    # Add blue bars
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=blue_bars,
        marker_color='#457999',
        showlegend=False
    ))
    
    # Add night bars
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=night_bars,
        marker_color='#AAC4C4',
        showlegend=False
    ))
    
    # Add day bars
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=day_bars,
        marker_color='#F5F3E9',
        showlegend=False
    ))
    
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