"""
Dash callbacks
"""

# Third party imports
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
from flask import current_app
from boto3.dynamodb.conditions import Attr, Key

# Local application imports
from app.extensions import dynamo
from app.repository.models import CommitteeFiles


def register_repository_callbacks(dashapp):

    table = dynamo.tables[current_app.config['DB_REPOSITORY']]

    # FILE LIST - LEFT

    @dashapp.callback([Output('file-list-left', 'children'),
                       Output('file-list-right', 'children')],
                      [Input('unit-input', 'value'),
                       Input('year-input', 'value')])
    def display_lists(unit, year):
        """Outputs two divs using the helper CommitteeFiles files: one where the files are grouped by committee,
        and one where files are grouped by year

        Args:
            unit (str): Value of the unit-input radio buttons
            year (str): Value of the year-input radio buttons

        Returns:
            dash_html_components.html.Div: Description.
        """

        #  Since we can't initialize an empty filter, start with a 'dummy' that's always true
        filter_expr = Attr('PK').exists()

        if not (unit == '' or unit is None):
            filter_expr = filter_expr & Attr('PK').eq(unit)

        if not (year == '' or year is None):
            filter_expr = filter_expr & Attr('year').eq(year)

        resp = table.scan(FilterExpression=filter_expr)

        # if (unit == '' or unit is None):

        #     if (year == '' or year is None):
        #         resp = table.query(
        #             IndexName='ByCategory',
        #             KeyConditionExpression='category = :category',
        #             ExpressionAttributeValues={':category': 'committees'},
        #             ScanIndexForward=False,
        #         )
        #     else:
        #         resp = table.query(
        #             IndexName='ByCategory',
        #             KeyConditionExpression='category = :category',
        #             ExpressionAttributeValues={':category': 'committees'},
        #             FilterExpression=Attr('year').eq(year),
        #             ScanIndexForward=False,
        #         )           

        # else:

        #     if (year == '' or year is None):
        #         resp = table.query(
        #             KeyConditionExpression=Key('PK').eq(unit),
        #             ScanIndexForward=False,
        #         )
        #     else:
        #         resp = table.query(
        #             KeyConditionExpression=Key('PK').eq(unit),
        #             FilterExpression=Attr('year').eq(year),
        #             ScanIndexForward=False,
        #         )

        items = resp['Items']
        files = CommitteeFiles(items=items)

        div_left = html.Div([html.H6('By committee', className='text-info'), files.file_list(groupby='committee')])
        div_right = html.Div([html.H6('By year', className='text-info'), files.file_list(groupby='year')])

        return div_left, div_right

    # FILE LIST - RIGHT

    # @dashapp.callback(Output('file-list-right', 'children'),
    #                   [Input('unit-input', 'value'),
    #                    Input('year-input', 'value')])
    # def committee_list_by_year(unit, year):

    #     if (unit == '' or unit is None):

    #         if (year == '' or year is None):
    #             resp = table.query(
    #                 IndexName='ByCategory',
    #                 KeyConditionExpression='category = :category',
    #                 ExpressionAttributeValues={':category': 'committees'},
    #                 ScanIndexForward=False,
    #             )
    #         else:
    #             resp = table.query(
    #                 IndexName='ByCategory',
    #                 KeyConditionExpression='category = :category',
    #                 ExpressionAttributeValues={':category': 'committees'},
    #                 FilterExpression=Attr('year').eq(year),
    #                 ScanIndexForward=False,
    #             )           

    #     else:

    #         if (year == '' or year is None):
    #             resp = table.query(
    #                 KeyConditionExpression=Key('PK').eq(unit),
    #                 ScanIndexForward=False,
    #             )
    #         else:
    #             resp = table.query(
    #                 KeyConditionExpression=Key('PK').eq(unit),
    #                 FilterExpression=Attr('year').eq(year),
    #                 ScanIndexForward=False,
    #             )

    #     items = resp['Items']
    #     files = CommitteeFiles(items=items)

    #     div = html.Div([html.H6('By year', className='text-info'), files.file_list(groupby='year')])

    #     return div

    # NAVBAR #
    # Navbar Collapse Toggle
    @dashapp.callback(Output('navbar-collapse', 'is_open'),
                      [Input('navbar-toggler', 'n_clicks')],
                      [State('navbar-collapse', 'is_open')])
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
