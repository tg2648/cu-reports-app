"""
Layout: Top row
"""

# Third party imports
import dash_html_components as html


title = html.Div(
    html.H5('A&S Faculty Governance', className='text-info mb-0'),
    className='col'
)

header = html.Div(
    [
        html.Div(
            [
                title,
            ],
            className='row mt-4'
        ),
        html.Hr()
    ]
)
