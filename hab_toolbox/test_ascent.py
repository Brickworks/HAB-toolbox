import logging
import numpy as np
from balloon_library import Balloon
from ascent_model.ideal_physics import Gas, gravity
from ascent_model.forces import weight, buoyancy, drag
from ambiance.ambiance import Atmosphere


log = logging.getLogger()


def step(dt, a, v, h, balloon, lift_gas, total_mass):
    atmosphere = Atmosphere(h)
    f_weight = weight(h, total_mass)
    f_buoyancy = buoyancy(h, lift_gas, atmosphere)
    f_drag = drag(v, lift_gas, balloon, atmosphere)
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


def run(duration=3000, dt=0.1):
    balloon = Balloon('HAB-3000')
    lift_gas = Gas(balloon.spec['lifting_gas'], mass=3.0)
    payload_mass = 0 # [kg]
    tspan = np.arange(0,duration,step=dt)
    h=0.0
    v=0.0
    a=gravity(h)

    total_mass = balloon.spec['mass']['value'] + payload_mass

    altitude=np.array([])
    ascent_rate=np.array([])
    ascent_accel=np.array([])
    for t in tspan:
        altitude = np.append(altitude, h)
        ascent_rate = np.append(ascent_rate, v)
        ascent_accel = np.append(ascent_accel, a)

        log.debug(f'elapsed sim time: {t}s')
        if balloon.burst_threshold_exceeded(lift_gas.volume):
            log.warning('Balloon burst threshold exceeded: time %s, altitude %s m, diameter %s m' % (t, h, balloon.diameter))
            tspan = np.transpose(np.where(tspan<t))
            break
        a, dv, dh = step(dt, a, v, h, balloon, lift_gas, total_mass)
        v += dv
        h += dh
    
    return tspan, altitude, ascent_rate, ascent_accel


if __name__ == '__main__':
    t, x, v, a = run()
    import plot_tools
    traces = [plot_tools.create_plot_trace(t, x)]
    plot_tools.plot_traces(traces, xlabel='Time (s)', ylabel='Altitude (m)')
