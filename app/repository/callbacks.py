"""
Dash callbacks
"""

# Third party imports
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import current_app
from flask import url_for

# Local application imports
from app.extensions import dynamo
from app.repository.models import CommitteeFiles
from app.repository.conversions import fiscal_to_academic


def register_repository_callbacks(dashapp):

    table = dynamo.tables[current_app.config['DB_REPOSITORY']]

    @dashapp.callback(Output('file-list-left', 'children'),
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
        # filter_expr = Attr('key').exists()

        # if not (unit == '' or unit is None):
        #     filter_expr = filter_expr & Attr('unit').eq(unit)

        # if not (year == '' or year is None):
        #     filter_expr = filter_expr & Attr('year').eq(year)

        # resp = table.scan(FilterExpression=filter_expr)

        key_expr = '#u = :u'
        expr_values = {
            ':u': unit
        }
        expr_names = {
            '#u': 'unit'
        }

        if not (year == '' or year is None):
            key_expr = f'{key_expr} AND #y = :y'
            expr_values[':y'] = year
            expr_names['#y'] = 'year'

        resp = table.query(
            IndexName='unit-year-index',
            KeyConditionExpression=key_expr,
            ExpressionAttributeValues=expr_values,
            ExpressionAttributeNames=expr_names,
        )

        items = resp['Items']
        files = CommitteeFiles(items=items)

        return files.file_list()

    # SEARCH #
    @dashapp.callback(Output('facgov-url', 'pathname'),
                      [Input('facgov-dropdown', 'value')])
    def on_dropdown_selection(value):
        if value == '' or value is None:
            raise PreventUpdate
        else:
            return url_for('repository.download', key=value)

    # YEAR CHECKBOXES #
    @dashapp.callback(Output('year-input', 'options'),
                      [Input('unit-input', 'value')])
    def build_year_options(unit):
        """
        Populate year checkboxes based on the selected unit.
        Needed to be done in a callback because not all units have files for all years.
        """
        table = dynamo.tables[current_app.config['DB_REPOSITORY']]
        resp = table.query(
            IndexName='unit-year-index',
            KeyConditionExpression='#u = :u',
            ExpressionAttributeValues={
                ':u': unit,
            },
            ExpressionAttributeNames={
                '#u': 'unit',
            },
        )

        items = resp['Items']
        years = sorted({item['year'] for item in items})

        options = [{'label': 'All', 'value': ''}]

        for year in reversed(years):
            options.append({'label': fiscal_to_academic(year), 'value': year})

        return options

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
