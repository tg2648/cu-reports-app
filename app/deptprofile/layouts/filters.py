"""
Layout: Filters for charts
"""

# Third party imports
# from flask import current_app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
# import dash_html_components as html

# from boto3.dynamodb.conditions import Key

# import pandas as pd

# Local application imports
# from app.users import User
# from app.extensions import dynamo


ALL_DROPDOWN_OPTIONS = [
    {'value': 'AS', 'label': 'All A&S'},
    {'value': 'HUM_', 'label': '────────── Humanities ──────────', 'disabled': True},
    {'value': 'HUM', 'label': 'All Humanities'},
    {'value': 'AHAR', 'label': 'Art History and Archaeology'},
    {'value': 'CLAS', 'label': 'Classics'},
    {'value': 'EALC', 'label': 'East Asian Languages and Cultures'},
    {'value': 'ENCL', 'label': 'English and Comparative Literature'},
    {'value': 'FRRP', 'label': 'French and Romance Philology'},
    {'value': 'GERL', 'label': 'Germanic Languages'},
    {'value': 'ITAL', 'label': 'Italian'},
    {'value': 'LAIC', 'label': 'Latin American and Iberian Cultures'},
    {'value': 'MESA', 'label': 'Middle Eastern, South Asian, and African Studies'},
    {'value': 'MUSI', 'label': 'Music'},
    {'value': 'PHIL', 'label': 'Philosophy'},
    {'value': 'RELI', 'label': 'Religion'},
    {'value': 'SLAL', 'label': 'Slavic Languages'},
    {'value': 'NS_'	, 'label': '────────── Natural Sciences ──────────', 'disabled': True},
    {'value': 'NS', 'label': 'All Natural Sciences'},
    {'value': 'ASTR', 'label': 'Astronomy'},
    {'value': 'BIOL', 'label': 'Biological Sciences'},
    {'value': 'CHEM', 'label': 'Chemistry'},
    {'value': 'DEES', 'label': 'Earth and Environmental Sciences'},
    {'value': 'EEEB', 'label': 'Ecology, Evolution, and Environmental Biology'},
    {'value': 'MATH', 'label': 'Mathematics'},
    {'value': 'PHYS', 'label': 'Physics'},
    {'value': 'PSYC', 'label': 'Psychology'},
    {'value': 'STAT', 'label': 'Statistics'},
    {'value': 'SS_'	, 'label': '────────── Social Sciences ──────────', 'disabled': True},
    {'value': 'SS', 'label': 'All Social Sciences'},
    {'value': 'AFAM', 'label': 'African American and African Diaspora Studies'},
    {'value': 'ANTH', 'label': 'Anthropology'},
    {'value': 'ECON', 'label': 'Economics'},
    {'value': 'HIST', 'label': 'History'},
    {'value': 'POLS', 'label': 'Political Science'},
    {'value': 'SOCI', 'label': 'Sociology'},
]


def serve_dept_dropdown(dropdown_options):

    dept_dropdown = dbc.Row(
        dbc.Col(
            dbc.FormGroup(
                [
                    dcc.Dropdown(
                        id='dept-dropdown',
                        options=dropdown_options,
                        multi=False,
                        clearable=False,
                        value=dropdown_options[0]['value']
                    ),
                ]
            ),
            width=5,
            className='mt-3'
        )
    )

    return dept_dropdown
