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

# Standard library imports
import warnings

# Third party imports
import dash_html_components as html
import dash_bootstrap_components as dbc

# Local application imports
from app.users import User
from app.logger import DynamoAccessLogger

from app.navbar import serve_navbar
from app.searchcom.layouts.header import header
from app.searchcom.layouts.filters import serve_req_dropdown
from app.searchcom.layouts.search_info import search_info
from app.searchcom.layouts.charts import charts
from app.searchcom.layouts.footer import subfields
from app.searchcom.layouts.crosstab import crosstab_table
from app.searchcom.layouts.session_data import session_data


warnings.filterwarnings("ignore")
logger = DynamoAccessLogger('searchcom')  # Initialize logger with appropriate resource


def serve_searchcom_layout():

    # if has_request_context():
    #     session.permanent = True

    current_user = User()

    # Check access, no access if an empty list is returned from a User class
    if len(current_user.searchcom_access()) > 0:

        # Log that a user accesssed this view and was authorized
        logger.log_access(has_access=True)
        # Sub-layouts can be served from functions as well, if necessary, to enable dynamic updates
        # For example, when current user object is acesssed in the navbar/filters, which requires a request context

        layout = html.Div(
            [
                serve_navbar(),
                html.Div(
                    [
                        header,
                        serve_req_dropdown(),
                        search_info,
                        # serve_slider(),
                        charts,
                        subfields,
                        crosstab_table,
                        session_data
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
                html.H5('You don\'t have access to this dashboard.', className='alert-heading'),
                html.P(
                    'If your department has a ladder-rank search posted in RAPS, please reach out to Timur Gulyamov (tg2648) to get access.',
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
