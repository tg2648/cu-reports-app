"""
Dash callbacks
"""

# Third party imports
from dash.dependencies import Input, Output, State

# Local application imports
from app.deptprofile.callback_functions.faculty import register_faculty_callbacks
from app.deptprofile.callback_functions.classes import register_classes_callbacks
from app.deptprofile.callback_functions.students import register_students_callbacks


def register_deptprofile_callbacks(dashapp):

    register_faculty_callbacks(dashapp)
    register_classes_callbacks(dashapp)
    register_students_callbacks(dashapp)

    # Navbar Collapse Toggle
    @dashapp.callback(Output('navbar-collapse', 'is_open'),
                      [Input('navbar-toggler', 'n_clicks')],
                      [State('navbar-collapse', 'is_open')])
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # Button popups
    @dashapp.callback(
        Output('changelog-popup', 'is_open'),
        [Input('changelog-popup-button', 'n_clicks'), Input('close-changelog', 'n_clicks')],
        [State('changelog-popup', 'is_open')],
    )
    def toggle_changelog_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dashapp.callback(
        Output('notes-popup', 'is_open'),
        [Input('notes-popup-button', 'n_clicks'), Input('close-notes', 'n_clicks')],
        [State('notes-popup', 'is_open')],
    )
    def toggle_notes_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dashapp.callback(
        Output('contact-popup', 'is_open'),
        [Input('contact-popup-button', 'n_clicks'), Input('close-contact', 'n_clicks')],
        [State('contact-popup', 'is_open')],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
