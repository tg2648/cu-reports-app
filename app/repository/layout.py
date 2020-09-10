"""
Main dash layout

Assemble the layout from individual components
The .container class is applied to the navbar in its own module
This is in order to only center the navbar content and let the bar span the entire width of the page

Sticky filters are a separate component because the 'stickiness' doesn't work if nested inside a non-sticky div,
    which is what happens when all filters are imported as one object

The layout is served as a function in order to enable refreshes on page load
As described here: https://dash.plot.ly/live-updates
This is in order for Dash to pick-up the session cookie
"""

# Third party imports
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

# Local application imports
from app.users import User
from app.logger import DynamoAccessLogger

from app.navbar import serve_navbar
from app.repository.layouts.header import header
from app.repository.layouts.file_list import serve_file_list


logger = DynamoAccessLogger('facgov')  # Initialize logger with appropriate resource


def serve_repository_layout():

    current_user = User('tg2648')

    # Check access, no access if an empty list is returned from a User class
    if current_user.has_facgov_access():

        logger.log_access(has_access=True)

        layout = html.Div(
            [
                serve_navbar(),
                html.Div(
                    [
                        dcc.Location(id='facgov-url', refresh=True),
                        header,
                        serve_file_list(),
                    ],
                    className="container pb-5",
                ),
            ]
        )

    else:

        # Log that a user accesssed this view and was NOT authorized
        logger.log_access(has_access=False)

        no_access_alert = dbc.Alert(
            [
                html.H5('You don\'t have access to this page.', className='alert-heading'),
                html.P(
                    'Please reach out to Timur Gulyamov (tg2648) to get access.',
                    className='mb-0',
                ),
            ],
            color='warning',
            className='mt-3'
        )

        layout = html.Div(
            [
                serve_navbar(),
                html.Div(
                    [
                        no_access_alert
                    ],
                    className="container"
                ),
            ]
        )

    return layout
