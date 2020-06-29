"""
Layout: Elements to hold session data

"""

# Third party imports
import dash_core_components as dcc
import dash_html_components as html


session_data = html.Div(
    [
        dcc.Store(id='searchcom-session-data-applicant', storage_type='session'),
        dcc.Store(id='searchcom-session-data-posting', storage_type='session'),
        dcc.Store(id='searchcom-session-data-pipeline', storage_type='session'),
        dcc.Store(id='searchcom-session-data-subfields', storage_type='session')
    ]
)
