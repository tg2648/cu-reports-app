"""
Layout: Top row
Contains the title, changelog, and notes.

TODO: The changelog might get too long after some time
"""

# Third party imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


notes_text = dcc.Markdown(
    '''
    The applicant data comes from RAPS. The demographics information in RAPS consists of: gender, ethnicity, and race.

    Ethnicity is determined by whether or not someone identifies as Hispanic or Latino.

    If an applicant self-identifies as multiple races, the least represented race is selected based on the order below (based on the Provost's Office guidelines):

    * American Indian or Alaska Native
    * Native Hawaiian or Other Pacific Islander
    * Black or African American
    * Asian
    * White

    *N/A* means either a non-response or an explicit "I prefer not to disclose."

    *URM* includes anyone who has self-identified as at least one of the following: Hispanic or Latino, American Indian or Alaska Native, Black or African American, or Native Hawaiian or Other Pacific Islander.

    To maintain confidentiality of applicant information, demographics are only displayed if the applicant pool meets certain requirements:

    * If no chart is displayed, there are fewer than three applicants.
    * If no table is displayed, there are fewer than five women and five men applicants.

    Availability data comes from the Survey of Earned Doctorates (SED), which only includes US citizens and Permanent Residents who received PhDs from US institutions in years and subfields indicated. The data was aggregated into several groups representing comparison data for non-tenured/tenure-track and tenured faculty positions in each department. For example, "Tenured availability 1993-2007" represents people who received their PhDs between 1993 and 2007 who are more likely to apply for a tenured position. The availability data provided here is intended as a general reference for the availability of potential women and minority US domestic doctoral degree holders by department. Please note that for each search, the subfields for the SED data may be wider than the specific search parameters.

    Dashes in the *All Applicants* table indicate zeros.

    RAPS data will be updated weekly.
    '''
)

changelog_text = html.Div(
    [
        html.B('v1.1'),
        html.I(' 2019-10-30'),
        html.Ul(
            [
                html.Li('The chart and the table will not be displayed if the applicant pool does not meet certain requirements. See notes for more details.'),
            ]
        ),

        html.B('v1.0.1'),
        html.I(' 2019-10-29'),
        html.Ul(
            [
                html.Li('Added a confidentiality label.'),
            ]
        ),

        html.B('v1.0'),
        html.I(' 2019-10-24'),
        html.Ul(
            [
                html.Li(
                    [
                        'Initial release! ',
                        html.Img(src='https://cu-dash-static.s3.us-east-2.amazonaws.com/img/party.png', height='25px')
                    ]
                ),
                html.Li('Expanded notes on availability data.'),
            ]
        ),

        html.B('v0.2'),
        html.I(' 2019-10-16'),
        html.Ul(
            [
                html.Li('Second phase pilot release.'),
                html.Li('Added a "Contact us" button.'),
            ]
        ),

        html.B('v0.1'),
        html.I(' 2019-10-09'),
        html.Ul(
            [
                html.Li('First phase pilot release.')
            ]
        ),

    ]
)

contact_text = dcc.Markdown(
    '''
    For any questions, please contact Timur Gulyamov (tg2648) or Rose Razaghian (rr222).
    '''
)

notes_button = dbc.Button(
    "Notes",
    id="notes-popup-button",
    color="info",
    outline=True
)

notes_popup = dbc.Modal(
    [
        dbc.ModalHeader(html.Span('Notes', className='text-info')),
        dbc.ModalBody(notes_text),
        dbc.ModalFooter(dbc.Button("Close", id="close-notes", className="ml-auto", size='sm')),
    ],
    id="notes-popup",
    size="lg",
    scrollable=True
)

changelog_button = dbc.Button(
    "Changelog",
    id="changelog-popup-button",
    color="info",
    outline=True
)

changelog_popup = dbc.Modal(
    [
        dbc.ModalHeader(html.Span('Changelog', className='text-info')),
        dbc.ModalBody(changelog_text),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-changelog", className="ml-auto", size='sm')
        ),
    ],
    id="changelog-popup",
    scrollable=True
)

contact_button = dbc.Button(
    "Contact us",
    id="contact-popup-button",
    color="info",
    outline=True
)

contact_popup = dbc.Modal(
    [
        dbc.ModalHeader(html.Span('Contact us', className='text-info')),
        dbc.ModalBody(contact_text),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-contact", className="ml-auto", size='sm')
        ),
    ],
    id="contact-popup"
)

button_group = dbc.Col(
    dbc.ButtonGroup(
        [
            contact_button,
            changelog_button,
            notes_button
        ],
        size='sm'
    ),
    width='auto'
)

warning_badge = html.Div(
    [
        html.Span('CONFIDENTIAL'),
        html.Span('—For intended recipients only', className='small font-weight-bold')
    ],
    className='mt-4 text-warning font-weight-bold'
)

title = dbc.Col(
    [
        html.H2(
            'Search Committee Dashboard',
            className='text-info'
        ),
    ]
)

header = html.Div(
    [
        warning_badge,
        dbc.Row(
            [
                title,
                button_group,
                contact_popup,
                changelog_popup,
                notes_popup,
            ],
            justify='between',
            className='mt-1'
        ),
    ]
)

# changelog_popup = dbc.Toast(
#             changelog_text,
#             id="=changelog-popup",
#             header="Changelog",
#             is_open=False,
#             dismissable=True,
#             # top: 66 positions the toast below the navbar
#             style={"position": "fixed", "top": 66, "right": 10, "width": 350},
#         )

# notes_popup = dbc.Toast(
#             notes_text,
#             id="=notes-popup",
#             header="Notes",
#             is_open=False,
#             dismissable=True,
#             # top: 66 positions the toast below the navbar
#             style={"position": "fixed", "top": 66, "right": 10, "width": 350},
#         )
