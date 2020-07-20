"""
Layout: File list
"""

# Third party imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


checklist_unit = dbc.FormGroup(
    [
        dbc.Label('Filter', className='h6 text-info'),
        dbc.RadioItems(
            options=[
                {'label': 'All', 'value': ''},
                {'label': 'PPC', 'value': 'PPC'},
                {'label': 'CED', 'value': 'CED'},
            ],
            value='',
            id='unit-input',
        ),
    ]
)

checklist_year = dbc.FormGroup(
    [
        dbc.RadioItems(
            options=[
                {'label': 'All', 'value': ''},
                {'label': '2019', 'value': '2019'},
                {'label': '2018', 'value': '2018'},
            ],
            value='',
            id='year-input',
        ),
    ]
)

col1 = html.Div(
    [
        checklist_unit,
        checklist_year,
    ],
    id='filter-column',
    className='col-sm-2 flex-column'
)

col2 = html.Div(
    id='file-list-left',
    className='col-sm',
)

col3 = html.Div(
    id='file-list-right',
    className='col-sm',
)

file_list = html.Div(
    [
        col1,
        col2,
        col3
    ],
    className='row mb-5'
)
