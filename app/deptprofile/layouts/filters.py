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


def serve_dept_dropdown():

    dept_dropdown = dbc.Row(
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Select department:", html_for="dept-dropdown"),
                    dcc.Dropdown(
                        id='dept-dropdown',
                        options=[
                            {"label": "Art History", "value": 'AHAR'},
                            {"label": "Anthropology", "value": 'ANTH'},
                            {"label": "History", "value": 'HIST'},
                            {"label": "Economics", "value": 'ECON'},
                            {"label": "Statistics", "value": 'STAT'},
                        ],
                        multi=False,
                        clearable=False,
                        value='STAT'
                    ),
                ]
            ),
            width=5,
            className='mt-3'
        )
    )

    return dept_dropdown
