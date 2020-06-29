"""
Styling helpers.

axes(): Helper function to create axes configurations for Plotly graph objects.
Default values are set, and anything else can be set as kwargs
"""


def axes(
    title='',
    titlefont_family='sans-serif',
    titlefont_size=18,
    titlefont_color='grey',
    tickmode='auto',
    ticks='outside',
    tick0=0,
    dtick=1,
    ticklen=0,
    tickwidth=0,
    tickcolor='#000',
    showticklabels=True,
    tickfont_family='sans-serif',
    tickfont_size=14,
    tickfont_color='black',
    **kwargs
):

    axis = dict(
        title=title,

        titlefont=dict(
            family=titlefont_family,
            size=titlefont_size,
            color=titlefont_color
        ),

        tickmode=tickmode,
        ticks=ticks,
        tick0=tick0,
        dtick=dtick,
        ticklen=ticklen,
        tickwidth=tickwidth,
        tickcolor=tickcolor,
        showticklabels=showticklabels,

        tickfont=dict(
            family=tickfont_family,
            size=tickfont_size,
            color=tickfont_color
        )
    )

    for key, value in kwargs.items():
        axis[key] = value

    return axis
