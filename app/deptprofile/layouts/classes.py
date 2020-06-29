'''
Layout: Classes Tab
'''

# Third party imports
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Local application imports
from app.deptprofile.utils.modebar import modebar_config


"""
Charts of the tab
"""
classes_bar_chart = dcc.Graph(
    id='classes-bar-chart',
    figure=go.Figure(),
    config=modebar_config
)

classes_core_chart = dcc.Graph(
    id='classes-core-chart',
    figure=go.Figure(),
    config=modebar_config
)

classes_tree_chart = dcc.Graph(
    id='classes-tree-chart',
    figure=go.Figure(),
    config=modebar_config
)

enrollments_bar_chart = dcc.Graph(
    id='enrollments-bar-chart',
    figure=go.Figure(),
    config=modebar_config
)

enrollments_core_chart = dcc.Graph(
    id='enrollments-core-chart',
    figure=go.Figure(),
    config=modebar_config
)

enrollments_tree_chart = dcc.Graph(
    id='enrollments-tree-chart',
    figure=go.Figure(),
    config=modebar_config
)

"""
Slider for tree charts common to both chart types
"""
classes_tree_chart_slider = dbc.Col(
    dbc.FormGroup(
        dcc.Slider(
            id='classes-tree-chart-slider',
            min=0,
            max=10,
            step=1,
            marks={
                0: '2007/08',
                10: '2019/20'
            },
            value=10,
        )
    ),
    width=6
)

enrollments_tree_chart_slider = dbc.Col(
    dbc.FormGroup(
        dcc.Slider(
            id='enrollments-tree-chart-slider',
            min=0,
            max=10,
            step=1,
            marks={
                0: '2007/08',
                10: '2019/20'
            },
            value=10,
        )
    ),
    width=6
)

"""
Classes/enrollments groups
"""
classes_group = html.Div(
    [
        html.H5('Department Offered Courses: Classes by Instructor Appointment', className='text-info'),
        classes_bar_chart,
        html.H6('Excludes Core courses. See notes for additional details.', className='small text-muted'),
        html.H5('Core Courses: Classes by Instructor Appointment', className='text-info'),
        classes_core_chart,
        html.H6('Core includes: Literature Humanities, Contemporary Civilizations, Art Humanities, Music Humanitites,\
                Frontiers of Science, Writing. See notes for additional details.', className='small text-muted'),
        classes_tree_chart_slider,
        classes_tree_chart
    ]
)

enrollments_group = html.Div(
    [
        html.H5('Department Offered Courses: Enrollments by Instructor Appointment', className='text-info'),
        enrollments_bar_chart,
        html.H6('Excludes Core courses. See notes for additional details.', className='small text-muted'),
        html.H5('Core Courses: Enrollments by Instructor Appointment', className='text-info'),
        enrollments_core_chart,
        html.H6('Core includes: Literature Humanities, Contemporary Civilizations, Art Humanities, Music Humanitites,\
                Frontiers of Science, Writing. See notes for additional details.', className='small text-muted'),
        enrollments_tree_chart_slider,
        enrollments_tree_chart
    ]
)

"""
Main classes tab skeleton
"""
classes_tab = html.Div(
    [
        dbc.Form(
            [
                dbc.FormGroup(
                    dbc.RadioItems(
                        options=[
                            {'label': 'Enrollments', 'value': 'enrollments'},
                            {'label': 'Classes', 'value': 'classes'}
                        ],
                        value='enrollments',
                        id='classes-chart-choices',
                    ),
                ),
                dbc.Col(
                    dbc.FormGroup(
                        dcc.RangeSlider(
                            id='classes-bar-chart-slider',
                            min=0,
                            max=10,
                            step=1,
                            marks={
                                0: '2007/08',
                                10: '2019/20'
                            },
                            value=[0, 10],
                            allowCross=False
                        ),
                    ),
                    width=6
                )
            ]
        ),
        html.Div(id='classes-chart-container'),
    ]
)
