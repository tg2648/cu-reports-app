"""Repository of various documents
"""

# Third party imports
from flask import Blueprint
from flask import render_template
from flask import Response
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from flask import abort
from flask_cas import login_required

from itsdangerous.exc import BadSignature

# Local application imports
from app.users import User
from app.utils.jinja_filters import file_name, file_type
from app.logger import DynamoAccessLogger
from app.errors.handlers import NotFoundError


bp = Blueprint('repository', __name__, url_prefix='/docs2')


# @login_required
@bp.route('/dl/<path:key>')
def download(key):
    """
    Downloads a file from S3 based on the key in the path
    """
    # logger = DynamoAccessLogger('fif_archive_download')

    client = current_app.config['S3_RESOURCE']
    bucket = client.Bucket(current_app.config['REPOSITORY_BUCKET'])

    # Reject keys that end with '/' which are valid S3 keys but are not files
    if key.endswith('/'):
        return redirect(url_for('repository.index'))

    try:
        file_obj = bucket.Object(key).get()
    except client.meta.client.exceptions.NoSuchKey:  # per boto3 docs
        # logger.log_access(has_access=True, downloaded_object=key)
        # return render_template('errors/404.html'), 404
        raise NotFoundError(f'File {file_name(key)} not found.')

    # logger.log_access(has_access=True, downloaded_object=key)
    return Response(
        file_obj['Body'].read(),
        mimetype=file_type(key),
        headers={"Content-Disposition": "inline; filename={}".format(file_name(key))}
    )
