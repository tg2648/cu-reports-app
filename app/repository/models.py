"""
Dash callbacks
"""

# Standard library imports
from collections import defaultdict

# Third party imports
import dash_html_components as html
from flask import url_for

# Local application imports
from app.utils.func import multisort
from app.repository.conversions import convert_for_heading
from app.repository.conversions import fiscal_to_academic


class CommitteeFiles(object):
    """Helper class to organize committee files.

    Accepts a Dynamo query output and produces an organized HTML div element with a list of links
    via the `file_list` method.

    Attributes:
        by_committee (dict[dict[list]]): Items grouped by committee
    """

    def __init__(self, items):
        """
        Args:
            items (list[dict]): List of Dynamo items.
        """

        self.by_committee = self.group(items)

    def group(self, items):
        """
        Dynamo items are of the form:
        {'key': 'PPC', 'year': '2020', 'file_name': 'abc.pdf', 'key': 'PPC/abc.pdf', ... }

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

        # First sort by committee, then by year, then by file name
        items = multisort(items, (('unit', True), ('year', True), ('file_name', False)))

        d = defaultdict(lambda: defaultdict(lambda: []))

        for item in items:
            unit = convert_for_heading(item['unit'])
            year = fiscal_to_academic(item['year'])
            d[unit][year].append(self.make_list_item(item))

        return d

    def make_list_item(self, item):
        return html.Li(self.make_link(item), className='ml-4')

    def make_link(self, item):
        return html.A(
            item['file_name'],
            href=url_for('repository.download', key=item['key']),
            target='blank',
            className='facgov-link'
        )

    def file_list(self):
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

        Returns:
            dash_html_components.html.Div
        """

        list_div = html.Div([])

        for cat_name, cat in self.by_committee.items():
            list_div.children.append(html.P(cat_name, className='text-info font-weight-bold'))

            for subcat_name, subcat in cat.items():
                row = html.Div([], className='row')  # Create a row for each subcategory
                col = html.Div(html.U(subcat_name), className='col-sm-auto')  # First column is the name of the subcategory
                row.children.append(col)

                ul = html.Ul([], className='pl-0')  # Second column is the list of items
                for item in subcat:
                    ul.children.append(item)

                col = html.Div(ul, className='col')
                row.children.append(col)

                list_div.children.append(row)

        return list_div
