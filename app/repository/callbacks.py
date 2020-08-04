"""
Dash callbacks
"""

# Third party imports
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
from flask import current_app
from flask import url_for
from boto3.dynamodb.conditions import Attr

# Local application imports
from app.extensions import dynamo
from app.repository.models import CommitteeFiles


def register_repository_callbacks(dashapp):

    table = dynamo.tables[current_app.config['DB_REPOSITORY']]

    @dashapp.callback([Output('file-list-left', 'children'),
                       Output('file-list-right', 'children')],
                      [Input('unit-input', 'value'),
                       Input('year-input', 'value')])
    def display_lists(unit, year):
        """Outputs two divs using the helper CommitteeFiles class: one where the files are grouped by committee,
        and one where files are grouped by year

        Args:
            unit (str): Value of the unit-input radio buttons
            year (str): Value of the year-input radio buttons

        Returns:
            dash_html_components.html.Div: Divs for both lists.
        """

        #  Since we can't initialize an empty filter, start with a 'dummy' that's always true
        filter_expr = Attr('key').exists()

        if not (unit == '' or unit is None):
            filter_expr = filter_expr & Attr('unit').eq(unit)

        if not (year == '' or year is None):
            filter_expr = filter_expr & Attr('year').eq(year)

        resp = table.scan(FilterExpression=filter_expr)

        items = resp['Items']
        files = CommitteeFiles(items=items)

        div_left = html.Div([html.H5('By committee', className='text-info'), files.file_list(groupby='committee')])
        div_right = html.Div([html.H5('By year', className='text-info'), files.file_list(groupby='year')])

        return div_left, div_right

    # SEARCH #
    @dashapp.callback(Output('facgov-url', 'pathname'),
                      [Input('facgov-dropdown', 'value')])
    def on_dropdown_selection(value):
        if value == '' or value is None:
            raise PreventUpdate
        else:
            return url_for('repository.download', key=value)

    # NAVBAR #
    @dashapp.callback(Output('navbar-collapse', 'is_open'),
                      [Input('navbar-toggler', 'n_clicks')],
                      [State('navbar-collapse', 'is_open')])
    def toggle_navbar_collapse(n, is_open):
        """
        Navbar collapse toggle
        """
        if n:
            return not is_open
        return is_open
