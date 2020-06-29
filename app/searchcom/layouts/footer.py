"""
Layout: Footer of the dashboard
"""

# Third party imports
import dash_html_components as html


subfields = html.Div(
    [
        html.Span('Subfields of SED data used for this department: '),
        html.Span(id='searchcom-search-subfields')
    ],
    id='searchcom-subfields-footer',
    className='mt-3 text-muted'
)
