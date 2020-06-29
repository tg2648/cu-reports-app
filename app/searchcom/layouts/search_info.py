"""
Layout: Basic search committee info
"""

# Third party imports
import dash_bootstrap_components as dbc
import dash_html_components as html


search_info = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.Span('Department: '),
                    html.Span(children='', id='search-info-dept', className='text-primary font-weight-bolder')
                ],
                width=8
            ),
            dbc.Col(
                [
                    html.Span('Search Open Date: '),
                    html.Span(id='search-info-open-date', className='text-primary font-weight-bolder')
                ],
                width='auto'
            )
        ]),

        dbc.Row([
            dbc.Col(
                [
                    html.Span('Position Title: '),
                    html.Span(id='search-info-title', className='text-primary font-weight-bolder')
                ],
                width=8
            ),
            dbc.Col(
                [
                    html.Span('Position Start Date: '),
                    html.Span(id='search-info-start-date', className='text-primary font-weight-bolder')
                ],
                width='auto'
            )
        ]),

        dbc.Row([
            dbc.Col(
                [
                    html.Span('Specialization: '),
                    html.Span(children='', id='search-info-field', className='text-primary font-weight-bolder')
                ],
                width=8
            ),
            dbc.Col(
                [
                    html.Span('Data Refresh Date: '),
                    html.Span(children='', id='search-info-data-refresh', className='text-primary')
                ],
                width='auto',
                className='font-italic'
            )
        ])
    ],
    id='basic-search-info'
)
