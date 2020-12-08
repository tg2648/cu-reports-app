"""
Dash callbacks
"""

# Standard library imports
from collections import defaultdict

# Third party imports
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import url_for

# Local application imports
from app.utils.func import multisort
from app.facgov.conversions import convert_for_heading
from app.facgov.conversions import fiscal_to_academic


class Facgov(object):
    """
    Methods used by all Facgov classes
    """
    def make_list_item(self, item):
        return html.Li(self.make_link(item), className='ml-4')

    def make_link(self, item):
        return html.A(
            item['file_name'],
            href=url_for('facgov.download', key=item['key']),
            target='blank',
            className='facgov-link'
        )


class FacgovGeneral(Facgov):
    """To organize general faculty governance files.

    Attributes:
        by_year (dict[dict[list]]): Items grouped by year
    """

    def __init__(self, items):
        """
        Args:
            items (list[dict]): List of Dynamo items.
        """
        self.by_year = self.group_by_year(items)

    def group_by_year(self, items):
        """
        Dynamo items are of the form:
        {'unit': 'PPC', 'year': '2020', 'file_name': 'abc.pdf', 'key': 'PPC/abc.pdf', ... }

        Grouping by year produces:

        {
            "Unit": {
                "2019/20": [{'key': ..., 'file_name': ...},
                            {'key': ..., 'file_name': ...}],
                "2018/19": [...],
                }
        }

        Key and file_name are required to build the A tag later on.

        Returns:
            dict[list[dict]]: Items grouped by year
        """

        # Sort descending by year, ascending by file name
        items = multisort(items, (('year', True), ('file_name', False)))

        d = defaultdict(lambda: defaultdict(lambda: []))

        for item in items:
            unit = convert_for_heading(item['unit'])
            year = fiscal_to_academic(item['year'])
            d[unit][year].append({'file_name': item['file_name'], 'key': item['key']})

        return d

    def file_list(self):
        """
        Converts grouped items into an HTML structure. The structure is a Div with a series of Rows.
        Each Rows contains two Cols.

        Returns:
            dash_html_components.html.Div
        """

        list_div = html.Div([])

        for cat_name, cat in self.by_year.items():
            list_div.children.append(html.P(cat_name, className='text-info font-weight-bold'))

            for subcat_name, subcat in cat.items():
                row = html.Div([], className='row')  # Create a row for each subcategory
                col = html.Div(subcat_name, className='col-sm-auto')  # First column is the name of the subcategory
                row.children.append(col)

                ul = html.Ul([], className='pl-0')  # Second column is the list of items
                for item in subcat:
                    ul.children.append(self.make_list_item(item))

                col = html.Div(ul, className='col')
                row.children.append(col)

                list_div.children.append(row)

        return list_div


class FacgovFacultyMeeting(Facgov):
    """Helper class to organize faculty meeting files.

    Attributes:
        by_year (dict[dict[list]]): Items grouped by year
    """

    def __init__(self, items):
        """
        Args:
            items (list[dict]): List of Dynamo items.
        """
        self.by_year = self.group_by_year(items)

    def group_by_year(self, items):
        """
        Dynamo items are of the form:
        {'unit': 'PPC', 'year': '2020', 'file_name': 'abc.pdf', 'key': 'faculty_meeting/abc.pdf', ... }

        Grouping by year produces:

        {
            'Faculty Meetings': {
                '2019/20': {
                    '2019-10-17': {
                        'minutes': {
                            'key':
                            'file_name':
                        }
                        'agenda': {
                            'key':
                            'file_name':
                        }
                    }
                }
            }
        }

        Returns:
            dict[list[dict]]: Items grouped by year
        """

        # Sort descending by year, ascending by file name
        items = multisort(items, (('year', True), ('file_name', False)))

        d = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))

        for item in items:
            unit = convert_for_heading(item['unit'])
            year = fiscal_to_academic(item['year'])

            name_parts = item['file_name'].split(' ')
            date = name_parts[-1]
            category = name_parts[-2]  # agenda or minutes

            d[unit][year][date][category.lower()]['file_name'] = category
            d[unit][year][date][category.lower()]['key'] = item['key']

        return d

    def file_list(self):
        """
        Converts grouped items into an HTML structure. The structure is a Div with a series of Rows.
        Each Rows contains two Cols.

        Returns:
            dash_html_components.html.Div
        """

        list_div = html.Div([])

        for unit_name, unit_data in self.by_year.items():
            list_div.children.append(html.P(unit_name, className='text-info font-weight-bold'))

            for year_name, year_data in unit_data.items():
                row = html.Div([], className='row')  # Create a row for each year
                col = html.Div(year_name, className='col-sm-auto')  # First column is the name of the year
                row.children.append(col)

                ul = html.Ul([], className='pl-0')  # Second column is the list of items
                for meeting_date, meeting_meta in year_data.items():  # Go through each meeting

                    links = html.Span([])
                    if ('agenda' in meeting_meta) and ('minutes' in meeting_meta):
                        links.children.append(self.make_link(meeting_meta['agenda']))
                        links.children.append(' / ')
                        links.children.append(self.make_link(meeting_meta['minutes']))
                    elif ('agenda' in meeting_meta):
                        links.children.append(self.make_link(meeting_meta['agenda']))
                    elif ('minutes' in meeting_meta):
                        links.children.append(self.make_link(meeting_meta['minutes']))

                    list_item = html.Li(
                        [
                            'Faculty Meeting ',
                            meeting_date,
                            ' (',
                            links,
                            ')'
                        ],
                        className='ml-4'
                    )

                    ul.children.insert(0, list_item)  # Insert at front to display in descending order

                col = html.Div(ul, className='col')
                row.children.append(col)

                list_div.children.append(row)

        disclaimer = dbc.Alert('Minutes will be made available whenever possible', color='info')
        return html.Div([disclaimer, list_div])
