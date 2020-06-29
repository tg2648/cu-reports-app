"""
Layout: Crosstab table
"""

# Third party imports
import dash_bootstrap_components as dbc
import dash_html_components as html


table_header_ethnicity = [
    html.Tr(
        [
            html.Th('', style={'width': '5rem', 'border-right': '1px solid #dee2e6', 'border-top': '0px', 'border-bottom': '0px'}),
            html.Th('American Indian or Alaska Native', colSpan=3, style={'width': '5rem', 'border-right': '1px solid #dee2e6'}),
            html.Th('Asian', colSpan=3, style={'width': '5rem', 'border-right': '1px solid #dee2e6'}),
            html.Th('Black or African American', colSpan=3, style={'width': '5rem', 'border-right': '1px solid #dee2e6'}),
            html.Th('Native Hawaiian or Other Pacific Islander', colSpan=3, style={'width': '5rem', 'border-right': '1px solid #dee2e6'}),
            html.Th('White', colSpan=3, style={'width': '5rem', 'border-right': '1px solid #dee2e6'}),
            html.Th('N/A', colSpan=3, style={'width': '5rem', 'border-right': '1px solid #dee2e6'})
        ]
    )
]

table_subheader_hispanic = [
    html.Tr(
        [
            html.Td('', style={'border-right': '1px solid #dee2e6', 'border-top': '0px', 'border-bottom': '0px'}),
            html.Td('Hisp.'), html.Td('Non-H.'), html.Td('N/A', style={'border-right': '1px solid #dee2e6'}),
            html.Td('Hisp.'), html.Td('Non-H.'), html.Td('N/A', style={'border-right': '1px solid #dee2e6'}),
            html.Td('Hisp.'), html.Td('Non-H.'), html.Td('N/A', style={'border-right': '1px solid #dee2e6'}),
            html.Td('Hisp.'), html.Td('Non-H.'), html.Td('N/A', style={'border-right': '1px solid #dee2e6'}),
            html.Td('Hisp.'), html.Td('Non-H.'), html.Td('N/A', style={'border-right': '1px solid #dee2e6'}),
            html.Td('Hisp.'), html.Td('Non-H.'), html.Td('N/A', style={'border-right': '1px solid #dee2e6'}),
        ],
        className='font-italic'
    )
]

# Each cell id is of the format [ethnicity]-[hispanic]-[gender]
row_female = html.Tr(
    [
        html.Th('Female', scope='row', style={'border-left': '1px solid #dee2e6', 'border-right': '1px solid #dee2e6'}),
        html.Td(id='amind-hisp-fem'), html.Td(id='amind-nonhisp-fem'), html.Td(id='amind-na-fem', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='asian-hisp-fem'), html.Td(id='asian-nonhisp-fem'), html.Td(id='asian-na-fem', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='black-hisp-fem'), html.Td(id='black-nonhisp-fem'), html.Td(id='black-na-fem', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='pacific-hisp-fem'), html.Td(id='pacific-nonhisp-fem'), html.Td(id='pacific-na-fem', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='white-hisp-fem'), html.Td(id='white-nonhisp-fem'), html.Td(id='white-na-fem', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='na-hisp-fem'), html.Td(id='na-nonhisp-fem'), html.Td(id='na-na-fem', style={'border-right': '1px solid #dee2e6'})
    ]
)

row_male = html.Tr(
    [
        html.Th('Male', scope='row', style={'border-left': '1px solid #dee2e6', 'border-right': '1px solid #dee2e6'}),
        html.Td(id='amind-hisp-male'), html.Td(id='amind-nonhisp-male'), html.Td(id='amind-na-male', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='asian-hisp-male'), html.Td(id='asian-nonhisp-male'), html.Td(id='asian-na-male', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='black-hisp-male'), html.Td(id='black-nonhisp-male'), html.Td(id='black-na-male', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='pacific-hisp-male'), html.Td(id='pacific-nonhisp-male'), html.Td(id='pacific-na-male', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='white-hisp-male'), html.Td(id='white-nonhisp-male'), html.Td(id='white-na-male', style={'border-right': '1px solid #dee2e6'}),
        html.Td(id='na-hisp-male'), html.Td(id='na-nonhisp-male'), html.Td(id='na-na-male', style={'border-right': '1px solid #dee2e6'})
    ]
)

row_na = html.Tr(
    [
        html.Th('N/A', scope='row', style={'border-left': '1px solid #dee2e6', 'border-right': '1px solid #dee2e6', 'border-bottom': '1px solid #dee2e6'}),
        html.Td(id='amind-hisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='amind-nonhisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='amind-na-na', style={'border-right': '1px solid #dee2e6', 'border-bottom': '1px solid #dee2e6'}),
        html.Td(id='asian-hisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='asian-nonhisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='asian-na-na', style={'border-right': '1px solid #dee2e6', 'border-bottom': '1px solid #dee2e6'}),
        html.Td(id='black-hisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='black-nonhisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='black-na-na', style={'border-right': '1px solid #dee2e6', 'border-bottom': '1px solid #dee2e6'}),
        html.Td(id='pacific-hisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='pacific-nonhisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='pacific-na-na', style={'border-right': '1px solid #dee2e6', 'border-bottom': '1px solid #dee2e6'}),
        html.Td(id='white-hisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='white-nonhisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='white-na-na', style={'border-right': '1px solid #dee2e6', 'border-bottom': '1px solid #dee2e6'}),
        html.Td(id='na-hisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='na-nonhisp-na', style={'border-bottom': '1px solid #dee2e6'}), html.Td(id='na-na-na', style={'border-right': '1px solid #dee2e6', 'border-bottom': '1px solid #dee2e6'})
    ]
)

table_body = [row_female, row_male, row_na]
table = html.Small(
    dbc.Table(
        table_header_ethnicity + table_subheader_hispanic + table_body,
        id='searchcom-xtab-table',
        bordered=False,
        responsive=True,
        className='mt-3 text-center',
    )
)


crosstab_table = html.Div(
    [
        html.H5('All Applicants'),
        table,
        # Text when the table cannot be displayed due to threshold restrictions
        html.P(
            [
                'To maintain confidentiality of applicant information, demographics are only displayed if the applicant pool includes at least five women and five men. If no table is displayed, there are fewer than five women and five men applicants.'
            ],
            id='searchcom-xtab-threshold-warning',
            className='text-warning',
            style={'display': 'none'}
        )
    ],
    className='mt-4'
)
