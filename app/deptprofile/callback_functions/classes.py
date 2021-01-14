"""
Faculty tab callacks
"""

# Third party imports
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from flask import current_app

from boto3.dynamodb.conditions import Attr

# Local application imports
from app.extensions import dynamo

from app.deptprofile.utils.styling import axes, margin
from app.deptprofile.utils.colors import enrollments_colors, classes_colors
from app.deptprofile.utils.years import YEARS, MAX_YEAR_ID, MAX_FISCAL_YEAR, make_academic_year_range

from app.deptprofile.layouts.classes import classes_group, enrollments_group


tenure_categories = {
    'Tenured': 'Tenured',
    'NTBOT': 'NTBOT',
    'NTBOT-professor-term': 'Term Asst. Prof.',
    'Lecturer': 'Lecturer',
    'Supplemental': 'Other Full-Time',
    'Part-time': 'Adjunct',
    'Graduate-student': 'Graduate St.',
}


def register_classes_callbacks(dashapp):

    @dashapp.callback(Output('classes-chart-container', 'children'),
                      [Input('classes-chart-choices', 'value')])
    def on_classes_chart_choice_change(choice):
        """
        Change the view based on the classes/enrollments choice
        """
        if choice == 'enrollments':
            return enrollments_group
        elif choice == 'classes':
            return classes_group

    table = dynamo.tables[current_app.config['DB_DEPTPROFILE']]

    # CLASSES

    @dashapp.callback(Output('classes-bar-chart', 'figure'),
                      [Input('dept-dropdown', 'value')])
    def update_classes_bar_chart(dept):

        # Use ExpressionAttributeNames because 'count' is a restricted keyword for ProjectionExpression
        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#AGG#CLASSES#2008',
                ':upper': f'DATA#AGG#CLASSES#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ProjectionExpression='#c, ten_stat',
            ExpressionAttributeNames={'#c': 'count'},
            ScanIndexForward=True,
        )

        data = resp['Items']

        chart_data = []
        x_axis = make_academic_year_range(3, MAX_YEAR_ID)

        for data_cat, chart_cat in tenure_categories.items():

            y_axis = [item.get('count') for item in data if item.get('ten_stat') == data_cat]

            chart_data.append(
                go.Bar(
                    name=chart_cat,
                    x=x_axis,
                    y=y_axis,
                    text=[f' {round(float(i)):,} ' for i in y_axis],  # pad with spaces to prevent labels from rotating
                    textposition='inside',
                    hovertext=[f'{chart_cat}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=classes_colors.get(data_cat),
                        line=dict(
                            color='floralwhite',
                            width=1
                        ),
                    )
                )
            )

        chart_layout = go.Layout(
            barmode='stack',
            xaxis=axes(),
            yaxis=axes(
                title='Number of Classes',
            ),
            legend={'traceorder': 'normal'},
            margin=margin(l=70),
        )

        return {'data': chart_data, 'layout': chart_layout}

    # CORE

    @dashapp.callback(Output('classes-core-chart', 'figure'),
                      [Input('dept-dropdown', 'value')])
    def update_classes_core_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#CLASSES#2008',
                ':upper': f'DATA#CLASSES#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            FilterExpression=Attr('course_type').eq('Core'),
            ProjectionExpression='#c, ten_stat',
            ExpressionAttributeNames={'#c': 'count'},
            ScanIndexForward=True,
        )

        data = resp['Items']

        x_axis = make_academic_year_range(3, MAX_YEAR_ID)
        chart_data = []
        for data_cat, chart_cat in tenure_categories.items():

            y_axis = [item.get('count') for item in data if item.get('ten_stat') == data_cat]

            chart_data.append(
                go.Bar(
                    name=chart_cat,
                    x=x_axis,
                    y=y_axis,
                    text=[f' {round(float(i)):,} ' for i in y_axis],  # pad with spaces to prevent labels from rotating
                    textposition='inside',
                    hovertext=[f'{chart_cat}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=classes_colors.get(data_cat),
                        line=dict(
                            color='floralwhite',
                            width=1
                        ),
                    )
                )
            )

        chart_layout = go.Layout(
            barmode='stack',
            xaxis=axes(),
            yaxis=axes(
                title='Number of Classes',
            ),
            legend={'traceorder': 'normal'},
            margin=margin(l=70),
        )

        return {'data': chart_data, 'layout': chart_layout}

    @dashapp.callback(Output('classes-tree-chart', 'figure'),
                      [Input('dept-dropdown', 'value'),
                       Input('classes-tree-chart-slider', 'value')])
    def update_classes_tree_chart(dept, slider_year):

        chart_year = YEARS.get(slider_year).academic
        data_year = YEARS.get(slider_year).fiscal

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': f'DATA#AGG#CLASSES#{data_year}',
                ':upper': f'DATA#AGG#CLASSES#{int(data_year) + 1}$',
            },
            ProjectionExpression='#c, ten_stat',
            ExpressionAttributeNames={'#c': 'count'},
            ScanIndexForward=True,
        )

        data = resp['Items']

        labels, parents, values = [], [], []
        for data_cat, chart_cat in tenure_categories.items():
            labels.append(chart_cat)
            parents.append(chart_year)
            value = [int(float(item.get('count'))) for item in data if item.get('ten_stat') == data_cat]
            values.append(value[0])

        chart_data = []
        chart_data.append(
            go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                texttemplate='%{label}<br>%{percentRoot} (%{value})',
            )
        )

        chart_layout = go.Layout(
            margin=margin(l=70),
        )

        return {'data': chart_data, 'layout': chart_layout}

    # ENROLLMENTS

    @dashapp.callback(Output('enrollments-bar-chart', 'figure'),
                      [Input('dept-dropdown', 'value')])
    def update_enrollments_bar_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#AGG#ENRL#2008',
                ':upper': f'DATA#AGG#ENRL#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ProjectionExpression='#c, ten_stat',
            ExpressionAttributeNames={'#c': 'count'},
            ScanIndexForward=True,
        )

        data = resp['Items']

        chart_data = []
        x_axis = make_academic_year_range(3, MAX_YEAR_ID)

        for data_cat, chart_cat in tenure_categories.items():

            y_axis = [item.get('count') for item in data if item.get('ten_stat') == data_cat]

            chart_data.append(
                go.Bar(
                    name=chart_cat,
                    x=x_axis,
                    y=y_axis,
                    text=[f' {round(float(i)):,} ' for i in y_axis],  # pad with spaces to prevent labels from rotating
                    textposition='inside',
                    hovertext=[f'{chart_cat}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=enrollments_colors.get(data_cat),
                        line=dict(
                            color='floralwhite',
                            width=1
                        ),
                    )
                )
            )

        chart_layout = go.Layout(
            barmode='stack',
            xaxis=axes(),
            yaxis=axes(
                title='Number of Enrollments',
            ),
            legend={'traceorder': 'normal'},
            margin=margin(l=70),
        )

        return {'data': chart_data, 'layout': chart_layout}

    # CORE

    @dashapp.callback(Output('enrollments-core-chart', 'figure'),
                      [Input('dept-dropdown', 'value')])
    def update_enrollments_core_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#ENRL#2008',
                ':upper': f'DATA#ENRL#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            FilterExpression=Attr('course_type').eq('Core'),
            ProjectionExpression='#c, ten_stat',
            ExpressionAttributeNames={'#c': 'count'},
            ScanIndexForward=True,
        )

        data = resp['Items']

        x_axis = make_academic_year_range(3, MAX_YEAR_ID)
        chart_data = []
        for data_cat, chart_cat in tenure_categories.items():

            y_axis = [item.get('count') for item in data if item.get('ten_stat') == data_cat]

            chart_data.append(
                go.Bar(
                    name=chart_cat,
                    x=x_axis,
                    y=y_axis,
                    text=[f' {round(float(i)):,} ' for i in y_axis],  # pad with spaces to prevent labels from rotating
                    textposition='inside',
                    hovertext=[f'{chart_cat}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=enrollments_colors.get(data_cat),
                        line=dict(
                            color='floralwhite',
                            width=1
                        ),
                    )
                )
            )

        chart_layout = go.Layout(
            barmode='stack',
            xaxis=axes(),
            yaxis=axes(
                title='Number of Enrollments',
            ),
            legend={'traceorder': 'normal'},
            margin=margin(l=70),
        )

        return {'data': chart_data, 'layout': chart_layout}
