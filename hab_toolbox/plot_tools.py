import logging
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = go.Figure(
    layout = {
        'showlegend': True,
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    }
)
templated_fig = plotly.io.to_templated(fig)
plotly.io.templates['my_template'] = templated_fig.layout.template
plotly.io.templates.default = 'my_template'


def create_plot_trace(x, y, label=''):
    return go.Scatter(
        x=x,
        y=y,
        name=label,
        opacity=0.8,
        mode='lines+markers',
        marker={
            'size': 0.5,
        }
    )


def create_fig_with_traces(traces, xlabel='', ylabel='', title='', showlegend=False):
    ''' Plot all traces on the same axes.
    '''
    layout = {
        'title': title,
        'showlegend': showlegend,
        'xaxis': {'title': xlabel},
        'yaxis': {'title': ylabel}
    }
    plotly.offline.iplot({
        'data': traces,
        'layout': layout
    })


def create_fig_with_subplots(traces):
    ''' Plot each trace on new axes, stacked vertically.
    '''
    fig = plotly.subplots.make_subplots(rows=len(traces), cols=1)
    for i, trace in enumerate(traces):
        fig.add_trace(trace, row=i+1, col=1)
    plotly.offline.iplot(fig)