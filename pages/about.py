from dash import html, dcc
import dash_bootstrap_components as dbc
import random
import config as cfg

def about_page_header():
    return html.Div(
        [
            html.Img(src=cfg.SITE_ROOT + f"/assets/ssw_img/ssw_about_header_{random.randint(1, 5)}.jpg", className="species-header-image"),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("SWAMP", className="species-overlay-text"),
                                html.H5("Sapsucker Woods Acoustic Monitoring Project", className="species-overlay-text"),
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

def about_page_content():
    return html.Div(
        [
            about_page_header(),
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
                                className="order-first order-md-last bg-light p-3 mb-3 mt-3 about-sidebar",
                            ),
                            dbc.Col(
                                [
                                    html.H3(id="about-goals", children="Project Goals", className="mb-3"),
                                    html.P([
                                        "The Sapsucker Woods Acoustic Monitoring Project combines technology and community engagement to showcase the power of acoustic monitoring in understanding the natural world. By listening to the sounds of Sapsucker Woods, visitors can explore how advanced tools are used to study wildlife and gain a deeper appreciation for the diversity of birdlife in the area. ",
                                        html.P(),
                                        "The project uses solar-powered recording units equipped with BirdNET software to capture and analyze bird songs and other natural sounds in real-time. These recordings provide a window into the daily rhythms of the woods, revealing which species are active and when. Visitors can see the results of this technology on interactive displays, learning about the species identified and the patterns uncovered. ",
                                        html.P(),
                                        "In addition to its educational role, the project demonstrates the potential of acoustic monitoring for gathering insights into wildlife activity. By continuously collecting and analyzing sound data, it highlights how such methods can help us better understand and connect with the environment. ",
                                        #html.P(),
                                        #"The Sapsucker Woods Acoustic Monitoring Project is as much about fostering curiosity and engagement as it is about research. By bringing the sounds of nature to life, it encourages visitors to explore the rich soundscapes of the woods and discover the stories they tell about the world around us."
                                    ]),
                                    
                                    html.H3(id="about-pam", children="Acoustic Monitoring", className="mb-3"),
                                    html.P([
                                        "Acoustic monitoring is a valuable method for studying ecosystems and biodiversity. By recording and analyzing soundscapes, it allows researchers to detect species presence and behavior without disturbing their habitats. This approach is particularly useful for monitoring elusive or nocturnal species such as birds, bats, and frogs. ",
                                        html.P(),
                                        "One of the main benefits of acoustic monitoring is its ability to provide long-term data. Continuous recording over extended periods helps reveal patterns in species activity, seasonal changes, and responses to environmental factors. This data is crucial for tracking ecosystem health and assessing conservation efforts. ",
                                        html.P(),
                                        "Advances in artificial intelligence have greatly enhanced acoustic monitoring. AI-powered tools, like BirdNET, can automatically identify species from their sounds, significantly reducing the time required for manual analysis. This enables researchers to process large datasets more efficiently and focus on conservation actions. ",
                                        html.P(),
                                        "AI-driven acoustic monitoring has already contributed to conservation successes, such as tracking endangered species, monitoring habitat recovery, and identifying environmental changes. By combining long-term acoustic data with AI, researchers gain valuable insights to support effective conservation strategies."
                                    ]),
                                    
                                    html.H3(id="about-recorder", children="Recording Units", className="mb-3"),
                                    html.Div(
                                        [
                                            html.Img(src=cfg.SITE_ROOT + "/assets/content-img/swamp_recording_unit.jpg", className="recorder-image float-left"),
                                            html.P([
                                                "Our recording units are designed to operate in remote and challenging environments. They are solar-powered, weather-resistant, and connected to the internet, enabling the automatic upload of recorded sounds to a central server for analysis. ",
                                                html.P(),
                                                "Each unit is built around a Raspberry Pi computer equipped with a sound card and a Sleepy Pi module for power management. They run BirdNET software for sound identification and use a SIM card dongle for internet connectivity, making them effective even in isolated locations. ",
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
                                    
                                    html.H3(id="about-ai", children="AI-powered Sound ID", className="mb-3"),
                                    html.P([
                                        "BirdNET is an AI-powered tool that identifies bird species based on their calls and songs. At its core, BirdNET uses a neural network, a type of machine learning model inspired by the structure of the human brain. Neural networks are particularly effective at recognizing patterns in complex datasets, such as sound recordings. ",
                                        html.P(),
                                        "To analyze sounds, BirdNET converts audio recordings into spectrograms, which are visual representations of sound showing frequency, intensity, and time. These spectrograms highlight the unique acoustic patterns of bird calls and songs, much like a fingerprint for each species. The neural network is trained to recognize these patterns using a large dataset of labeled bird sounds. ",
                                        html.P(),
                                        "By applying visual pattern recognition to these spectrograms, BirdNET can detect and identify specific bird species with high accuracy. This approach is efficient, scalable, and well-suited for analyzing large audio datasets, making it an essential tool for biodiversity monitoring. ",
                                        html.P(),
                                        "BirdNET is widely used in conservation efforts to monitor bird populations, study migration patterns, and identify areas of concern for endangered species. Its ability to process recordings automatically and at scale provides researchers with valuable data to support habitat protection and conservation strategies."
                                    ]),
                                    
                                    html.H3(id="about-team", children="Meet the Team", className="mb-4"),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [                                                    
                                                    html.Img(src=cfg.SITE_ROOT + "/assets/content-img/stefan.png", className="team-image"),
                                                    html.H5("Stefan Kahl", className="team-name"),
                                                    html.H6("Project lead and web development")
                                                ],
                                                width=6,
                                                md=4,
                                                className="mb-4 text-center"
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Img(src=cfg.SITE_ROOT + "/assets/content-img/felix.png", className="team-image"),
                                                    html.H5("Felix Günther", className="team-name"),
                                                    html.H6("Backend development")
                                                ],
                                                width=6,
                                                md=4,
                                                className="mb-4 text-center"
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Img(src=cfg.SITE_ROOT + "/assets/content-img/patrick.png", className="team-image"),
                                                    html.H5("Patrick T. Chaopricha", className="team-name"),
                                                    html.H6("Hardware deployment")
                                                ],
                                                width=6,
                                                md=4,
                                                className="mb-4 text-center"
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Img(src=cfg.SITE_ROOT + "/assets/content-img/max.png", className="team-image"),
                                                    html.H5("Max Mauermann", className="team-name"),
                                                    html.H6("Web development")
                                                ],
                                                width=6,
                                                md=4,
                                                className="mb-4 text-center"
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Img(src=cfg.SITE_ROOT + "/assets/content-img/josef.png", className="team-image"),
                                                    html.H5("Josef Haupt", className="team-name"),
                                                    html.H6("AI development")
                                                ],
                                                width=6,
                                                md=4,
                                                className="mb-4 text-center"
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Img(src=cfg.SITE_ROOT + "/assets/content-img/raja.png", className="team-image"),
                                                    html.H5("Raja Seifert", className="team-name"),
                                                    html.H6("Visual design")
                                                ],
                                                width=6,
                                                md=4,
                                                className="mb-4 text-center"
                                            ),
                                        ]
                                    ),
                                    
                                    html.H3(id="about-partners", children="Partners", className="mb-3"),
                                    html.P("The SWAMP project is a collaboration between the Cornell Lab of Ornithology, Chemnitz University of Technology, and OekoFor GbR."),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(src=cfg.SITE_ROOT + "/assets/logo-img/logo_box_lab.png", className="partner-logo"),
                                                sm=4,
                                                xs=6,
                                                className="text-center mb-4"
                                            ),
                                            dbc.Col(
                                                html.Img(src=cfg.SITE_ROOT + "/assets/logo-img/logo_box_tuc.png", className="partner-logo"),
                                                sm=4,
                                                xs=6,
                                                className="text-center mb-4"
                                            ),
                                            dbc.Col(
                                                html.Img(src=cfg.SITE_ROOT + "/assets/logo-img/logo_box_oekofor.png", className="partner-logo"),
                                                sm=4,
                                                xs=12,
                                                className="text-center mb-4"
                                            ),
                                        ],
                                        className="mt-4 mb-4",
                                    ),                                    
                                    
                                    html.H3(id="about-funding", children="Funding", className="mb-3"),
                                    html.P("This project is supported by Jake Holshuh (Cornell class of ’69) and The Arthur Vining Davis Foundations. Our work in the K. Lisa Yang Center for Conservation Bioacoustics is made possible by the generosity of K. Lisa Yang to advance innovative conservation technologies to inspire and inform the conservation of wildlife and habitats."),
                                    html.P("The German Federal Ministry of Education and Research is funding the development of BirdNET through the project \"BirdNET+\" (FKZ 01|S22072). Additionally, the German Federal Ministry of Environment, Nature Conservation and Nuclear Safety is funding the development of BirdNET through the project \"DeepBirdDetect\" (FKZ 67KI31040E)."),
                                    
                                    html.H3(id="about-contact", children="Contact", className="mb-3"),
                                    html.P([
                                        "Dr. Holger Klinck",
                                        html.Br(),
                                        "John W. Fitzpatrick Director of the K. Lisa Yang Center for Conservation Bioacoustics,",
                                        html.Br(),
                                        "Cornell Lab of Ornithology,",
                                        html.Br(),
                                        "Cornell University",
                                        html.Br(),
                                        html.Br(),
                                        "Mailing address:",
                                        html.Br(),
                                        "159 Sapsucker Woods Road",
                                        html.Br(),
                                        "Ithaca, NY 14850, USA",
                                        html.Br(),
                                        html.Br(),
                                        "Email: ",
                                        html.A("ccb-birdnet@cornell.edu", href="mailto:ccb-birdnet@cornell.edu", className="about-link"),
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