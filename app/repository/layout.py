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
# import dash_bootstrap_components as dbc
import dash_core_components as dcc

# Local application imports
# from app.users import User
# from app.logger import DynamoAccessLogger

from app.navbar import serve_navbar
from app.repository.layouts.header import header
from app.repository.layouts.file_list import file_list


# logger = DynamoAccessLogger('deptprofile')  # Initialize logger with appropriate resource


def serve_repository_layout():

    layout = html.Div(
        [
            serve_navbar(),
            dcc.Location(id='url', refresh=False),
            html.Div(
                [
                    header,
                    file_list,
                    html.Div(id='page-url')
                ],
                className="container pb-5",
            ),
        ]
    )

    return layout
