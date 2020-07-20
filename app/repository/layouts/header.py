"""
Layout: Top row
"""

# Third party imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


title = html.Div(
    html.H5('A&S Faculty Governance', className='text-info mb-0'),
    className='col'
)

# col1 = html.Div(
#     html.A('A&S Document Repository', className='text-info mb-0'),
#     className='col-sm-auto'
# )

# col1 = html.Div(
#     dcc.Link(
#         'Committee Reports & Letters',
#         id='committee-button',
#         href='committees'
#     ),
#     className='col-sm-auto'
# )

# col2 = html.Div(
#     dcc.Link(
#         'Minutes',
#         id='minutes-button',
#         href='minutes'
#     ),
#     className='col-sm-auto'
# )

header = html.Div(
    [
        html.Div(
            [
                title,
                # col1,
                # col2,
            ],
            className='row mt-4'
        ),
        html.Hr()
    ]
)
