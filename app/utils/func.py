"""
Utility functions
"""

# Standard library imports
from operator import itemgetter


def multisort(data, specs):
    """
    https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts

    Args:
        data (list[dict])
        specs (Tuple[Tuple]): Each tuple consists of
            0: Attribute to sort by
            1: True for a descending sort

    Returns:
        Sorted list[dict]
    """
    for key, reverse in reversed(specs):
        data.sort(key=itemgetter(key), reverse=reverse)

    return data
