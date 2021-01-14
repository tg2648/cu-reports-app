"""
Layout: Tabs
"""

# Third party imports
import dash_core_components as dcc

# Local application imports
from app.deptprofile.layouts.faculty import faculty_tab
from app.deptprofile.layouts.students import students_tab
from app.deptprofile.layouts.classes import classes_tab


tab_style = {
    'backgroundColor': 'white',
    'padding': '12px',
    'color': 'black',
    'height': '50px',

}

tab_selected_style = {
    'padding': '12px',
    'color': 'black',
    'height': '50px',
    'border-top-color': '#033C73'
}

tabs = dcc.Tabs(
    value='faculty',
    children=[
        dcc.Tab(faculty_tab, label='Faculty', value='faculty', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(students_tab, label='Students', value='students', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(classes_tab, label='Classes', value='classes', style=tab_style, selected_style=tab_selected_style),
    ],
    id='tabs',
    className='my-3'
)
