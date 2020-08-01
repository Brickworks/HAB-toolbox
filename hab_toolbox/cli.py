#!/usr/bin/env python3

import logging
import click
import json
import numpy as np

from ascent_model import simulation
import plot_tools


FORMAT = '%(module)-10s %(levelname)+8s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z")
log = logging.getLogger()


@click.group()
@click.option('-v', '--verbose', is_flag=True, 
    help='Show log messages at the INFO level and above.')
@click.option('--debug', is_flag=True, 
    help='Show log messages at the DEBUG level and above.')
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
    help='Plot altitude, velocity, and acceleration after simulating.'
)
def sim(config_file, save_output, plot):
    ''' Start a simulation. 
    
    Specify initial conditions and configurable parameters with a CONFIG_FILE 
    formatted as a JSON.

    \b
    "balloon": (required)
        "type": Part number of the balloon to import from balloon_library
        "reserve_mass_kg": Mass of lift gas to always keep in balloon (kg)
        "bleed_mass_kg": Mass of lift gas allowed to be bled from balloon (kg)
    "payload": (required)
        "bus_mass_kg": Mass of non-ballast payload mass (kg)
        "ballast_mass_kg": Mass of ballast material (kg)
    "pid": (optional)
        "mode": Altitude controller mode. [pwm, continuous]
        "bleed_rate_kgps": Mass flow rate of lift gas bleed (kg/s)
        "ballast_rate_kgps": Mass flow rate of ballast release (kg/s)
        "gains":
            "kp": Proportional gain
            "ki": Integral gain
            "kd": Derivative gain
            "n":  Filter coefficient
    "simulation": (required)
        "duration": Max time duration of simulation (seconds)
        "dt": Time step (seconds)
        "initial_altitude": Altitude at simulation start (m), [-5004 to 80000]
        "initial_velocity": Velocity at simulation start (m/s)
    '''
    sim_config = json.load(config_file)
    log.info(f'Loaded configuration from {config_file}')
    t, h, v, a = simulation.run(sim_config)
    if save_output:
        # vertical stack single rows then transpose so they are columns
        output_array = np.vstack([t, h, v, a]).T
        np.savetxt(
            save_output, output_array, fmt='%.6f', delimiter=',', newline='\n',
            header='time,altitude,ascent_rate,ascent_accel', footer='', 
            comments='# ', encoding=None
        )
        log.warning(f'Simulation output saved to {save_output}')
    if plot:
        log.warning('Plotting results...')
        plot_tools.plot_ascent(t, h, v, a, 
            title=sim_config['simulation']['id'], show=True)
    log.warning('Done.')

cli.add_command(sim)

if __name__ == '__main__':
    cli()
