'''
Layout: Faculty Tab
'''

# Third party imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go

# Local application imports
from app.deptprofile.utils.modebar import modebar_config
from app.deptprofile.utils.years import MAX_ACADEMIC_YEAR

"""
Components of the tab (charts/tables)
"""

# Not wrapping in Col would make the table go outside the container width for some reason
faculty_table = dbc.Col(dash_table.DataTable(
    id='faculty-table',
    columns=[
        {'name': 'Tenure Status', 'id': 'ten_stat'},
        {'name': 'Rank', 'id': 'rank'},
        {'name': 'Name', 'id': 'name'},
        {'name': 'Joint/Interdisc.', 'id': 'joint_interdisc'},
        {'name': 'FTE', 'id': 'fte'},
    ],
    data=[],
    style_cell={'textAlign': 'left',
                'font-family': 'sans-serif',
                'font-size': '14px'},
    style_cell_conditional=[
        {
            'if': {'column_id': 'fte'},
            'textAlign': 'right'
        },
        {
            'if': {'column_id': 'joint'},
            'width': '12%'
        },
        {
            'if': {'column_id': 'tenure_status'},
            'width': '15%'
        },

    ],
    style_as_list_view=True,
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'border-top': '0px'
    },
))

faculty_fte_chart = dcc.Graph(
    id='faculty-fte-chart',
    figure=go.Figure(),
    config=modebar_config
)

faculty_demo_chart = dcc.Graph(
    id='faculty-demo-chart',
    figure=go.Figure(),
    config=modebar_config
)

"""
Main faculty tab skeleton
"""
faculty_tab = html.Div(
    [
        dbc.FormGroup(
            [
                dbc.Label('Show by:', html_for='faculty-chart-choices', className='pr-3', width=1),
                dbc.Col(
                    dbc.RadioItems(
                        options=[
                            {'label': 'Ladder-rank: FTE and Demographics', 'value': 'fte-with-demo'},
                            {'label': 'Faculty and Instructors', 'value': 'fte'}
                        ],
                        value='fte-with-demo',
                        inline=True,
                        id='faculty-chart-choices',
                    ),
                    className='align-self-center',
                    width=11,
                ),
            ],
            row=True
        ),
        html.Div(id='faculty-chart-container'),
        html.Div(
            [
                html.H5(MAX_ACADEMIC_YEAR, className='text-info'),
                faculty_table,
            ],
            id='faculty-table-container'
        )
    ]
)
