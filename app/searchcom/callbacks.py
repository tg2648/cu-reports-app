"""
Dash callbacks

Only applicant and posting data depend on the requisition number value
Pipeline and subfield data depend on the posting data

Callback chain:
Requisition number dropdown value changes
-> applicant data and posting data load
---> pipeline and subfield data load
-----> charts and footers load
"""

# Third party imports
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go

from flask import current_app

from boto3.dynamodb.conditions import Key

# Local application imports
from app.extensions import dynamo
from app.searchcom.chart_config.styling import axes
from app.searchcom.chart_config.colors import colors

# Crosstab table outputs
## Category values as they are entered in HTML id fields
gen_cat_html = ['fem', 'male', 'na']
ethn_cat_html = ['amind', 'asian', 'black', 'pacific', 'white', 'na']
hisp_cat_html = ['hisp', 'nonhisp', 'na']

## Build a list of outputs to all combinations of those fields
xtab_output_list = [Output('searchcom-xtab-table', 'style'), Output('searchcom-xtab-threshold-warning', 'style')]
for i in ethn_cat_html:
    for j in hisp_cat_html:
        for k in gen_cat_html:
            xtab_output_list.append(Output(f"{i}-{j}-{k}", 'children'))


# Category values as they are in the xtab data
# The order should be the same as in HTML categories so that the callback output matches the output list (Male-White-Yes matches male-white-hisp, etc.)
gen_cat = ['Female', 'Male', 'Blank']
ethn_cat = ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Native Hawaiian or Other Pacific Islander', 'White', 'Blank']
hisp_cat = ['Yes', 'No', 'Blank']


def register_searchcom_callbacks(dashapp):

    posting_table = dynamo.tables[current_app.config['DB_SEARCHCOM_POSTING']]
    applicant_table = dynamo.tables[current_app.config['DB_SEARCHCOM_APPLICANT']]
    pipeline_table = dynamo.tables[current_app.config['DB_SEARCHCOM_PIPELINE']]
    subfields_table = dynamo.tables[current_app.config['DB_SEARCHCOM_SUBFIELDS']]

    # DATA

    ## POSTING DATA
    @dashapp.callback(Output('searchcom-session-data-posting', 'data'),
                      [Input('req-num-dropdown', 'value')],
                      [State('searchcom-session-data-posting', 'data')])
    def load_posting_data(req_num, posting_data):
        """
        Loads posting data for the selected job requisition number into session data
        """
        if (req_num == '') or (req_num is None):
            raise PreventUpdate

        response = posting_table.query(KeyConditionExpression=Key('req_num').eq(req_num))

        return response['Items'][0]  # DynamoDB query returns a list, since we are querying on a unique requisition number, we need the first and only element of the list

    ## APPLICANT DATA
    @dashapp.callback(Output('searchcom-session-data-applicant', 'data'),
                      [Input('req-num-dropdown', 'value')],
                      [State('searchcom-session-data-applicant', 'data')])
    def load_applicant_data(req_num, applicant_data):
        """
        Loads applicant data for the selected job requisition number into session data
        """
        if (req_num == '') or (req_num is None):
            raise PreventUpdate

        response = applicant_table.query(KeyConditionExpression=Key('req_num').eq(req_num))
        applicant_data = response['Items'][0]

        CHART_THRESHOLD_FAIL = applicant_data['agg']['person_id_count'] < 3
        CROSSTAB_THRESHOLD_FAIL = (applicant_data['agg']['gender_Female_sum'] < 5) or (applicant_data['agg']['gender_Male_sum'] < 5)

        if CHART_THRESHOLD_FAIL:
            applicant_data['agg'] = {}

        if CROSSTAB_THRESHOLD_FAIL:
            applicant_data['xtab'] = {}

        return applicant_data

    ## PIPELINE DATA
    @dashapp.callback(Output('searchcom-session-data-pipeline', 'data'),
                      [Input('searchcom-session-data-posting', 'modified_timestamp')],
                      [State('searchcom-session-data-posting', 'data')])
    def load_pipeline_data(ts, posting_data):
        """
        Loads the pipeline based on the department code of the selected job requisition number
        """
        if (ts is None) or (ts == -1):
            raise PreventUpdate

        dept = posting_data['dept_code']
        response = pipeline_table.query(KeyConditionExpression=Key('Dept').eq(dept))

        return response['Items'][0]

    # LAYOUT
    ## BASIC SEARCH INFO
    @dashapp.callback([Output('search-info-dept', 'children'),
                       Output('search-info-title', 'children'),
                       Output('search-info-open-date', 'children'),
                       Output('search-info-start-date', 'children'),
                       Output('search-info-field', 'children'),
                       Output('search-info-data-refresh', 'children')],
                      [Input('searchcom-session-data-posting', 'modified_timestamp'),
                      Input('searchcom-session-data-applicant', 'modified_timestamp')],
                      [State('searchcom-session-data-posting', 'data'),
                      State('searchcom-session-data-applicant', 'data')])
    def populate_search_info(posting_ts, applicant_ts, posting_data, applicant_data):
        """
        Populates basic search info from the selected job requisition number's posting data
        """
        if (posting_ts is None) or (posting_ts == -1) or (applicant_ts is None) or (applicant_ts == -1):
            raise PreventUpdate

        return posting_data['dept_name'], \
            posting_data['position_title'], \
            posting_data['open_date'], \
            posting_data['start_date'], \
            posting_data['field'], \
            applicant_data['refresh_date']

    ## FOOTER

    @dashapp.callback(Output('searchcom-search-subfields', 'children'),
                      [Input('searchcom-session-data-posting', 'modified_timestamp')],
                      [State('searchcom-session-data-posting', 'data')])
    def populate_footer(ts, posting_data):
        """
        Populates the subfield info based on the department code of the selected job requisition number
        """
        if (ts is None) or (ts == -1):
            raise PreventUpdate

        dept = posting_data['dept_code']
        response = subfields_table.query(KeyConditionExpression=Key('Dept').eq(dept))

        return response['Items'][0]['Subfield']

    ## TABLE

    @dashapp.callback(xtab_output_list,
                      [Input('searchcom-session-data-applicant', 'modified_timestamp')],
                      [State('searchcom-session-data-applicant', 'data')])
    def build_crosstab_table(applicant_ts, applicant_data):
        if (applicant_ts is None) or (applicant_ts == -1):
            raise PreventUpdate

        if applicant_data['xtab']:

            applicant_data_xtab = applicant_data['xtab']

            return_list = [
                {'display': 'inline'},
                {'display': 'none'}
            ]
            # Loop through gender, then hispanic, then ethnicity in order match the output list (Male-White-Yes matches male-white-hisp, etc.)
            for j in ethn_cat:
                for k in hisp_cat:
                    for i in gen_cat:
                        return_value = applicant_data_xtab[i][j][k]
                        if return_value == 0:
                            return_list.append('-')
                        else:
                            return_list.append(return_value)

            return return_list

        else:

            return_list = [
                {'display': 'none'},
                {'display': 'inline'}
            ]

            # Fill with blanks
            for j in ethn_cat:
                for k in hisp_cat:
                    for i in gen_cat:
                        return_list.append('-')

            return return_list

    ## CHARTS

    @dashapp.callback([Output('searchcom-applicant-chart', 'figure'),
                       Output('searchcom-applicant-chart', 'style'),
                       Output('searchcom-chart-threshold-warning', 'style'),
                       Output('searchcom-subfields-footer', 'style')],
                      [Input('searchcom-session-data-applicant', 'modified_timestamp'),
                       Input('searchcom-session-data-pipeline', 'modified_timestamp')],
                      [State('searchcom-session-data-applicant', 'data'),
                       State('searchcom-session-data-pipeline', 'data')])
    def build_applicant_chart(applicant_ts, pipeline_ts, applicant_data, pipeline_data):
        if (applicant_ts is None) or (applicant_ts == -1) or (pipeline_ts is None) or (pipeline_ts == -1):
            raise PreventUpdate

        if applicant_data['agg']:

            applicant_data_agg = applicant_data['agg']
            x_axis = ['Female', 'URM', 'Asian', 'White']

            chart_data = [
                go.Bar(
                    name='Combined availability 1993-2012',
                    x=x_axis,
                    y=[
                        pipeline_data['combined_1993-2012_women'],
                        pipeline_data['combined_1993-2012_urm'],
                        pipeline_data['combined_1993-2012_asian'],
                        pipeline_data['combined_1993-2012_white'],
                    ],
                    text=[
                        str(pipeline_data['combined_1993-2012_women']) + '%',
                        str(pipeline_data['combined_1993-2012_urm']) + '%',
                        str(pipeline_data['combined_1993-2012_asian']) + '%',
                        str(pipeline_data['combined_1993-2012_white']) + '%',
                    ],
                    hoverinfo='text',
                    marker=dict(
                        color=colors.get('blue1'),
                    )
                ),

                go.Bar(
                    name='Tenured availability 1993-2007',
                    x=x_axis,
                    y=[
                        pipeline_data['tenured_1993-2007_women'],
                        pipeline_data['tenured_1993-2007_urm'],
                        pipeline_data['tenured_1993-2007_asian'],
                        pipeline_data['tenured_1993-2007_white'],
                    ],
                    text=[
                        str(pipeline_data['tenured_1993-2007_women']) + '%',
                        str(pipeline_data['tenured_1993-2007_urm']) + '%',
                        str(pipeline_data['tenured_1993-2007_asian']) + '%',
                        str(pipeline_data['tenured_1993-2007_white']) + '%',
                    ],
                    hoverinfo='text',
                    marker=dict(
                        color=colors.get('blue2'),
                    )
                ),

                go.Bar(
                    name='Untenured availability 2008-2012',
                    x=x_axis,
                    y=[
                        pipeline_data['untenured_2008-2012_women'],
                        pipeline_data['untenured_2008-2012_urm'],
                        pipeline_data['untenured_2008-2012_asian'],
                        pipeline_data['untenured_2008-2012_white'],
                    ],
                    text=[
                        str(pipeline_data['untenured_2008-2012_women']) + '%',
                        str(pipeline_data['untenured_2008-2012_urm']) + '%',
                        str(pipeline_data['untenured_2008-2012_asian']) + '%',
                        str(pipeline_data['untenured_2008-2012_white']) + '%',
                    ],
                    hoverinfo='text',
                    marker=dict(
                        color=colors.get('blue3'),
                    )
                ),

                go.Bar(
                    name='Untenured availability 2013-2016',
                    x=x_axis,
                    y=[
                        pipeline_data['untenured_2013-2016_women'],
                        pipeline_data['untenured_2013-2016_urm'],
                        pipeline_data['untenured_2013-2016_asian'],
                        pipeline_data['untenured_2013-2016_white'],
                    ],
                    text=[
                        str(pipeline_data['untenured_2013-2016_women']) + '%',
                        str(pipeline_data['untenured_2013-2016_urm']) + '%',
                        str(pipeline_data['untenured_2013-2016_asian']) + '%',
                        str(pipeline_data['untenured_2013-2016_white']) + '%',
                    ],
                    hoverinfo='text',
                    marker=dict(
                        color=colors.get('blue4'),
                    )
                ),

                go.Bar(
                    name='Applicants',
                    x=x_axis,
                    y=[
                        applicant_data_agg['gender_Female_pcnt'],
                        applicant_data_agg['ethnicity_URM_pcnt'],
                        applicant_data_agg['ethnicity_Asian_pcnt'],
                        applicant_data_agg['ethnicity_White_pcnt'],
                    ],
                    text=[
                        f"{applicant_data_agg['gender_Female_pcnt']}%<br>n={applicant_data_agg['gender_Female_sum']}",
                        f"{applicant_data_agg['ethnicity_URM_pcnt']}%<br>n={applicant_data_agg['ethnicity_URM_sum']}",
                        f"{applicant_data_agg['ethnicity_Asian_pcnt']}%<br>n={applicant_data_agg['ethnicity_Asian_sum']}",
                        f"{applicant_data_agg['ethnicity_White_pcnt']}%<br>n={applicant_data_agg['ethnicity_White_sum']}",
                    ],
                    textposition='outside',
                    hovertext=[
                        f"{applicant_data_agg['gender_Female_pcnt']}% (n={applicant_data_agg['gender_Female_sum']})",
                        f"{applicant_data_agg['ethnicity_URM_pcnt']}% (n={applicant_data_agg['ethnicity_URM_sum']})",
                        f"{applicant_data_agg['ethnicity_Asian_pcnt']}% (n={applicant_data_agg['ethnicity_Asian_sum']})",
                        f"{applicant_data_agg['ethnicity_White_pcnt']}% (n={applicant_data_agg['ethnicity_White_sum']})",
                    ],
                    hoverinfo='text',
                    marker=dict(
                        color=colors.get('orange1'),
                    )
                ),

                # go.Scatter(
                #     name='dept',
                #     x=x_axis,
                #     y=[10, 20, 30, 40],
                #     mode='markers',
                #     marker=dict(
                #         symbol='diamond',
                #         size=8,
                #         color='#D585E9'
                #     )
                # )
            ]

            chart_layout = go.Layout(
                barmode='group',
                xaxis=axes(),
                yaxis=axes(
                    title='%',
                    range=[0, 110]
                )
            )

            return {'data': chart_data, 'layout': chart_layout}, \
                   {'display': 'inline'}, \
                   {'display': 'none'}, \
                   {'display': 'inline'}

        else:

            return {'data': [], 'layout': {}}, \
                   {'display': 'none'}, \
                   {'display': 'inline'}, \
                   {'display': 'none'}

    # NAVBAR

    ## Navbar Collapse Toggle
    @dashapp.callback(Output("navbar-collapse", "is_open"),
                      [Input("navbar-toggler", "n_clicks")],
                      [State("navbar-collapse", "is_open")])
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    ## Button popups
    @dashapp.callback(
        Output("changelog-popup", "is_open"),
        [Input("changelog-popup-button", "n_clicks"), Input("close-changelog", "n_clicks")],
        [State("changelog-popup", "is_open")],
    )
    def toggle_changelog_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dashapp.callback(
        Output("notes-popup", "is_open"),
        [Input("notes-popup-button", "n_clicks"), Input("close-notes", "n_clicks")],
        [State("notes-popup", "is_open")],
    )
    def toggle_notes_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @dashapp.callback(
        Output("contact-popup", "is_open"),
        [Input("contact-popup-button", "n_clicks"), Input("close-contact", "n_clicks")],
        [State("contact-popup", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    # # TOASTS
    # @dashapp.callback([Output("changelog-popup", "is_open"),
    #                    Output("notes-popup", "is_open")],
    #                  [Input("changelog-popup-button", "n_clicks"),
    #                  Input("notes-popup-button", "n_clicks")],
    #                  [State("changelog-popup", "is_open"),
    #                  State("notes-popup", "is_open")])
    # def open_toast(n_changelog, n_notes, state_changelog, state_notes):
    #     # "How do I determine which Input has changed?"
    #     # https://dash.plot.ly/faqs
    #     ctx = dash.callback_context

    #     if n_changelog or n_notes:
    #         # Determine which button was triggered last
    #         triggered_button = ctx.triggered[0]['prop_id'].split('.')[0]
    #         if triggered_button == 'changelog-popup-button': # If changelog is pressed
    #             return [not state_changelog, False] # Flip state of changelog and close notes
    #         elif triggered_button == 'notes-popup-button':
    #             return [False, not state_notes]
    #     else:
    #         return [False, False]
