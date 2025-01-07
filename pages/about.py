from dash import html, dcc
import dash_bootstrap_components as dbc
import random

from utils.strings import Strings

import config as cfg

def about_page_header(locale):
    strings = Strings(locale, project=cfg.PROJECT_ID)
    return html.Div(
        [
            html.Img(src=cfg.SITE_ROOT + f"/assets/header_img/{random.choice(cfg.ABOUT_HEADER_IMG_LIST)}", className="species-header-image"),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(cfg.PROJECT_ACRONYM, className="species-overlay-text"),
                                html.H5(strings.get('project_main_title'), className="species-overlay-text"),
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
    strings = Strings(locale, project=cfg.PROJECT_ID)
    team_members = []
    for member in cfg.TEAM_MEMBERS:
        team_members.append(
            dbc.Col(
                [
                    html.Img(src=cfg.SITE_ROOT + f"/assets/content_img/{member['img']}", className="team-image"),
                    html.H6(member["name"], className="team-name"),
                    html.P(strings.get(member["role"]))
                ],
                width=6,
                md=4,
                className="mb-4 text-center"
            )
        )
        
    partner_logos = []
    for logo in cfg.PARTNER_LOGOS:
        partner_logos.append(
            dbc.Col(
                html.Img(src=cfg.SITE_ROOT + f"/assets/logo_img/{logo}", className="partner-logo"),
                sm=4,
                xs=6,
                className="text-center mb-4 p-4"
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
                                    html.H6(html.A(strings.get('about_headline_project_goals'), href="#about-goals", className="about-link"), className="mb-3"),
                                    html.H6(html.A(strings.get('about_headline_acoustic_monitoring'), href="#about-pam", className="about-link"), className="mb-3"),
                                    html.H6(html.A(strings.get('about_headline_recording_units'), href="#about-recorder", className="about-link"), className="mb-3"),
                                    html.H6(html.A(strings.get('about_headline_ai_sound_id'), href="#about-ai", className="about-link"), className="mb-3"),
                                    html.H6(html.A(strings.get('about_headline_meet_the_team'), href="#about-team", className="about-link"), className="mb-3"),
                                    html.H6(html.A(strings.get('about_headline_partners'), href="#about-partners", className="about-link"), className="mb-3"),
                                    html.H6(html.A(strings.get('about_headline_funding'), href="#about-funding", className="about-link"), className="mb-3"),
                                    html.H6(html.A(strings.get('about_headline_contact'), href="#about-contact", className="about-link"), className="mb-3"),
                                ],
                                width=12,
                                md=3,
                                className="order-first order-md-last bg-light p-3 mb-3 about-sidebar",
                            ),
                            dbc.Col(
                                [
                                    html.H4(id="about-goals", children=strings.get('about_headline_project_goals'), className="mb-3"),
                                    html.P([
                                        strings.get('project_goal'),
                                        html.P(),
                                        strings.get('about_project_goal_2'),
                                        html.P(),
                                        html.B(strings.get('about_no_voice_note'), className="bold-text"),
                                    ]),
                                    
                                    html.H4(id="about-pam", children=strings.get('about_headline_acoustic_monitoring'), className="mb-3"),
                                    html.P([
                                        strings.get('about_acoustic_monitoring_1'),
                                        html.P(),
                                        strings.get('about_acoustic_monitoring_2'),
                                        html.P(),
                                        strings.get('about_acoustic_monitoring_3'),
                                    ]),

                                    html.H4(id="about-recorder", children=strings.get('about_headline_recording_units'), className="mb-3"),
                                    html.Div(
                                        [
                                            html.P([
                                                strings.get('about_recording_units_1'),
                                                html.P(),
                                                strings.get('about_recording_units_2'),
                                                html.P(),
                                                html.Img(src=cfg.SITE_ROOT + "/assets/content_img/swamp_recording_unit.jpg", className="full-width"),
                                                html.P(),
                                                strings.get('about_recording_units_3'),
                                                html.P(),
                                                strings.get('about_recording_units_4'),
                                                html.P(),
                                                strings.get('about_recording_units_5'),
                                            ]),
                                        ],
                                        className="clearfix"
                                    ),

                                    html.H4(id="about-ai", children=strings.get('about_headline_ai_sound_id'), className="mb-3"),
                                    html.P([
                                        strings.get('about_ai_sound_id_1'),
                                        html.P(),
                                        strings.get('about_ai_sound_id_2'),
                                        html.P(),
                                        html.Img(src=cfg.SITE_ROOT + "/assets/content_img/birdnet_how_it_works.jpg", className="full-width p-4"),
                                        html.P(),
                                        strings.get('about_ai_sound_id_3'),
                                    ]),
                                    
                                    html.H4(id="about-team", children=strings.get('about_headline_meet_the_team'), className="mb-4"),
                                    dbc.Row(team_members),                           
                                    html.H4(id="about-partners", children=strings.get('about_headline_partners'), className="mb-3"),
                                    html.P(strings.get(cfg.PARTNER_STATEMENT)),
                                    dbc.Row(
                                        partner_logos,
                                        className="mt-4 mb-4",
                                    ),                                    
                                    
                                    html.H4(id="about-funding", children=strings.get('about_headline_funding'), className="mb-3"),
                                    html.P(strings.get('about_funding_1')),
                                    html.P(strings.get('about_funding_2')),
                                    
                                    html.H4(id="about-contact", children=strings.get('about_headline_contact'), className="mb-3"),
                                    html.P([
                                        "Dr. Stefan Kahl",
                                        html.Br(),
                                        "K. Lisa Yang Center for Conservation Bioacoustics,",
                                        html.Br(),
                                        "Cornell Lab of Ornithology, Cornell University",
                                        html.Br(),
                                        html.Br(),
                                        f"{strings.get('about_mailing_us')}:",
                                        html.Br(),
                                        "159 Sapsucker Woods Road",
                                        html.Br(),
                                        "Ithaca, NY 14850, USA",
                                        html.Br(),
                                        html.Br(),
                                        f"{strings.get('about_mailing_de')}:",
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
            html.Div(
                html.A(
                    [
                        html.I(className="bi bi-arrow-up-circle"),
                        " " + strings.get('misc_back_to_top'),
                    ],
                    href="#",
                    className="back-to-top-link"
                ),
                id="back-to-top-link",  # Assign an ID to the "Back to top" link
                className="d-flex justify-content-end p-4",
            ),
        ]
    )