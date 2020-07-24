"""
Dash callbacks
"""

# Standard library imports
from collections import defaultdict

# Third party imports
import dash_html_components as html
from flask import url_for


class CommitteeFiles(object):
    """Helper class to organize committee files.

    Accepts a Dynamo query output and produces an organized HTML div element with a list of links
    via the `file_list` method.

    Attributes:
        by_committee (dict[dict[list]]): Items grouped by committee
        by_year (dict[dict[list]]): Items grouped by year
    """

    def __init__(self, items):
        """
        Args:
            items (list[dict]): List of Dynamo items.
        """

        self.by_committee = self.group(items, by='committee')
        self.by_year = self.group(items, by='year')

    def group(self, items, by=None):
        """
        Dynamo items are of the form:
        {'PK': 'PPC', 'year': '2020', 'file_name': 'abc.pdf', 'key': 'PPC/abc.pdf', ... }

        Grouping by committee produces:

        "PPC": {
                "2019": [html.Li(html.A(...)),
                         html.Li(html.A(...))],
                "2019": [...],
                "2018": [...],
            }

        Grouping by year is similar but with swapped dictionary keys.

        Args:
            by (str): How to group items

        Returns:
            dict[dict[list]]: Items grouped by the indicated metric
        """

        d = defaultdict(lambda: defaultdict(lambda: []))

        if by == 'committee':

            for item in items:
                committee = item['PK']
                year = item['year']
                d[committee][year].append(self.make_list_item(item))

        elif by == 'year':

            for item in items:
                committee = item['PK']
                year = item['year']
                d[year][committee].append(self.make_list_item(item))

        return d

    def make_list_item(self, item):
        return html.Li(self.make_link(item), className='ml-4')

    def make_link(self, item):
        return html.A(item['file_name'], href=url_for('repository.download', key=item['key']), target='blank')

    def file_list(self, groupby):
        """
        Converts this:

            "PPC": {
                    "2019": [html.Li(html.A(...)),
                            html.Li(html.A(...))],
                    "2019": [...],
                    "2018": [...],
                }

        Into this:

            Div([
                P('PPC'),
                Ul(
                    [
                        Span('2019'),
                        Li(A(...)),
                        Span('2018'),
                        Li(A(...)),
                    ]
            ])

        Args:
            groupby (str): Which grouping to use

        Returns:
            dash_html_components.html.Div
        """

        if groupby == 'committee':
            d = self.by_committee
        elif groupby == 'year':
            d = self.by_year

        list_div = html.Div([])

        for cat_name, cat in d.items():
            list_div.children.append(html.P(html.U(cat_name), className='text-info'))
            ul = html.Ul([], className='pl-0')

            for subcat_name, subcat in cat.items():
                ul.children.append(html.Span(subcat_name))

                for item in subcat:
                    ul.children.append(item)

            list_div.children.append(ul)

        return list_div
