import logging
import plotly
import plotly.graph_objects as go


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


def plot_traces(traces, xlabel='', ylabel='', title='', showlegend=False):
    layout = {
        'title': title,
        'showlegend': showlegend,
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'xaxis': {'showgrid': True, 'title': xlabel},
        'yaxis': {'showgrid': True, 'title': ylabel}
    }
    plotly.offline.iplot({
        'data': traces,
        'layout': layout
    })
