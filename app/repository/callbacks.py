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


    @dashapp.callback(Output('page-url', 'children'),
                      [Input('url', 'pathname'),
                       Input('url', 'search'),
                       Input('url', 'hash')])
    def display_page(pathname, search, url_hash):

        return html.Div([
            html.H5('pathname: {}'.format(pathname)),
            html.H5('search: {}'.format(search)),
            html.H5('url_hash: {}'.format(url_hash))
        ])

    # FILE LIST - LEFT

    @dashapp.callback(Output('file-list-left', 'children'),
                      [Input('url', 'pathname'),
                       Input('unit-input', 'value'),
                       Input('year-input', 'value')])
    def committee_list_by_committee(url_pathname, unit, year):

        if (url_pathname is None) or (url_pathname == ''):
            raise PreventUpdate

        # By default, render the committee list
        if (url_pathname == '/faculty_governance/' or 'committees' in url_pathname):

            column_title = 'By committee'

            if (unit == '' or unit is None) and (year == '' or year is None):

                resp = table.query(
                    IndexName='ByCategory',
                    KeyConditionExpression='category = :category',
                    ExpressionAttributeValues={':category': 'committees'},
                    ScanIndexForward=False,
                )

            else:

                resp = table.query(
                    KeyConditionExpression=Key('PK').eq(unit),
                    ScanIndexForward=False,
                )

        elif ('minutes' in url_pathname):

            column_title = 'By meeting'

            if (unit == [] or unit is None):

                resp = table.query(
                    IndexName='ByCategory',
                    KeyConditionExpression='category = :category',
                    ExpressionAttributeValues={':category': 'minutes'},
                    ScanIndexForward=False,
                )

            else:

                resp = table.query(
                    IndexName='ByYear',
                    KeyConditionExpression='#year = :year',
                    FilterExpression='category = :category',
                    ExpressionAttributeNames={'#year': 'year'},
                    ExpressionAttributeValues={':year': '2019', ':category': 'minutes'},
                    ScanIndexForward=False,
                )

        items = resp['Items']
        files = CommitteeFiles(items=items)

        div = html.Div([html.H6(column_title, className='text-info'), files.file_list(groupby='committee')])

        return div

    # FILE LIST - RIGHT

    @dashapp.callback(Output('file-list-right', 'children'),
                      [Input('url', 'hash'),
                       Input('url', 'pathname'),])
    def committee_list_by_year(url_hash, url_pathname):

        if (url_pathname is None) or (url_pathname == ''):
            raise PreventUpdate

        # By default, render the committee list
        if (url_pathname == '/faculty_governance/' or 'committees' in url_pathname):

            if (url_hash is None) or (url_hash == ''):

                resp = table.query(
                    IndexName='ByCategory',
                    KeyConditionExpression='category = :category',
                    ExpressionAttributeValues={':category': 'committees'},
                    ScanIndexForward=False,
                )

            else:

                resp = table.query(
                    IndexName='ByYear',
                    KeyConditionExpression='#year = :year',
                    ExpressionAttributeNames={'#year': 'year'},
                    ExpressionAttributeValues={':year': '2019'},
                    ScanIndexForward=False,
                )

        elif ('minutes' in url_pathname):

            if (url_hash is None) or (url_hash == ''):

                resp = table.query(
                    IndexName='ByCategory',
                    KeyConditionExpression='category = :category',
                    ExpressionAttributeValues={':category': 'minutes'},
                    ScanIndexForward=False,
                )

            else:

                resp = table.query(
                    IndexName='ByYear',
                    KeyConditionExpression='#year = :year',
                    FilterExpression='category = :category',
                    ExpressionAttributeNames={'#year': 'year'},
                    ExpressionAttributeValues={':year': '2019', ':category': 'minutes'},
                    ScanIndexForward=False,
                )

        items = resp['Items']
        files = CommitteeFiles(items=items)

        div = html.Div([html.H6('By year', className='text-info'), files.file_list(groupby='year')])

        return div

    # BUTTONS

    @dashapp.callback([Output('committee-button', 'className'),
                       Output('minutes-button', 'className')],
                      [Input('url', 'pathname')])
    def button_color(url_pathname):
        """
        Simulate the effect of being 'active' on selection
        """

        if (url_pathname is None) or (url_pathname == ''):
            raise PreventUpdate

        # Committees is default
        if 'minutes' in url_pathname:
            return None, 'text-info'
        else:
            return 'text-info', None

    # NAVBAR #
    # Navbar Collapse Toggle
    @dashapp.callback(Output('navbar-collapse', 'is_open'),
                      [Input('navbar-toggler', 'n_clicks')],
                      [State('navbar-collapse', 'is_open')])
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
