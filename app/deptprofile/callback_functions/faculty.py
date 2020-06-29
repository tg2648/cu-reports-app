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
from app.deptprofile.utils.colors import colors, faculty_colors
from app.deptprofile.utils.years import MAX_YEAR_ID, MAX_FISCAL_YEAR, make_academic_year_range
from app.deptprofile.utils.charts import make_text_labels

from app.deptprofile.layouts.faculty import faculty_fte_chart, faculty_demo_chart


def register_faculty_callbacks(dashapp):

    table = dynamo.tables[current_app.config['DB_DEPTPROFILE']]

    # CHART

    @dashapp.callback(Output('faculty-chart-container', 'children'),
                      [Input('faculty-chart-choices', 'value')])
    def on_faculty_chart_choice_change(choice):
        """
        Change the view based on the faculty chart
        """
        if choice == 'fte':
            return faculty_fte_chart
        elif choice == 'fte-with-demo':
            return faculty_demo_chart

    @dashapp.callback(Output('faculty-fte-chart', 'figure'),
                      [Input('dept-dropdown', 'value')])
    def update_faculty_fte_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#FACULTY_DATA#2005',
                ':upper': f'DATA#FACULTY_DATA#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ProjectionExpression='fte, ten_stat',
            ScanIndexForward=True,
        )

        data = resp['Items']

        chart_data = []
        x_axis = make_academic_year_range(0, MAX_YEAR_ID)

        # Categories determine filtering for the y-axis and obtaining a color
        category_names = {
            'Tenured': 'Tenured',
            'NTBOT': 'NTBOT',
            'NTBOT-professor-term': 'Term Asst. Prof',
            'Lecturers': 'Lecturers',
            'Other Full-Time': 'Other Full-Time',
            'Adjunct': 'Adjunct',
        }

        for cat in category_names.keys():

            y_axis = [item.get('fte') for item in data if item.get('ten_stat') == cat]

            chart_data.append(
                go.Bar(
                    name=category_names.get(cat),
                    x=x_axis,
                    y=y_axis,
                    text=[f' {round(float(i))} ' for i in y_axis],  # pad with spaces to prevent labels from rotating
                    textposition='inside',
                    hovertext=[f'{cat}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=faculty_colors.get(cat),
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
                title='FTE for Faculty/Person Count for Adjuncts',
            ),
            legend={'traceorder': 'normal'},
            margin=margin(),
        )

        return {'data': chart_data, 'layout': chart_layout}

    @dashapp.callback(Output('faculty-demo-chart', 'figure'),
                      [Input('dept-dropdown', 'value')])
    def update_faculty_demo_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#FACULTY_DATA#2005',
                ':upper': f'DATA#FACULTY_DATA#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            FilterExpression=Attr('ten_stat').eq('Tenured') | Attr('ten_stat').eq('NTBOT'),
            ProjectionExpression='fte, ten_stat, percent_fem, percent_urm',
            ScanIndexForward=True,
        )

        data = resp['Items']

        chart_data = []
        x_axis = make_academic_year_range(0, MAX_YEAR_ID)

        # Construct charts without a loop to preserve y values for further calculation

        y_axis_bar_t = [item.get('fte') for item in data if item.get('ten_stat') == 'Tenured']

        chart_data.append(
            go.Bar(
                name='Tenured',
                x=x_axis,
                y=y_axis_bar_t,
                text=[f' {round(float(i))} ' for i in y_axis_bar_t],  # pad with spaces to prevent labels from rotating
                textposition='inside',
                hovertext=[f'Tenured: {i}' for i in y_axis_bar_t],
                hoverinfo='text',
                marker=dict(
                    color=faculty_colors.get('Tenured'),
                    line=dict(
                        color='floralwhite',
                        width=1
                    ),
                )
            )
        )

        y_axis_bar_nt = [item.get('fte') for item in data if item.get('ten_stat') == 'NTBOT']

        chart_data.append(
            go.Bar(
                name='NTBOT',
                x=x_axis,
                y=y_axis_bar_nt,
                text=[f' {round(float(i))} ' for i in y_axis_bar_nt],  # pad with spaces to prevent labels from rotating
                textposition='inside',
                hovertext=[f'NTBOT: {i}' for i in y_axis_bar_nt],
                hoverinfo='text',
                marker=dict(
                    color=faculty_colors.get('NTBOT'),
                    line=dict(
                        color='floralwhite',
                        width=1
                    ),
                )
            )
        )

        # LINE PLOTS

        y_axis_line_t = [round(float(item.get('percent_fem')) * 100) if item.get('percent_fem') is not None else None
                         for item in data if item.get('ten_stat') == 'Tenured']
        hover_labels = [f'{i}%' if i is not None else None for i in y_axis_line_t]
        text_labels = make_text_labels(hover_labels)

        chart_data.append(
            go.Scatter(
                name='% Tenured Female',
                x=x_axis,
                y=y_axis_line_t,
                mode='lines+markers+text',
                text=text_labels,
                textposition='top center',
                textfont=dict(
                    color=colors.get('orange2'),
                ),
                hovertext=hover_labels,
                hoverinfo='text',
                marker=dict(
                    color=colors.get('orange2'),
                ),
                yaxis='y2'
            )
        )

        y_axis_line_nt = [round(float(item.get('percent_fem')) * 100) if item.get('percent_fem') is not None else None
                          for item in data if item.get('ten_stat') == 'NTBOT']
        hover_labels = [f'{i}%' if i is not None else None for i in y_axis_line_nt]
        text_labels = make_text_labels(hover_labels)

        chart_data.append(
            go.Scatter(
                name='% NTBOT Female',
                x=x_axis,
                y=y_axis_line_nt,
                mode='lines+markers+text',
                text=text_labels,
                textposition='top center',
                textfont=dict(
                    color=colors.get('red1'),
                ),
                hovertext=hover_labels,
                hoverinfo='text',
                marker=dict(
                    color=colors.get('red1'),
                ),
                yaxis='y2'
            )
        )

        # URM line calculation
        # (Tenured FTE * Tenured % URM + NTBOT FTE * NTBOT% URM) / (Tenured FTE + NTBOT FTE)

        urm_t = [float(item.get('percent_urm')) if item.get('percent_urm') is not None else None
                 for item in data if item.get('ten_stat') == 'Tenured']

        urm_nt = [float(item.get('percent_urm')) if item.get('percent_urm') is not None else None
                  for item in data if item.get('ten_stat') == 'NTBOT']

        y_axis_line_urm = []

        for t_fte, nt_fte, t_urm, nt_urm in zip(y_axis_bar_t, y_axis_bar_nt, urm_t, urm_nt):
            if t_urm is not None or nt_urm is not None:
                calc = (float(t_fte) * t_urm + float(nt_fte) * nt_urm) / (float(t_fte) + float(nt_fte))
                y_axis_line_urm.append(round(calc * 100))
            else:
                y_axis_line_urm.append(None)

        hover_labels = [f'{i}%' if i is not None else None for i in y_axis_line_urm]
        text_labels = make_text_labels(hover_labels)

        chart_data.append(
            go.Scatter(
                name='% NTBOT and Tenured URM',
                x=x_axis,
                y=y_axis_line_urm,
                mode='lines+markers+text',
                text=text_labels,
                textposition='top center',
                textfont=dict(
                    color=colors.get('teal1'),
                ),
                hovertext=hover_labels,
                hoverinfo='text',
                marker=dict(
                    color=colors.get('teal1'),
                ),
                yaxis='y2'
            )
        )

        chart_layout = go.Layout(
            barmode='stack',
            xaxis=axes(),
            yaxis=axes(
                title='FTE',
            ),
            yaxis2=axes(
                title='% FTE',
                overlaying='y',
                side='right',
                rangemode='tozero',
                showgrid=False,
            ),
            legend={'traceorder': 'normal',
                    'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
            margin=margin(),
        )

        return {'data': chart_data, 'layout': chart_layout}

    # TABLE

    @dashapp.callback(Output('faculty-table', 'data'),
                      [Input('dept-dropdown', 'value')])
    def update_faculty_table(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': f'DATA#FACULTY_LIST#{MAX_FISCAL_YEAR}',
                ':upper': f'DATA#FACULTY_LIST#{MAX_FISCAL_YEAR}$',
            },
            ScanIndexForward=True
        )

        return resp['Items']
