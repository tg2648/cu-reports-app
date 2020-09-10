"""
1. To convert S3 keys to user-friendly values
2. To convert fiscal years to academic years
"""

checkbox_conversion = {
    'faculty_meeting_minutes': 'Faculty Meetings',
}

heading_conversion = {
    'EPPC': 'Educational Policy and Planning Committee',
    'PPC': 'Policy and Planning Committee',
    'CED': 'Committee on Equity and Diversity',
    'faculty_meeting_minutes': 'Faculty Meetings',
}


def convert_for_checkbox(old):
    """
    If present in the dictionary, return converted value. Otherwise return unchanged.
    """
    if old in checkbox_conversion:
        return checkbox_conversion[old]
    else:
        return old


def convert_for_heading(old):
    """
    If present in the dictionary, return converted value. Otherwise return unchanged.
    """
    pass
    if old in heading_conversion:
        return heading_conversion[old]
    else:
        return old


def fiscal_to_academic(fiscal):
    """
    Converts fiscal year to academic year. Returns a string.
    """
    fiscal_int = int(fiscal)
    fiscal_str = str(fiscal)

    return f'{fiscal_int - 1}/{fiscal_str[-2:]}'
