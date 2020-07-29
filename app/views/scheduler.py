"""
Scheduler
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
from flask import jsonify
from flask_cas import login_required

from itsdangerous.exc import BadSignature

# Local application imports
from app.users import User
from app.utils.jinja_filters import file_name, file_type
from app.logger import DynamoAccessLogger
from app.extensions import dynamo


bp = Blueprint('scheduler', __name__, url_prefix='/room_scheduler')


# @login_required
@bp.route('/')
def index():

    return render_template('scheduler.html')


@bp.route('/event_data')
def return_event_data():

    if not ('start' in request.args and 'end' in request.args):
        return redirect(url_for('scheduler.index'))

    # events = [
    #     {
    #         "title": "John Appleseed",
    #         "start": "2020-07-24T12:30:00",
    #         "end": "2020-07-24T13:30:00",
    #         'resourceId': 'a'
    #     },
    #     {
    #         "title": "Bobert",
    #         "start": "2020-07-24T09:00:00",
    #         "end": "2020-07-24T11:00:00",
    #         'resourceId': 'b'
    #     }
    # ]

    table_name = current_app.config['DB_SCHEDULING']
    resp = dynamo.tables[table_name].scan(
        FilterExpression='#s BETWEEN :lower AND :upper',
        ExpressionAttributeValues={
            ':lower': request.args.get('start'),
            ':upper': request.args.get('end'),
        },
        ProjectionExpression='title, #s, #e, resourceId',
        ExpressionAttributeNames={'#s': 'start', '#e': 'end'},
    )

    return jsonify(resp['Items'])


@bp.route('/resource_data')
def return_resource_data():

    # print(f'resource_data headers: {request.headers}')
    # print(f'resource_data args: {request.args}')

    resources = [
        {'id': 'a', 'room': '100 Dodge', 'title': 'Space A'},
        {'id': 'b', 'room': '100 Dodge', 'title': 'Space B'},
        {'id': 'c', 'room': '100 Dodge', 'title': 'Space C'},
        {'id': 'd', 'room': '200 Dodge', 'title': 'Space A'},
        {'id': 'e', 'room': '200 Dodge', 'title': 'Space B'},
        {'id': 'f', 'room': '200 Dodge', 'title': 'Space C'},
    ]

    return jsonify(resources)


@bp.route('/event_drop', methods=['POST'])
def on_event_drop():

    # print(f'event_drop data: {request.json}')
    # print(f'event_drop args: {request.args}')

    return '200'

@bp.route('/event_selection', methods=['POST'])
def on_event_selection():

    current_user = User('tg2648')
    data = request.json

    uni = current_user.uni
    title = f"{uni}'s event"

    item = {
        'PK': uni,
        'SK': f"EVENT#{data.get('start')}#{data.get('resourceId')}",
        'start': data.get('start'),
        'end': data.get('end'),
        'resourceId': data.get('resourceId'),
        'title': title
    }

    table_name = current_app.config['DB_SCHEDULING']
    dynamo.tables[table_name].put_item(Item=item)

    return title, 200
