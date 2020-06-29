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
    Todo
    '''
)

changelog_text = dcc.Markdown(
    '''
    **v0.1** *2020-03-24*
    * Initial alpha
    '''
)

contact_text = dcc.Markdown(
    '''
    For any questions, please contact Timur Gulyamov (tg2648) or Rose Razaghian (rr222).
    '''
)

notes_button = dbc.Button(
    "Notes",
    id="notes-popup-button",
    color="link",
    outline=False
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
    color="link",
    outline=False
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
    color="link",
    outline=False
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
    className='pt-1',
    width='auto'
)

warning_badge = dbc.Col(
    html.Div(
        [
            html.Span('CONFIDENTIAL'),
            html.Span('—For intended recipients only', className='small font-weight-bold')
        ],
        className='mt-2 text-warning font-weight-bold'
    )
)

title = html.H3(
    'Department Profile Dashboard',
    className='text-info'
)

header = html.Div(
    [
        dbc.Row(
            [
                warning_badge,
                button_group,
                contact_popup,
                changelog_popup,
                notes_popup,
            ],
            justify='between',
            className='mt-2'
        ),
        title
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
