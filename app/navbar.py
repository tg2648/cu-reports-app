'''
Layout: Navigation bar for Dash applications
Duplicates the navigation bar of the root of the website
by using the dash-bootstrap-components extension instead

TODO: a way of determining an active tab and changing the 'active' element of NavItems
'''

# Third party imports
import dash_bootstrap_components as dbc
import dash_html_components as html

# Local application imports
from app.users import User


LOGO_PATH = 'https://cu-dash-static.s3.us-east-2.amazonaws.com/img/crown-white.png'
current_user = User()


def serve_navbar():

    navbar_left = [
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink('Lab Occupancy Form', href='/lab_occupancy/', external_link=True)),
                html.Div(style={'border-left': '1px solid rgba(255,255,255,0.5)'}),
                # dbc.NavItem(dbc.NavLink('Dept. Profiles', href='/deptprofile/', external_link=True)),
                dbc.NavItem(dbc.NavLink('Search Dashboard', href='/searchcom/', external_link=True)),
                dbc.NavItem(dbc.NavLink('FIF Archive', href='/fif_archive/', external_link=True)),
            ],
            className='navbar-nav mr-auto'
        )
    ]

    navbar_right = [
        html.Span('Signed in as ' + current_user.uni, className='navbar-text'),
        html.A(
            dbc.Button('Logout', id='logout-button', className='btn-secondary my-2 ml-2 my-sm-0'),
            href='/logout'
        )
    ]

    navbar_brand = dbc.NavbarBrand(
        [
            html.Img(src=LOGO_PATH, height='30px', className='d-inline-block align-top mr-2'),
            'A&S Reporting'
        ],
        href='/',
        className='mb-0 h1',
        external_link=True
    )

    navbar = dbc.Navbar(
        [
            html.Div(
                [
                    navbar_brand,
                    dbc.NavbarToggler(id='navbar-toggler'),
                    # Collapse contains elements that will be collapsed when the window size changes
                    # Each navbar subcomponent is a list, need to merge into one list
                    # to pass as children
                    dbc.Collapse(
                        navbar_left + navbar_right,
                        id='navbar-collapse',
                        navbar=True),
                ],
                className='container'
            )
        ],
        color='dark',
        dark=True,
    )

    return navbar
