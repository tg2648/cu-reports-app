"""
Layout: Filters for charts
"""

# Third party imports
from flask import current_app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from boto3.dynamodb.conditions import Key

import pandas as pd

# Local application imports
from app.users import User
from app.extensions import dynamo


def build_req_dropdown_options(current_user_reqs):
    """
    Builds dropdown options in the form [requisition number]: [department] - [position title]
    First uses the posting table to obtain all search info
    Then utilizes a DataFrame to sort first on the department name, then on the requisition number

    Args:
        List of requisition numbers to which user has access to.

    Returns:
        A list of dictionaries to populate the 'options' arguments of a dropdown component
    """
    posting_table = dynamo.tables[current_app.config['DB_SEARCHCOM_POSTING']]

    search_info = {
        'req_num': [],
        'dept_name': [],
        'position_title': [],
        'academic_year': [],
    }

    for req_num in current_user_reqs:
        response = posting_table.query(
            KeyConditionExpression=Key('req_num').eq(req_num),
            ProjectionExpression='dept_name,position_title,academic_year'  # will return only these attributes
        )

        dept_name = response['Items'][0]['dept_name']
        position_title = response['Items'][0]['position_title']
        academic_year = response['Items'][0]['academic_year']

        search_info['req_num'].append(req_num)
        search_info['dept_name'].append(dept_name)
        search_info['position_title'].append(position_title)
        search_info['academic_year'].append(academic_year)

    options_df = pd.DataFrame.from_dict(search_info)
    options_df.sort_values(by=['dept_name', 'academic_year', 'req_num'], inplace=True, ascending=[True, False, True])

    options = []
    for i in range(len(options_df)):
        options.append({'label': f"{options_df['academic_year'].iloc[i]} - {options_df['req_num'].iloc[i]} - {options_df['dept_name'].iloc[i]} - {options_df['position_title'].iloc[i]}", 'value': options_df['req_num'].iloc[i]})

    return options


def serve_req_dropdown():

    current_user = User()
    current_user_reqs = current_user.searchcom_access()

    req_dropdown_options = build_req_dropdown_options(current_user_reqs)

    req_dropdown = html.Div(
        dbc.FormGroup(
            [
                dbc.Label("Select search:", html_for="req-num-dropdown"),
                dcc.Dropdown(
                    id='req-num-dropdown',
                    options=req_dropdown_options,
                    value=req_dropdown_options[0]['value'],
                    multi=False,
                    clearable=False
                ),
            ]
        ),
        className='mt-3'
    )

    return req_dropdown


def serve_slider():

    slider = dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Refresh Date:", html_for="refresh-date-slider"),
                        dcc.Slider(
                            min=0,
                            max=9,
                            marks={i: 'Label {}'.format(i) for i in range(10)},
                            value=5,
                        ),
                    ]
                ),
                width=8
            )
        ],
        className='mt-3'
    )

    return slider
