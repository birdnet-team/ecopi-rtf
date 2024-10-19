import plotly.graph_objs as go

def get_hourly_detections_plot(detections):
    max_val = max(detections)
    
    # Create two sets of bars: one for blue and one for gray
    blue_bars = [val if val != 0 else 0 for val in detections]
    gray_bars = [max_val - val if val != 0 else max_val for val in detections]
    
    fig = go.Figure()
    
    # Add blue bars
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=blue_bars,
        marker_color='#69A0C2',
        showlegend=False
    ))
    
    # Add gray bars
    fig.add_trace(go.Bar(
        x=list(range(24)),
        y=gray_bars,
        marker_color='#EAE9E9',
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