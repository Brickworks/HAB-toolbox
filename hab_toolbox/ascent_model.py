import logging
import numpy as np
from ambiance.ambiance import Atmosphere

from hab_toolbox.balloon_library.balloon import Balloon, Gas, Payload


log = logging.getLogger()
np.set_printoptions(formatter={'float': '{:8.4f}'.format})
MAX_ALLOWED_DT = 0.5
MIN_ALLOWED_DT = 0.001


# All forces assume positive up coordinate frame.
def weight(atmosphere, total_mass)->float:
    ''' Weight (N) as a function of gropotential altitude (m) and mass (kg).

    Args:
        atmosphere (Atmosphere): Atmosphere object initialized at a specific
            altitude.
        total_mass (float): Total dry mass in kilograms.

    Returns:
        float: Weight force (positive up) in Newtons.
    '''
    return -atmosphere.grav_accel * total_mass


def buoyancy(atmosphere, balloon)->float:
    ''' Buoyancy force (N) from air displaced by lift gas at a given
    geometric altitude (m).

    Args:
        atmosphere (Atmosphere): Atmosphere object initialized at a specific
            altitude.
        balloon (Balloon): Balloon object.

    Returns:
        float: Buoyancy force (positive up) in Newtons.
    '''
    balloon.lift_gas.match_ambient(atmosphere)
    density_diff = balloon.lift_gas.density - atmosphere.density
    displaced_air = balloon.lift_gas.volume * density_diff
    return -atmosphere.grav_accel * displaced_air


def drag(atmosphere, balloon, ascent_rate)->float:
    ''' Drag force (N) from air against the windward cross-sectional area (m^2)
    at a given geometric altitude (m).

    Args:
        atmosphere (Atmosphere): Atmosphere object initialized at a specific
            altitude.
        balloon (Balloon): Balloon object.
        ascent_rate (float): Velocity (positive up) in meters/second.

    Returns:
        float: Drag force (positive up) in Newtons.
    '''
    Cd = balloon.cd
    area = balloon.projected_area
    direction = -np.sign(ascent_rate)  # always oppose direction of motion
    return direction * (1/2) * Cd * area * (ascent_rate ** 2) * atmosphere.density


def step(dt, a, v, h, balloon, payload):
    ''' Progress the simulation by one time step.

    Args:
        dt (float): Time step size in seconds.
        a (float): Acceleration (positive up) in meters/second^2.
        v (float): Velocity (positive up) in meters/second.
        h (float): Altitude in meters.
        balloon (Balloon): Balloon object.
        payload (Payload): Payload object.

    Returns:
        tuple: Tuple containing rates of change over the time step:

        - `a` (`float`): Instantaneous acceleration (positive up) in
                meters/second^2.
        - `dv` (`float`): Delta velocity (positive up) between the previous
                time index and the latest one in meters/second.
        - `dh` (`float`): Delta altitude between the previous time index and
                the latest one in meters.
    '''
    atmosphere = Atmosphere(h)
    balloon.match_ambient(atmosphere)
    total_mass = balloon.mass + payload.total_mass

    f_weight = weight(atmosphere, total_mass)
    f_buoyancy = buoyancy(atmosphere, balloon)
    f_drag = drag(atmosphere, balloon, v)
    f_net = f_weight + f_buoyancy + f_drag

    a = f_net/total_mass
    dv = a*dt
    dh = v*dt
    log.debug(' | '.join([
        f'f_net {f_net[0]} N',
        f'f_weight {f_weight[0]} N',
        f'f_buoyancy {f_buoyancy[0]} N',
        f'f_drag {f_drag[0]} N',
        f''
    ]))
    return a, dv, dh


def run(sim_config):
    ''' Start a simulation. Specify initial conditions and configurable
    parameters with a dictionary containing special keys.

    Simulation starts at a time 0 and increments the time index in steps of
    `dt` seconds until the `duration` is reached or a balloon burst event is
    detected.

    The following `sim_config` key-value pairs are supported:
    ``` json
    {
        "balloon": {
            "type": (string) Part number of the balloon to import from balloon_library,
            "reserve_mass_kg": (float) Mass of lift gas to always keep in balloon (kg),
            "bleed_mass_kg": (float) Mass of lift gas allowed to be bled from balloon (kg),
        },
        "payload": {
            "bus_mass_kg": (float) Mass of non-ballast payload mass (kg),
            "ballast_mass_kg": (float) Mass of ballast material (kg),
        },
        "pid": {
            "mode": (string) Altitude controller mode. [pwm, continuous],
            "bleed_rate_kgps": (float) Mass flow rate of lift gas bleed (kg/s),
            "ballast_rate_kgps": (float) Mass flow rate of ballast release (kg/s),
            "gains": {
                "kp": (float) Proportional gain,
                "ki": (float) Integral gain,
                "kd": (float) Derivative gain,
                "n":  (float) Filter coefficient,
            }
        },
        "simulation": {
            "id": (string) An identifier for the simulation,
            "duration": (float) Max time duration of simulation (seconds),
            "dt": (float) Time step (seconds),
            "initial_altitude": (float) Altitude at simulation start (m), [-5004 to 80000],
            "initial_velocity": (float) Velocity at simulation start (m/s)
        }
    }
    ```
    Args:
        sim_config (dict): Dictionary of simulation config parameters.

    Returns:
        tuple: Tuple containing timeserieses of simulation values:

        - `tspan` (`array`): Array of time indices in seconds.
        - `altitude` (`array`): Instantaneous acceleration (positive up) in
                meters/second^2.
        - `altitude` (`array`): Array of altitudes.
            One entry for each time index.
        - `velocity` (`array`): Array of ascent velocities.
            One entry for each time index. Positive up.
        - `acceleration` (`array`): Array of ascent accelerations.
            One entry for each time index. Positive up.
    '''
    altitude=np.array([])
    ascent_rate=np.array([])
    ascent_accel=np.array([])

    balloon = Balloon(sim_config['balloon']['type'])
    balloon.reserve_gas = sim_config['balloon']['reserve_mass_kg']
    balloon.bleed_gas = sim_config['balloon']['bleed_mass_kg']
    balloon.lift_gas = Gas(balloon.spec['lifting_gas'],
                           mass=balloon.reserve_gas+balloon.bleed_gas)
    bus_mass = sim_config['payload']['bus_mass_kg']
    ballast_mass = sim_config['payload']['ballast_mass_kg']
    payload = Payload(dry_mass=bus_mass, ballast_mass=ballast_mass)

    duration = sim_config['simulation']['duration']
    dt = sim_config['simulation']['dt']
    if dt < MIN_ALLOWED_DT or dt > MAX_ALLOWED_DT:
        # solver gets unstable with time steps above 0.5
        log.error(f'Time step must be between 0.001 and 0.5 seconds, not {dt}')
        if dt < MIN_ALLOWED_DT:
            dt = MIN_ALLOWED_DT
        elif dt > MAX_ALLOWED_DT:
            dt = MAX_ALLOWED_DT
        log.warning(f'Using closest allowed time step: {dt} seconds')

    tspan = np.arange(0, duration, step=dt)

    h = sim_config['simulation']['initial_altitude']
    v = sim_config['simulation']['initial_velocity']
    a = Atmosphere(h).grav_accel

    log.warning(
        f'Starting simulation: '
        f'balloon: {balloon.name} | '
        f'duration: {duration} s | '
        f'dt: {dt} s')
    for t in tspan:
        if balloon.burst_threshold_exceeded:
            log.warning('Balloon burst threshold exceeded: time %s, altitude %s m, diameter %s m' % (
                t, h, balloon.diameter))
            # truncate timesteps that weren't simulated
            tspan = np.transpose(tspan[np.where(tspan < t)])
            break
        a, dv, dh = step(dt, a, v, h, balloon, payload)
        v += dv
        h += dh
        log.info(' | '.join([
            f'{t:6.1f} s',
            f'{a} m/s^2',
            f'{v} m/s | {h} m',
        ]))
        altitude = np.append(altitude, h)
        ascent_rate = np.append(ascent_rate, v)
        ascent_accel = np.append(ascent_accel, a)

    return tspan, altitude, ascent_rate, ascent_accel
