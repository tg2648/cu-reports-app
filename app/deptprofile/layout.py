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
# from dash.dependencies import ALL
import dash_html_components as html
import dash_bootstrap_components as dbc

from app.navbar import serve_navbar
from app.deptprofile.layouts.filters import serve_dept_dropdown
from app.deptprofile.layouts.filters import ALL_DROPDOWN_OPTIONS
from app.deptprofile.layouts.header import header
from app.deptprofile.layouts.tabs import tabs

# Local application imports
from app.users import User
from app.logger import DynamoAccessLogger


logger = DynamoAccessLogger('deptprofile')  # Initialize logger with appropriate resource


def serve_deptprofile_layout():

    current_user = User()

    depts = current_user.deptprofile_access('dept')

    if depts:

        logger.log_access(has_access=True)

        # Create a list of dropdown options based on user permissions
        # Do this here to call deptprofile_access only once
        dropdown_options = []
        for option in ALL_DROPDOWN_OPTIONS:
            if option['value'] in depts:
                dropdown_options.append(option)

        layout = html.Div(
            [
                serve_navbar(),
                html.Div(
                    [
                        header,
                        serve_dept_dropdown(dropdown_options=dropdown_options),
                        tabs
                    ],
                    className='container pb-5',
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
                    className='container'
                ),
            ]
        )

    return layout
