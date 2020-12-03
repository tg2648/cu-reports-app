"""
Repository of various documents
"""

# Third party imports
from flask import Blueprint
from flask import Response
from flask import redirect
from flask import current_app
from flask_cas import login_required

# Local application imports
from app.users import User
from app.utils.jinja_filters import file_name, file_type
from app.logger import DynamoAccessLogger
from app.errors.handlers import NotFoundError, ForbiddenError


bp = Blueprint('facgov', __name__, url_prefix='/faculty_governance')


@bp.route('/<path:key>')
@login_required
def download(key):
    """
    Downloads a file from S3 based on the key in the path
    """
    logger = DynamoAccessLogger('facgov_download')
    current_user = User()

    # Check access, no access if an empty list is returned from a User class
    if current_user.has_facgov_access():

        client = current_app.config['S3_RESOURCE']
        bucket = client.Bucket(current_app.config['FACGOV_BUCKET'])

        # Redirect to base url for keys that end with '/' which are valid S3 keys but are not files
        if key.endswith('/'):
            return redirect(bp.url_prefix)

        try:
            file_obj = bucket.Object(key).get()
        except client.meta.client.exceptions.NoSuchKey:  # per boto3 docs
            logger.log_access(has_access=False, downloaded_object=key)
            raise NotFoundError(f'File {file_name(key)} not found.')

        logger.log_access(has_access=True, downloaded_object=key)
        return Response(
            file_obj['Body'].read(),
            mimetype=file_type(key),
            headers={"Content-Disposition": "inline; filename={}".format(file_name(key))}
        )

    else:

        logger.log_access(has_access=False, downloaded_object=key)
        raise ForbiddenError('You do not have access to this page. \
                              Please reach out to Timur Gulyamov (tg2648) to get access.')
