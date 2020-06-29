"""FIF archive routing
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


bp = Blueprint('fif_archive', __name__, url_prefix='/fif_archive')


@bp.route('/')
@login_required
def index():
    logger = DynamoAccessLogger('fif_archive')
    logger.log_access(has_access=True)

    current_user = User()
    bucket = current_app.config['S3_RESOURCE'].Bucket(current_app.config['FIF_FILES_BUCKET'])
    bucket_prefix = f'{current_user.uni}/'

    objs = bucket.objects.filter(Prefix=bucket_prefix)
    return render_template('fif_archive.html', files=objs)


@bp.route('/download', methods=['POST'])
@login_required
def download():
    """
    The key is serialized in the template to prevent tampering. Needs to be de-serialized first.
    """
    logger = DynamoAccessLogger('fif_archive_download')
    s = current_app.config['SERIALIZER']

    try:
        key = s.loads(request.form['key'])
    except BadSignature:
        logger.log_access(has_access=False)
        abort(400)

    bucket = current_app.config['S3_RESOURCE'].Bucket(current_app.config['FIF_FILES_BUCKET'])
    file_obj = bucket.Object(key).get()

    logger.log_access(has_access=True, downloaded_object=key)

    return Response(
        file_obj['Body'].read(),
        mimetype=file_type(key),
        headers={"Content-Disposition": "attachment;filename={}".format(file_name(key))}
    )


@bp.route('/download', methods=['GET'])
@login_required
def download_redirect():
    return redirect(url_for('fif_archive.index'))
