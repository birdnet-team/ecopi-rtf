import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os

import config as cfg

def privacy_page_content(locale):
    
    # Construct the file path for the privacy policy markdown file
    file_path = f"assets/text/privacy_policy_{locale}.md"
    
    # Check if the file exists, if not, fall back to the English version
    if not os.path.exists(file_path):
        file_path = f"assets/text/privacy_policy_en.md"
    
    # Read the privacy policy markdown file
    with open(file_path, 'r') as file:
        privacy_policy_md = file.read()

    return html.Div(
        [
            dcc.Markdown(privacy_policy_md, className="markdown-content", link_target="_blank"),
        ],
        className="main-content"
    )