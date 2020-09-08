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

from app.navbar import serve_navbar
from app.deptprofile.layouts.filters import serve_dept_dropdown
from app.deptprofile.layouts.header import header
from app.deptprofile.layouts.tabs import tabs


def serve_deptprofile_layout():

    layout = html.Div(
        [
            serve_navbar(),
            html.Div(
                [
                    header,
                    serve_dept_dropdown(),
                    tabs
                ],
                className="container pb-5",
            ),
        ]
    )

    return layout
