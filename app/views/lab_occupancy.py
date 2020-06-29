"""
Lab occupancy form routing
"""

# Standard library imports
from datetime import datetime

# Third party imports
from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request
from flask_cas import login_required

# Local application imports
from app.users import User
from app.extensions import dynamo


bp = Blueprint('lab_occupancy', __name__, url_prefix='/lab_occupancy')


@bp.route('/')
@login_required
def index():
    current_user = User()
    form_url = current_app.config['FORM_URL']

    # Get all existing records
    table_name = current_app.config['DB_LAB_OCCUPANCY']
    records = dynamo.tables[table_name].query(
        KeyConditionExpression='uni = :uni AND #t BETWEEN :lower AND :upper',
        ExpressionAttributeValues={
            ':uni': current_user.uni,
            ':lower': '2020-06-21',
            ':upper': '9999-99-99'
        },
        ExpressionAttributeNames={'#t': 'timestamp'},  # timestamp is a reserved keyword
        ScanIndexForward=False,
    )

    return render_template('lab_occupancy.html', uni=current_user.uni, url=form_url, records=records['Items'])


@bp.route('/cognito', methods=['POST'])
def cognito_webhook():
    """
    Accepts JSON data from Cognito and records it in a Dynamo table
    https://www.cognitoforms.com/support/66/data-integration/webhooks
    """
    table_name = current_app.config['DB_LAB_OCCUPANCY']
    req_data = request.json

    try:

        destination = req_data['Destination']

        if destination.lower() == 'my lab':
            # In this case, rooms are in a list of dictionaries
            rooms = [str(r['Label']) for r in req_data['RoomByPI']]
            room = ', '.join(rooms)
        elif destination.lower() == 'another lab':
            room = f"{req_data['BuildingOther']} {req_data['RoomOther']['Label']}"

        item = {
            'timestamp': req_data['Entry']['Timestamp'],
            'uni': req_data['UNI'],
            'action': req_data['Action'],
            'destination': destination,
            'room': room
        }

        dynamo.tables[table_name].put_item(Item=item)

        return 'Success'

    except KeyError:

        dynamo.tables[table_name].put_item(Item={
            'timestamp': str(datetime.now()),
            'uni': 'key error',
        })

        return 'Failure'
