#!/usr/bin/env python3

import logging
import click
import json
import numpy as np

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
@click.option('-o', '--save_output', type=click.Path(), 
    help='Save output to file.'
)
@click.option('-p', '--plot', is_flag=True, 
    help='Plot altitude after simulating.'
)
def sim(config_file, save_output, plot):
    sim_config = json.load(config_file)
    t, h, v, a = simulation.run(sim_config)
    if save_output:
        # vertical stack single rows then transpose so they are columns
        output_array = np.vstack([t, h, v, a]).T
        np.savetxt(
            save_output, output_array, fmt='%.6f', delimiter=',', newline='\n',
            header='time,altitude,ascent_rate,ascent_accel', footer='', comments='# ', encoding=None
        )
    if plot:
        import plot_tools
        traces = [plot_tools.create_plot_trace(t, h)]
        plot_tools.plot_traces(traces, xlabel='Time (s)', ylabel='Altitude (m)')


cli.add_command(sim)

if __name__ == '__main__':
    cli()
