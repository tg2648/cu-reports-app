"""
Error handlers
"""

# Third party imports
from flask import Blueprint
from flask import render_template


bp = Blueprint('errors', __name__)


class NotFoundError(ValueError):
    """Exception class for 404 errors"""
    pass


@bp.app_errorhandler(404)
def not_found_handler_404(error):
    """Generic handling of 404 errors"""
    message = 'Requested page does not exist.'
    return render_template('errors/404.html', message=message), 404


@bp.app_errorhandler(NotFoundError)
def not_found_handler_exc(error):
    """More flexible handling of 404-like errors. Use by raising NotFoundError.

    Args:
        error (str) - Custom message to display
    """
    return render_template('errors/404.html', message=error), 404
