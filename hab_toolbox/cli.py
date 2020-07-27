#!/usr/bin/env python3

import logging
import click

import utils
import test_ascent


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
def test_logger():
    # test the current logging level
    utils.test_logger()


@cli.command()
@click.option('-d', '--duration', default=3000, show_default=True,
    help='Duration of the simulation (seconds)'
)
@click.option('--dt', default=0.1, show_default=True, 
    help='Time step of the simulation (seconds) Bounded: 0 < dt < 0.5'
)
def run(duration, dt):
    if dt > 0 and dt <= 0.5:
        t, x, v, a = test_ascent.run(duration, dt)
        import plot_tools
        traces = [plot_tools.create_plot_trace(t, x)]
        plot_tools.plot_traces(traces, xlabel='Time (s)', ylabel='Altitude (m)')

    else:
        log.error('Time step must be between 0 and 0.5 seconds.')


cli.add_command(test_logger)
cli.add_command(run)

if __name__ == '__main__':
    cli()
