"""
Styling helpers.
axes(): Helper function to create axes configurations for Plotly graph objects.
"""


def axes(
        title='',
        titlefont_family='sans-serif',
        titlefont_size=14,
        titlefont_color='black',
        tickmode='auto',
        ticks='outside',
        tick0=0,
        dtick=1,
        ticklen=0,
        tickwidth=0,
        tickcolor='#000',
        tickformat=',d',
        showticklabels=True,
        tickfont_family='sans-serif',
        tickfont_size=14,
        tickfont_color='black',
        # showline=True,
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
        tickformat=tickformat,
        showticklabels=showticklabels,

        tickfont=dict(
            family=tickfont_family,
            size=tickfont_size,
            color=tickfont_color
        ),
        # showline=showline
    )

    for key, value in kwargs.items():
        axis[key] = value

    return axis


def margin(l=45, t=5, autoexpand=True):
    
    margin = dict(
        l=l,
        t=t,
        autoexpand=autoexpand
    )
    
    return margin
