"""
Helper chart-related functions
"""


def make_text_labels(hover_labels):
    """
    Take hover lables and remove all except the first and the last label (excluding None)
    Turns [None, None, 30%, 29%, 28%, 34%] into [None, None, '30%', None, None, '34%']
    """
    text_labels = [None] * len(hover_labels)

    i = 0
    while hover_labels[i] is None:
        i += 1

    text_labels[i] = hover_labels[i]
    text_labels[-1] = hover_labels[-1]

    return text_labels
