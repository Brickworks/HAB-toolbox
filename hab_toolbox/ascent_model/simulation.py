import logging
import numpy as np
from balloon_library.balloon import Balloon, Gas
from ascent_model.forces import weight, buoyancy, drag
from ambiance.ambiance import Atmosphere


log = logging.getLogger()


def step(dt, a, v, h, balloon, total_mass):
    atmosphere = Atmosphere(h)
    balloon.match_ambient(atmosphere)
    f_weight = weight(atmosphere, total_mass)
    f_buoyancy = buoyancy(atmosphere, balloon)
    f_drag = drag(atmosphere, balloon, v)
    f_net = f_weight + f_buoyancy + f_drag

    a = f_net/total_mass
    dv = a*dt
    dh = v*dt
    log.info(
        f'{a} m/s^2 | {v} m/s | {h} m'
    )
    log.debug(
        f'f_net {f_net} N | f_weight {f_weight} N | f_buoyancy {f_buoyancy} N | f_drag {f_drag} N'
    )
    return a, dv, dh


def run(sim_config):
    balloon = Balloon(sim_config['balloon']['type'])
    lift_gas_reserve = sim_config['balloon']['reserve_mass_kg']
    lift_gas_bleed = sim_config['balloon']['bleed_mass_kg']
    balloon.lift_gas = Gas(balloon.spec['lifting_gas'], 
        mass=lift_gas_reserve+lift_gas_bleed)

    duration = sim_config['simulation']['duration']
    dt = sim_config['simulation']['dt']
    tspan = np.arange(0, duration, step=dt)
    if dt < 0 or dt >= 0.5:
        log.error('Time step must be between 0 and 0.5 seconds.')
        return

    h=sim_config['simulation']['initial_altitude']
    v=sim_config['simulation']['initial_velocity']
    a=Atmosphere(h).grav_accel

    balloon_mass = balloon.spec['mass']['value']
    bus_mass = sim_config['payload']['bus_mass_kg']
    ballast_mass = sim_config['payload']['ballast_mass_kg']
    total_mass = balloon_mass + bus_mass + ballast_mass  # [kg]

    altitude=np.array([])
    ascent_rate=np.array([])
    ascent_accel=np.array([])
    for t in tspan:
        log.debug(f'elapsed sim time: {t}s')
        if balloon.burst_threshold_exceeded:
            log.warning('Balloon burst threshold exceeded: time %s, altitude %s m, diameter %s m' % (t, h, balloon.diameter))
            tspan = np.transpose(np.where(tspan<t))
            break
        a, dv, dh = step(dt, a, v, h, balloon, total_mass)
        v += dv
        h += dh
        
        altitude = np.append(altitude, h)
        ascent_rate = np.append(ascent_rate, v)
        ascent_accel = np.append(ascent_accel, a)
    
    return tspan, altitude, ascent_rate, ascent_accel
