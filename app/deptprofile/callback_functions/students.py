"""
Students tab callacks
"""

# Third party imports
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from flask import current_app

# Local application imports
from app.extensions import dynamo

from app.deptprofile.utils.styling import axes, margin
from app.deptprofile.utils.colors import students_ug_colors, students_grad_colors
from app.deptprofile.utils.years import MAX_YEAR_ID, MAX_FISCAL_YEAR, make_academic_year_range
from app.deptprofile.utils.charts import make_text_labels


def is_blank_grad(data):
    """
    Returns True if all year records are zero.
    {
        'year': '2005',
        'existing': '0',
        'cohort': '0'
    }
    """

    for year in data:
        if (year['existing'] != '0' or year['cohort'] != '0'):
            return False

    return True


def register_students_callbacks(dashapp):

    table = dynamo.tables[current_app.config['DB_DEPTPROFILE']]

    #################
    # UNDERGRADUATE #
    #################

    @dashapp.callback(Output('students-ug-chart', 'figure'),
                      [Input('dept-dropdown', 'value')])
    def update_student_ug_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#STUDENTS#UG#2005',
                ':upper': f'DATA#STUDENTS#UG#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ScanIndexForward=True,
        )

        data = resp['Items']

        chart_data = []
        x_axis = make_academic_year_range(0, MAX_YEAR_ID)

        # Categories determine filtering for the y-axis and obtaining a color
        categories = {
            'maj': 'Majors',
            'conc': 'Concentrations',
            'intdmaj': 'Interdepartmental Majors',
            'min': 'Minors'
        }

        for cat in categories.keys():

            y_axis = [item.get(cat) for item in data]

            chart_data.append(
                go.Bar(
                    name=categories.get(cat),
                    x=x_axis,
                    y=y_axis,
                    text=[i if len(i) > 1 else f' {i} ' for i in y_axis],  # pad single-digit numbers to prevent rotation
                    textposition='inside',
                    hovertext=[f'{categories.get(cat)}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=students_ug_colors.get(cat),
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
                title='Number of Students',
            ),
            legend={'traceorder': 'normal'},
            margin=margin(l=55),
        )

        return {'data': chart_data, 'layout': chart_layout}

    @dashapp.callback([Output('students-masters-chart', 'figure'),
                       Output('students-masters-container', 'style')],
                      [Input('dept-dropdown', 'value')])
    def update_student_masters_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#STUDENTS#MASTERS#2005',
                ':upper': f'DATA#STUDENTS#MASTERS#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ScanIndexForward=True,
        )

        data = resp['Items']

        if is_blank_grad(data):
            return [], {'display': 'none'}

        chart_data = []
        x_axis = make_academic_year_range(0, MAX_YEAR_ID)

        # Categories determine filtering for the y-axis and obtaining a color
        categories = {
            'cohort': 'Entering Cohort<br>(starting 2009/10)',
            'existing': 'Existing Students',
        }

        for cat in categories.keys():

            y_axis = [item.get(cat) for item in data]

            chart_data.append(
                go.Bar(
                    name=categories.get(cat),
                    x=x_axis,
                    y=y_axis,
                    text=[i if len(i) > 1 else f' {i} ' for i in y_axis],  # pad single-digit numbers to prevent rotation
                    textposition='inside',
                    hovertext=[f'{categories.get(cat)}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=students_grad_colors.get(cat),
                        line=dict(
                            color='floralwhite',
                            width=1
                        ),
                    )
                )
            )

        if dept not in ['AS', 'HUM', 'NS', 'SS']:
            # Do not add selectivity/yield for aggregates
            for cat in ('selectivity', 'yield'):

                y_axis_selectivity = [round(float(item.get(cat)) * 100) if item.get(cat) is not None
                                      else None for item in data]
                hover_labels = [f'{i}%' if i is not None else None for i in y_axis_selectivity]
                text_labels = make_text_labels(hover_labels)

                chart_data.append(
                    go.Scatter(
                        name=f'{cat.title()}',
                        x=x_axis,
                        y=y_axis_selectivity,
                        mode='lines+markers+text',
                        text=text_labels,
                        textposition='top center',
                        textfont=dict(
                            color=students_grad_colors.get(cat),
                        ),
                        hovertext=hover_labels,
                        hoverinfo='text',
                        marker=dict(
                            color=students_grad_colors.get(cat),
                        ),
                        yaxis='y2'
                    )
                )

            chart_layout = go.Layout(
                barmode='stack',
                xaxis=axes(),
                yaxis=axes(
                    title='Number of Students',
                ),
                yaxis2=axes(
                    title='% Selectivity or Yield',
                    overlaying='y',
                    side='right',
                    rangemode='tozero',
                    showgrid=False,
                ),
                legend={'traceorder': 'normal',
                        'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
                margin=margin(l=55),
            )

        else:

            chart_layout = go.Layout(
                barmode='stack',
                xaxis=axes(),
                yaxis=axes(
                    title='Number of Students',
                ),
                legend={'traceorder': 'normal',
                        'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
                margin=margin(l=55),
            )

        return {'data': chart_data, 'layout': chart_layout}, {'display': 'inline'}

    @dashapp.callback([Output('students-interdept-chart', 'figure'),
                       Output('students-interdept-container', 'style')],
                      [Input('dept-dropdown', 'value')])
    def update_student_interdept_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#STUDENTS#INTDMASTERS#2005',
                ':upper': f'DATA#STUDENTS#INTDMASTERS#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ScanIndexForward=True,
        )

        data = resp['Items']

        if is_blank_grad(data):
            return [], {'display': 'none'}

        chart_data = []
        x_axis = make_academic_year_range(0, MAX_YEAR_ID)

        # Categories determine filtering for the y-axis and obtaining a color
        categories = {
            'cohort': 'Entering Cohort<br>(starting 2009/10)',
            'existing': 'Existing Students',
        }

        for cat in categories.keys():

            y_axis = [item.get(cat) for item in data]

            chart_data.append(
                go.Bar(
                    name=categories.get(cat),
                    x=x_axis,
                    y=y_axis,
                    text=[i if len(i) > 1 else f' {i} ' for i in y_axis],  # pad single-digit numbers to prevent rotation
                    textposition='inside',
                    hovertext=[f'{categories.get(cat)}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=students_grad_colors.get(cat),
                        line=dict(
                            color='floralwhite',
                            width=1
                        ),
                    )
                )
            )

        if dept not in ['AS', 'HUM', 'NS', 'SS']:
            # Do not add selectivity/yield for aggregates
            for cat in ('selectivity', 'yield'):

                y_axis_selectivity = [round(float(item.get(cat)) * 100) if item.get(cat) is not None
                                      else None for item in data]
                hover_labels = [f'{i}%' if i is not None else None for i in y_axis_selectivity]
                text_labels = make_text_labels(hover_labels)

                chart_data.append(
                    go.Scatter(
                        name=f'{cat.title()}',
                        x=x_axis,
                        y=y_axis_selectivity,
                        mode='lines+markers+text',
                        text=text_labels,
                        textposition='top center',
                        textfont=dict(
                            color=students_grad_colors.get(cat),
                        ),
                        hovertext=hover_labels,
                        hoverinfo='text',
                        marker=dict(
                            color=students_grad_colors.get(cat),
                        ),
                        yaxis='y2'
                    )
                )

            chart_layout = go.Layout(
                barmode='stack',
                xaxis=axes(),
                yaxis=axes(
                    title='Number of Students',
                ),
                yaxis2=axes(
                    title='% Selectivity or Yield',
                    overlaying='y',
                    side='right',
                    rangemode='tozero',
                    showgrid=False,
                ),
                legend={'traceorder': 'normal',
                        'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
                margin=margin(l=55),
            )

        else:

            chart_layout = go.Layout(
                barmode='stack',
                xaxis=axes(),
                yaxis=axes(
                    title='Number of Students',
                ),
                legend={'traceorder': 'normal',
                        'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
                margin=margin(l=55),
            )

        return {'data': chart_data, 'layout': chart_layout}, {'display': 'inline'}

    @dashapp.callback([Output('students-hybrid-chart', 'figure'),
                       Output('students-hybrid-container', 'style')],
                      [Input('dept-dropdown', 'value')])
    def update_student_hybrid_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#STUDENTS#HYBRIDMASTERS#2005',
                ':upper': f'DATA#STUDENTS#HYBRIDMASTERS#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ScanIndexForward=True,
        )

        data = resp['Items']

        if is_blank_grad(data):
            return [], {'display': 'none'}

        chart_data = []
        x_axis = make_academic_year_range(0, MAX_YEAR_ID)

        # Categories determine filtering for the y-axis and obtaining a color
        categories = {
            'cohort': 'Entering Cohort<br>(starting 2009/10)',
            'existing': 'Existing Students',
        }

        for cat in categories.keys():

            y_axis = [item.get(cat) for item in data]

            chart_data.append(
                go.Bar(
                    name=categories.get(cat),
                    x=x_axis,
                    y=y_axis,
                    text=[i if len(i) > 1 else f' {i} ' for i in y_axis],  # pad single-digit numbers to prevent rotation
                    textposition='inside',
                    hovertext=[f'{categories.get(cat)}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=students_grad_colors.get(cat),
                        line=dict(
                            color='floralwhite',
                            width=1
                        ),
                    )
                )
            )

        if dept not in ['AS', 'HUM', 'NS', 'SS']:
            # Do not add selectivity/yield for aggregates
            for cat in ('selectivity', 'yield'):

                y_axis_selectivity = [round(float(item.get(cat)) * 100) if item.get(cat) is not None
                                      else None for item in data]
                hover_labels = [f'{i}%' if i is not None else None for i in y_axis_selectivity]
                text_labels = make_text_labels(hover_labels)

                chart_data.append(
                    go.Scatter(
                        name=f'{cat.title()}',
                        x=x_axis,
                        y=y_axis_selectivity,
                        mode='lines+markers+text',
                        text=text_labels,
                        textposition='top center',
                        textfont=dict(
                            color=students_grad_colors.get(cat),
                        ),
                        hovertext=hover_labels,
                        hoverinfo='text',
                        marker=dict(
                            color=students_grad_colors.get(cat),
                        ),
                        yaxis='y2'
                    )
                )

            chart_layout = go.Layout(
                barmode='stack',
                xaxis=axes(),
                yaxis=axes(
                    title='Number of Students',
                ),
                yaxis2=axes(
                    title='% Selectivity or Yield',
                    overlaying='y',
                    side='right',
                    rangemode='tozero',
                    showgrid=False,
                ),
                legend={'traceorder': 'normal',
                        'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
                margin=margin(l=55),
            )

        else:

            chart_layout = go.Layout(
                barmode='stack',
                xaxis=axes(),
                yaxis=axes(
                    title='Number of Students',
                ),
                legend={'traceorder': 'normal',
                        'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
                margin=margin(l=55),
            )

        return {'data': chart_data, 'layout': chart_layout}, {'display': 'inline'}

    @dashapp.callback([Output('students-sps-chart', 'figure'),
                       Output('students-sps-container', 'style')],
                      [Input('dept-dropdown', 'value')])
    def update_student_sps_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#STUDENTS#SPS#2005',
                ':upper': f'DATA#STUDENTS#SPS#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ScanIndexForward=True,
        )

        data = resp['Items']

        if is_blank_grad(data):
            return [], {'display': 'none'}

        chart_data = []
        x_axis = make_academic_year_range(0, MAX_YEAR_ID)

        # Categories determine filtering for the y-axis and obtaining a color
        categories = {
            'cohort': 'Entering Cohort<br>(starting 2009/10)',
            'existing': 'Existing Students',
        }

        for cat in categories.keys():

            y_axis = [item.get(cat) for item in data]

            chart_data.append(
                go.Bar(
                    name=categories.get(cat),
                    x=x_axis,
                    y=y_axis,
                    text=[i if len(i) > 1 else f' {i} ' for i in y_axis],  # pad single-digit numbers to prevent rotation
                    textposition='inside',
                    hovertext=[f'{categories.get(cat)}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=students_grad_colors.get(cat),
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
                title='Number of Students',
            ),
            legend={'traceorder': 'normal',
                    'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
            margin=margin(l=55),
        )

        return {'data': chart_data, 'layout': chart_layout}, {'display': 'inline'}

    @dashapp.callback([Output('students-phd-chart', 'figure'),
                       Output('students-phd-container', 'style')],
                      [Input('dept-dropdown', 'value')])
    def update_student_phd_chart(dept):

        resp = table.query(
            KeyConditionExpression='PK = :pk AND SK BETWEEN :lower AND :upper',
            ExpressionAttributeValues={
                ':pk': f'DEPT#{dept}',
                ':lower': 'DATA#STUDENTS#PHD#2005',
                ':upper': f'DATA#STUDENTS#PHD#{int(MAX_FISCAL_YEAR) + 1}$',
            },
            ScanIndexForward=True,
        )

        data = resp['Items']

        if is_blank_grad(data):
            return [], {'display': 'none'}

        chart_data = []
        x_axis = make_academic_year_range(0, MAX_YEAR_ID)

        # Categories determine filtering for the y-axis and obtaining a color
        categories = {
            'cohort': 'Entering Cohort<br>(starting 2009/10)',
            'existing': 'Existing Students',
        }

        for cat in categories.keys():

            y_axis = [item.get(cat) for item in data]

            chart_data.append(
                go.Bar(
                    name=categories.get(cat),
                    x=x_axis,
                    y=y_axis,
                    text=[i if len(i) > 1 else f' {i} ' for i in y_axis],  # pad single-digit numbers to prevent rotation
                    textposition='inside',
                    hovertext=[f'{categories.get(cat)}: {i}' for i in y_axis],
                    hoverinfo='text',
                    marker=dict(
                        color=students_grad_colors.get(cat),
                        line=dict(
                            color='floralwhite',
                            width=1
                        ),
                    )
                )
            )

        if dept not in ['AS', 'HUM', 'NS', 'SS']:
            # Do not add selectivity/yield for aggregates
            for cat in ('selectivity', 'yield'):

                y_axis_selectivity = [round(float(item.get(cat)) * 100) if item.get(cat) is not None
                                      else None for item in data]
                hover_labels = [f'{i}%' if i is not None else None for i in y_axis_selectivity]
                text_labels = make_text_labels(hover_labels)

                chart_data.append(
                    go.Scatter(
                        name=f'{cat.title()}',
                        x=x_axis,
                        y=y_axis_selectivity,
                        mode='lines+markers+text',
                        text=text_labels,
                        textposition='top center',
                        textfont=dict(
                            color=students_grad_colors.get(cat),
                        ),
                        hovertext=hover_labels,
                        hoverinfo='text',
                        marker=dict(
                            color=students_grad_colors.get(cat),
                        ),
                        yaxis='y2'
                    )
                )

            chart_layout = go.Layout(
                barmode='stack',
                xaxis=axes(),
                yaxis=axes(
                    title='Number of Students',
                ),
                yaxis2=axes(
                    title='% Selectivity or Yield',
                    overlaying='y',
                    side='right',
                    rangemode='tozero',
                    showgrid=False,
                ),
                legend={'traceorder': 'normal',
                        'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
                margin=margin(l=55),
            )

        else:

            chart_layout = go.Layout(
                barmode='stack',
                xaxis=axes(),
                yaxis=axes(
                    title='Number of Students',
                ),
                legend={'traceorder': 'normal',
                        'x': 1.05},  # By default x is 1.02 which will make it overlap with the 2nd y-axis
                margin=margin(l=55),
            )

        return {'data': chart_data, 'layout': chart_layout}, {'display': 'inline'}
