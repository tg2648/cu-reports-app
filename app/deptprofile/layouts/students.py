'''
Layout: Students Tab
'''

# Third party imports
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Local application imports
from app.deptprofile.utils.modebar import modebar_config

"""
Components of the tab
"""

students_ug_chart = dcc.Graph(
    id='students-ug-chart',
    figure=go.Figure(),
    config=modebar_config
)

students_masters_chart = dcc.Graph(
    id='students-masters-chart',
    figure=go.Figure(),
    config=modebar_config
)

students_interdept_chart = dcc.Graph(
    id='students-interdept-chart',
    figure=go.Figure(),
    config=modebar_config
)

students_hybrid_chart = dcc.Graph(
    id='students-hybrid-chart',
    figure=go.Figure(),
    config=modebar_config
)

students_sps_chart = dcc.Graph(
    id='students-sps-chart',
    figure=go.Figure(),
    config=modebar_config
)

students_phd_chart = dcc.Graph(
    id='students-phd-chart',
    figure=go.Figure(),
    config=modebar_config
)

"""
Main students tab skeleton
"""
students_tab = html.Div(
    [
        html.H5('Undergraduate', id='students-ug-header', className='text-info'),
        students_ug_chart,
        html.Div(
            [
                html.H5('Masters', id='students-masters-header', className='text-info'),
                students_masters_chart,
            ],
            id='students-masters-container'
        ),
        html.Div(
            [
                html.H5('Interdepartmental Masters', id='students-interdept-header', className='text-info'),
                students_interdept_chart,
            ],
            id='students-interdept-container'
        ),
        html.Div(
            [
                html.H5('Hybrid Masters', id='students-hybrid-header', className='text-info'),
                students_hybrid_chart,
            ],
            id='students-hybrid-container'
        ),
        html.Div(
            [
                html.H5('SPS', id='students-sps-header', className='text-info'),
                students_sps_chart,
            ],
            id='students-sps-container'
        ),
        html.Div(
            [
                html.H5('PhD', id='students-phd-header', className='text-info'),
                students_phd_chart,
            ],
            id='students-phd-container'
        ),
    ]
)
