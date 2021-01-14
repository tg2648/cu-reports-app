"""
Layout: File list
"""

# Third party imports
from flask import current_app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# Local application imports
from app.extensions import dynamo
from app.utils.func import multisort
from app.facgov.conversions import convert_for_checkbox, fiscal_to_academic


def build_search_dropdown():
    """
    Build dropdown options from unique years across all DB items
    Display in reverse order
    """
    table = dynamo.tables[current_app.config['DB_FACGOV']]
    resp = table.scan()

    # First sort by committee, then by year, then by file name
    items = multisort(resp['Items'], (('unit', True), ('year', True), ('file_name', False)))
    options = []

    for item in items:
        options.append(
            {'label': f"{convert_for_checkbox(item['unit'])} - {fiscal_to_academic(item['year'])} - {item['file_name']}",
             'value': item['key']}
        )

    return options


def serve_file_list():

    checklist_unit = dbc.FormGroup(
        [
            dbc.Label('Filter', className='h6 text-info'),
            dbc.RadioItems(
                options=[
                    {'label': 'Faculty Meetings', 'value': 'faculty_meeting'},
                    {'label': 'PPC', 'value': 'PPC'},
                    {'label': 'EPPC', 'value': 'EPPC'},
                    {'label': 'CED', 'value': 'CED'},
                ],
                value='faculty_meeting',
                id='unit-input',
            ),
        ]
    )

    checklist_year = dbc.FormGroup(
        [
            dbc.RadioItems(
                options=[],
                value='',
                id='year-input',
            ),
        ]
    )

    col_filter = html.Div(
        [
            checklist_unit,
            checklist_year,
        ],
        id='filter-column',
        className='col-sm-2 flex-column'
    )

    col_left = html.Div(
        id='file-list-left',
        className='col-sm',
    )

    col_search = html.Div(
        dcc.Dropdown(
            id='facgov-dropdown',
            options=build_search_dropdown(),
            placeholder='Search by filename',
            multi=False,
            clearable=True
        ),
        className='mb-3'
    )

    file_list = html.Div(
        [
            col_filter,
            html.Div(
                [
                    col_search,
                    html.Div(
                        [
                            col_left,
                        ],
                        className='row'
                    )
                ],
                className='col'
            )
        ],
        className='row mb-5'
    )

    return file_list
