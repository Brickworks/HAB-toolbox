import logging
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = go.Figure(
    layout = {
        'showlegend': True,
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis': {'showgrid': True, 'gridcolor': 'LightGray'},
        'yaxis': {'showgrid': True, 'gridcolor': 'LightGray'}
    }
)
templated_fig = plotly.io.to_templated(fig)
plotly.io.templates['my_template'] = templated_fig.layout.template
plotly.io.templates.default = 'my_template'
plotly.io.rederers.default = 'browser'


def create_plot_trace(x, y, label=''):
    return go.Scatter(
        x=x,
        y=y,
        name=label,
        opacity=0.8,
        mode='lines+markers',
        marker={
            'size': 0.5,
            'opacity': 0.5,
            'line': {'color': 'DarkSlateGrey'},
        }
    )


def create_figure(traces, xlabel='', ylabel='', title='', showlegend=False):
    ''' Plot all traces on the same axes.
    '''
    layout = {
        'title': title,
        'showlegend': showlegend,
        'xaxis': {'title': xlabel},
        'yaxis': {'title': ylabel}
    }
    return go.Figure({
        'data': traces,
        'layout': layout
    })


def create_subplots(traces, rows, cols):
    ''' Create subplots from plot traces.
    traces = {
        'trace': create_plot_trace(blah),
        'row': row_index,
        'col': col_index
    }
    '''
    fig = make_subplots(rows=rows, cols=cols)
    for trace in traces:
        fig.add_trace(trace['trace'], row=trace['row'], col=trace['col'])
    return fig


def plot_figure(fig, renderer='browser'):
    fig.show(renderer=renderer)
