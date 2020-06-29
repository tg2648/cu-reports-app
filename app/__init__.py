"""
Main application package

Contains the app factory function.
"""

# Third party imports
import dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask.helpers import get_root_path, get_debug_flag
from flask_cas import login_required

# Local application imports
from config import DevConfig, ProdConfig
from app.utils import jinja_filters


def create_app():
    """Application factory.

        - Creates a Flask object
        - Sets a config depending on the FLASK_DEBUG environment variable
        - Registers Flask extensions on routing (Flask blueprints)
        - Registers Dash applications

    Returns:
        Flask object
    """
    server = Flask(__name__)

    # Apply either development or production config
    Config = DevConfig if get_debug_flag() else ProdConfig
    server.config.from_object(Config)

    # Register Flask extensions and routing
    register_extensions(server)
    register_blueprints(server)

    # Register Jinja filters
    server.jinja_env.filters['datetimeformat'] = jinja_filters.datetimeformat
    server.jinja_env.filters['datetime_utc_to_est'] = jinja_filters.datetime_utc_to_est
    server.jinja_env.filters['file_type'] = jinja_filters.file_type
    server.jinja_env.filters['file_name'] = jinja_filters.file_name
    server.jinja_env.filters['serialize'] = jinja_filters.serialize
    server.jinja_env.filters['convert_to_list'] = jinja_filters.convert_to_list

    # Register Search Committee dashboard
    from app.searchcom.layout import serve_searchcom_layout as searchcom_layout
    from app.searchcom.callbacks import register_searchcom_callbacks as searchcom_callbacks
    register_dashapp(server, 'Search Committee Dashboard', 'searchcom', searchcom_layout, searchcom_callbacks)

    # # Register Department Profile dashboard
    # from app.deptprofile.layout import serve_deptprofile_layout as deptprofile_layout
    # from app.deptprofile.callbacks import register_deptprofile_callbacks as deptprofile_callbacks
    # register_dashapp(server, 'Dept. Profile', 'deptprofile', deptprofile_layout, deptprofile_callbacks)

    return server


def register_dashapp(app, title, base_pathname, serve_layout, register_callbacks):
    """Registers a Dash application. Comment out assets_external_path during local development.
    Assets located in assets_folder will be served from S3 when assets_external_path is uncommented.
    The folder structure in S3 should match that of assets_folder

    Args:
        app (Flask object): Flask server to which the Dash object is registered to.
        title (str): Title of the webpage in the browser.
        base_pathname (str): URL path where Dash application can be accessed from.
        serve_layout (func): Function that creates and returns the layout of the Dash application.
        register_callbacks (func): Function that defines callback functions of the Dash application.

    Returns:
        None
    """
    # Meta tags for viewport responsiveness
    meta_viewport = {
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
    }

    if get_debug_flag():

        # Dev Dash instance
        my_dashapp = dash.Dash(
            __name__,
            server=app,
            url_base_pathname=f'/{base_pathname}/',
            assets_folder=f'{get_root_path(__name__)}/assets/',
            external_stylesheets=[dbc.themes.CERULEAN]
        )

    else:

        # Prod Dash instance - serve assets from S3
        my_dashapp = dash.Dash(
            __name__,
            server=app,
            url_base_pathname=f'/{base_pathname}/',
            assets_folder=f'{get_root_path(__name__)}/assets/',
            assets_external_path='https://cu-dash-static.s3.us-east-2.amazonaws.com/assets/',
            external_stylesheets=[dbc.themes.CERULEAN]
        )

        my_dashapp.css.config.serve_locally = False
        my_dashapp.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                <!-- Global site tag (gtag.js) - Google Analytics -->
                <script async src="https://www.googletagmanager.com/gtag/js?id=UA-145333546-1"></script>
                <script>
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());

                gtag('config', 'UA-145333546-1');
                </script>
                {%metas%}
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''

    my_dashapp.title = title
    my_dashapp.config.suppress_callback_exceptions = True
    my_dashapp.config.meta_tags = [meta_viewport]
    my_dashapp.layout = serve_layout
    with app.app_context():  # Push an application context so we can use Flask's 'current_app'
        register_callbacks(my_dashapp)

    # Require login to access Dash pathnames
    _protect_dashviews(my_dashapp)


def _protect_dashviews(dashapp):
    """Restricts access to Dash URL paths

    Applies the `login_required` function of `flask_cas` to every view of a Dash application.

    Args:
        dashapp (Dash object)

    Returns:
        None
    """
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    """
    Registers Flask extensions to the Flask server.

    Args:
        server (Flask object)

    Returns:
        None
    """
    from app.extensions import cas
    from app.extensions import dynamo
    # from app.extensions import mail

    cas.init_app(server)
    dynamo.init_app(server)
    # mail.init_app(server)


def register_blueprints(server):
    """
    Registers web routing to the Flask server.

    Args:
        server (Flask object)

    Returns:
        None
    """
    from app.views import home
    from app.views import fif_archive
    from app.views import fif_changelog
    from app.views import lab_occupancy

    server.register_blueprint(home.bp)
    server.register_blueprint(lab_occupancy.bp)
    server.register_blueprint(fif_archive.bp)
    server.register_blueprint(fif_changelog.bp)
