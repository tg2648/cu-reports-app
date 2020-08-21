"""
To convert S3 keys to user-friendly values
"""

checkbox_conversion = {
    'faculty_meeting_minutes': 'Minutes',
}

heading_conversion = {
    'EPPC': 'Educational Policy and Planning Committee',
    'PPC': 'Policy and Planning Committee',
    'faculty_meeting_minutes': 'Faculty Meeting Minutes',
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
