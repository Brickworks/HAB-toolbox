import logging
import click
import json
import os
import numpy as np
from hab_toolbox import ascent_model
from hab_toolbox import plot_tools

FORMAT = '%(module)-10s %(levelname)+8s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z")
log = logging.getLogger()


@click.group()
@click.option('-v',
              '--verbose',
              is_flag=True,
              help='Show log messages at the INFO level and above.')
@click.option('-vv',
              '--debug',
              is_flag=True,
              help='Show log messages at the DEBUG level and above.')
def cli(verbose, debug):
    ''' The HAB-toolbox Command Line Interface (CLI).

    Execute with Python Poetry -> $ poetry run hab-toolbox

    Execute with Plain Python  -> $ python hab_toolbox/cli.py
    '''
    if debug:
        log.setLevel(logging.DEBUG)
    elif verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)


@cli.command()
@click.argument('config_file', type=click.File('rb'))
@click.option(
    '-o',
    '--save_output',
    type=click.Path(),
    help='Save output to file. (Name only, data will be saved as CSV)')
@click.option(
    '-p',
    '--plot',
    is_flag=True,
    help='Plot altitude, velocity, and acceleration after simulating.')
def simple_ascent(config_file, save_output, plot):
    ''' Start a 1D ascent simulation.
    
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
    t, h, v, a = ascent_model.run(sim_config)
    if save_output:
        # vertical stack single rows then transpose so they are columns
        output_array = np.vstack([t, h, v, a]).T
        output_filename, _ = os.path.splitext(save_output)
        output_filename = f'{output_filename}.csv'
        np.savetxt(output_filename,
                   output_array,
                   fmt='%.6f',
                   delimiter=',',
                   newline='\n',
                   header='time,altitude,ascent_rate,ascent_accel',
                   footer='',
                   comments='# ',
                   encoding=None)
        log.warning(f'Simulation output saved to {output_filename}')
    if plot:
        log.warning('Plotting results...')
        if save_output:
            output_filename, _ = os.path.splitext(save_output)
            save_fig = output_filename
        else:
            save_fig = None
        plot_tools.plot_ascent(t,
                               h,
                               v,
                               a,
                               title=sim_config['simulation']['id'],
                               show=True,
                               save_fig=save_fig)
    log.warning('Done.')


@cli.command()
@click.argument('csv_file', type=click.File('rb'))
@click.option('-o',
              '--save_output',
              type=click.Path(),
              help='Save output to file. Creates a .png by default.')
def plot_ascent(csv_file, save_output):
    ''' Plot altitude, velocity, and acceleration from a CSV file.
    '''
    data = np.genfromtxt(csv_file, delimiter=',')
    log.info(f'Loaded data from {csv_file}.')
    time = data[:, 0]
    altitude = data[:, 1]
    ascent_rate = data[:, 2]
    ascent_accel = data[:, 3]
    log.warning('Plotting results...')
    plot_tools.plot_ascent(time,
                           altitude,
                           ascent_rate,
                           ascent_accel,
                           title=csv_file,
                           show=True,
                           save_fig=save_output)
    log.warning('Done.')


# @cli.command()
# def pendulum():
#     ''' Simulate HAB motion as a spherical pendulum.
#     '''
#     log.error(
#         '''Nothing happened because this feature has not been implemented yet!
#         See `etc/kinematics_model`
#         ''')

cli.add_command(simple_ascent)
cli.add_command(plot_ascent)

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    cli()
