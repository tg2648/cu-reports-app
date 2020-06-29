"""
Layout: Dashboard charts
"""

# Third party imports
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Local application imports
from app.searchcom.chart_config.modebar import modebar_config


charts = html.Div(
    [

        html.Div(
            [
                html.H5(
                    'Representativeness: Gender and Ethnicity/Race'
                ),

                # CHART
                dcc.Graph(
                    id='searchcom-applicant-chart',
                    figure=go.Figure(),
                    config=modebar_config
                ),

                # Text when the chart cannot be displayed due to threshold restrictions
                html.P(
                    [
                        'To maintain confidentiality of applicant information, demographics are only displayed for three or more applicants. If no chart is displayed, there are fewer than three applicants.'
                    ],
                    id='searchcom-chart-threshold-warning',
                    className='text-warning',
                    style={'display': 'none'}
                )
            ]
        )
    ],
    className='mt-4'
)
