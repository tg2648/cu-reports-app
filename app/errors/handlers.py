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


class ForbiddenError(ValueError):
    """Exception class for 403 errors"""
    pass


# @bp.app_errorhandler(404)
# def not_found_handler(error):
#     """Generic handling of 404 errors"""
#     message = 'Requested page does not exist.'
#     return render_template('errors/404.html', message=message), 404


@bp.app_errorhandler(NotFoundError)
def not_found_handler_exc(message):
    """More flexible handling of 404-like errors. Used by raising NotFoundError.

    Args:
        message (str) - Custom message to display
    """
    return render_template('errors/404.html', message=message), 404


# @bp.app_errorhandler(403)
# def forbidden_handler(error):
#     """Generic handling of 403 errors"""
#     message = 'You do not have access to this page. Please reach out to Timur Gulyamov (tg2648) to get access.'
#     return render_template('errors/403.html', message=message), 403


@bp.app_errorhandler(ForbiddenError)
def forbidden_handler_exc(message):
    """More flexible handling of 404-like errors. Used by raising ForbiddenError.

    Args:
        message (str) - Custom message to display
    """
    return render_template('errors/403.html', message=message), 403
