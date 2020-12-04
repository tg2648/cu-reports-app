"""
Layout: Top row
"""

# Third party imports
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


contact_text = dcc.Markdown(
    '''
    For any questions, please contact Timur Gulyamov (<tg2648@columbia.edu>) or Rose Razaghian (<rr222@columbia.edu>).
    '''
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
        ],
        size='sm'
    ),
    width='auto'
)

title = dbc.Col(
    html.H5('Faculty Governance', className='text-info mb-0'),
)

header = html.Div(
    [
        dbc.Row(
            [
                title,
                button_group,
                contact_popup,
            ],
            className='mt-4'
        ),
        html.Hr(className='mt-0'),
    ]
)
