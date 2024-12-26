from dash import html, dcc
import dash_bootstrap_components as dbc
import random
import config as cfg

def about_page_header(locale):
    return html.Div(
        [
            html.Img(src=cfg.SITE_ROOT + f"/assets/header_img/{random.choice(cfg.ABOUT_HEADER_IMG_LIST)}", className="species-header-image"),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(cfg.PROJECT_ACRONYM, className="species-overlay-text"),
                                html.H5(cfg.PROJECT_MAIN_TITLE, className="species-overlay-text"),
                            ],
                            width=12,
                        ),
                    ],
                    className="species-overlay-row"
                ),
                className="species-overlay",
            ),
        ],
        className="species-header",
    )

def about_page_content(locale):
    
    team_members = []
    for member in cfg.TEAM_MEMBERS:
        team_members.append(
            dbc.Col(
                [
                    html.Img(src=cfg.SITE_ROOT + f"/assets/content_img/{member['img']}", className="team-image"),
                    html.H6(member["name"], className="team-name"),
                    html.P(member["role"])
                ],
                width=6,
                md=4,
                className="mb-4 text-center"
            )
        )
    
    return html.Div(
        [
            about_page_header(locale),
            dbc.Container(
                [
                    # Two columns
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H6(html.A("Project goals", href="#about-goals", className="about-link"), className="mb-3"),
                                    html.H6(html.A("Acoustic monitoring", href="#about-pam", className="about-link"), className="mb-3"),
                                    html.H6(html.A("Recording units", href="#about-recorder", className="about-link"), className="mb-3"),
                                    html.H6(html.A("AI-powered sound ID", href="#about-ai", className="about-link"), className="mb-3"),
                                    html.H6(html.A("Meet the team", href="#about-team", className="about-link"), className="mb-3"),
                                    html.H6(html.A("Partners", href="#about-partners", className="about-link"), className="mb-3"),
                                    html.H6(html.A("Funding", href="#about-funding", className="about-link"), className="mb-3"),
                                    html.H6(html.A("Contact", href="#about-contact", className="about-link"), className="mb-3"),
                                ],
                                width=12,
                                md=3,
                                className="order-first order-md-last bg-light p-3 mb-3 about-sidebar",
                            ),
                            dbc.Col(
                                [
                                    html.H4(id="about-goals", children="Project Goals", className="mb-3"),
                                    html.P([
                                        cfg.PROJECT_GOAL,
                                        html.P(),
                                        "The project uses solar-powered recording units equipped with BirdNET software to capture and analyze bird songs and other natural sounds in real-time. These recordings provide a window into the daily rhythms of the woods, revealing which species are active and when.",
                                        html.P(),
                                        html.B("Note: No voice is recorded. Our recording devices use an AI model that recognizes human conversations and discards them.", className="bold-text"),
                                    ]),
                                    
                                    html.H4(id="about-pam", children="Acoustic Monitoring", className="mb-3"),
                                    html.P([
                                        "Acoustic monitoring is a valuable method for studying ecosystems and biodiversity. By recording and analyzing soundscapes, it allows researchers to detect species presence and behavior without disturbing their habitats.",
                                        html.P(),
                                        "One of the main benefits of acoustic monitoring is its ability to provide long-term data. Continuous recording over extended periods helps reveal patterns in species activity, seasonal changes, and responses to environmental factors. This data is crucial for tracking ecosystem health and assessing conservation efforts. ",
                                        html.P(),
                                        "AI-driven acoustic monitoring has already contributed to conservation successes, such as tracking endangered species, monitoring habitat recovery, and identifying environmental changes. By combining long-term acoustic data with AI, researchers gain valuable insights to support effective conservation strategies."
                                    ]),
                                    
                                    html.H4(id="about-recorder", children="Recording Units", className="mb-3"),
                                    html.Div(
                                        [                                            
                                            html.P([
                                                "Our recording units are designed to operate in remote and challenging environments. They are solar-powered, weather-resistant, and connected to the internet, enabling the automatic upload of recorded sounds to a central server. ",
                                                html.P(),
                                                "Each unit is built around a Raspberry Pi computer equipped with a sound card and a Sleepy Pi module for power management. They run BirdNET software for sound identification and use a SIM card dongle for internet connectivity, making them effective even in isolated locations. ",
                                                html.P(),
                                                html.Img(src=cfg.SITE_ROOT + "/assets/content_img/swamp_recording_unit.jpg", className="full-width"),
                                                html.P(),
                                                "Powered by a battery and a 10W solar panel, the units follow an hourly recording schedule to conserve energy. They record for a few minutes each hour, focusing on capturing activity during the most vocal periods of the day. ",
                                                html.P(),
                                                "These units are manufactured by OekoFor GbR in Germany, a company that specializes in ecological monitoring equipment. They are used in various projects worldwide, contributing to real-time monitoring systems that support research and conservation. ",
                                                html.P(),
                                                "By providing reliable data on soundscapes and species activity, the units play an important role in understanding and preserving ecosystems."
                                            ]),

                                        ],
                                        className="clearfix"
                                    ),
                                    
                                    html.H4(id="about-ai", children="AI-powered Sound ID", className="mb-3"),
                                    html.P([
                                        "BirdNET is an AI-powered tool that identifies bird species based on their calls and songs. At its core, BirdNET uses a neural network, a type of machine learning model inspired by the structure of the human brain. Neural networks are particularly effective at recognizing patterns in complex datasets, such as sound recordings. ",
                                        html.P(),
                                        "To analyze sounds, BirdNET converts audio recordings into spectrograms, which are visual representations of sound showing frequency, amplitude, and time. These spectrograms highlight the unique acoustic patterns of bird calls and songs, much like a fingerprint for each species. The neural network is trained to recognize these patterns using a large dataset of labeled bird sounds. ",
                                        html.P(),
                                        html.Img(src=cfg.SITE_ROOT + "/assets/content_img/birdnet_how_it_works.jpg", className="full-width p-4"),
                                        html.P(),
                                        "BirdNET is widely used in conservation efforts to monitor bird populations, study migration patterns, and identify areas of concern for endangered species. Its ability to process recordings automatically and at scale provides researchers with valuable data to support habitat protection and conservation strategies."
                                    ]),
                                    
                                    html.H4(id="about-team", children="Meet the Team", className="mb-4"),
                                    dbc.Row(team_members),                           
                                    html.H4(id="about-partners", children="Partners", className="mb-3"),
                                    html.P("This project is a collaboration between the Cornell Lab of Ornithology, Chemnitz University of Technology, and OekoFor GbR."),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(src=cfg.SITE_ROOT + "/assets/logo_img/logo_box_lab.png", className="partner-logo"),
                                                sm=4,
                                                xs=6,
                                                className="text-center mb-4"
                                            ),
                                            dbc.Col(
                                                html.Img(src=cfg.SITE_ROOT + "/assets/logo_img/logo_box_tuc.png", className="partner-logo"),
                                                sm=4,
                                                xs=6,
                                                className="text-center mb-4"
                                            ),
                                            dbc.Col(
                                                html.Img(src=cfg.SITE_ROOT + "/assets/logo_img/logo_box_oekofor.png", className="partner-logo"),
                                                sm=4,
                                                xs=12,
                                                className="text-center mb-4"
                                            ),
                                        ],
                                        className="mt-4 mb-4",
                                    ),                                    
                                    
                                    html.H4(id="about-funding", children="Funding", className="mb-3"),
                                    html.P("This project is supported by Jake Holshuh (Cornell class of ’69) and The Arthur Vining Davis Foundations. Our work in the K. Lisa Yang Center for Conservation Bioacoustics is made possible by the generosity of K. Lisa Yang to advance innovative conservation technologies to inspire and inform the conservation of wildlife and habitats."),
                                    html.P("The development of BirdNET is supported by the German Federal Ministry of Education and Research through the project “BirdNET+” (FKZ 01|S22072). The German Federal Ministry for the Environment, Nature Conservation and Nuclear Safety contributes through the “DeepBirdDetect” project (FKZ 67KI31040E). In addition, the Deutsche Bundesstiftung Umwelt supports BirdNET through the project “RangerSound” (project 39263/01)."),
                                    
                                    html.H4(id="about-contact", children="Contact", className="mb-3"),
                                    html.P([
                                        "Dr. Stefan Kahl",
                                        html.Br(),
                                        "K. Lisa Yang Center for Conservation Bioacoustics,",
                                        html.Br(),
                                        "Cornell Lab of Ornithology, Cornell University",
                                        html.Br(),
                                        html.Br(),
                                        "Mailing address (USA):",
                                        html.Br(),
                                        "159 Sapsucker Woods Road",
                                        html.Br(),
                                        "Ithaca, NY 14850, USA",
                                        html.Br(),
                                        html.Br(),
                                        "Mailing address (Germany):",
                                        html.Br(),
                                        "Straße der Nationen 62",
                                        html.Br(),
                                        "DE-09111, Chemnitz, Germany",
                                        html.Br(),
                                        html.Br(),
                                        "Email: ",
                                        html.A("stefan.kahl@cornell.edu", href="mailto:stefan.kahl@cornell.edu", className="about-link"),
                                    ]),
                                ],
                                width=12,
                                md=9,
                                className="order-last order-md-first",
                            ),
                        ],
                        className="species-content-row",
                    ),
                ],
                fluid=True,
                className="main-content",
            ),
        ]
    )