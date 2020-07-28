#!/usr/bin/env python3

import logging
import click
import json

from ascent_model import simulation


FORMAT = '%(asctime)-15s %(levelname)+8s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z")
log = logging.getLogger()


@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
def cli(verbose, debug):
    if debug:
        log.setLevel(logging.DEBUG)
    elif verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)


@cli.command()
@click.argument('config_file', type=click.File('rb'))
@click.option('-p', '--plot', is_flag=True, 
    help='Plot altitude after simulating.'
)
def sim(config_file, plot):
    sim_config = json.load(config_file)
    t, x, v, a = simulation.run(sim_config)
    if plot:
        import plot_tools
        traces = [plot_tools.create_plot_trace(t, x)]
        plot_tools.plot_traces(traces, xlabel='Time (s)', ylabel='Altitude (m)')


cli.add_command(sim)

if __name__ == '__main__':
    cli()
