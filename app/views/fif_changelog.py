"""FIF changelog routing
"""

# Third party imports
from flask import Blueprint
from flask import render_template_string
from flask import current_app
from flask_cas import login_required

# Local application imports
from app.logger import DynamoAccessLogger


bp = Blueprint('fif_changelog', __name__, url_prefix='/fif_changelog')


@bp.route('/')
@login_required
def index():
    logger = DynamoAccessLogger('fif_changelog')
    logger.log_access(has_access=True)

    bucket = current_app.config['S3_RESOURCE'].Bucket(current_app.config['TEMPLATES_BUCKET'])
    file_obj = bucket.Object('fif_changelog.html').get()
    template_string = file_obj['Body'].read().decode('utf-8')

    return render_template_string(template_string)
