import logging
import numpy as np

# All forces assume positive up coordinate frame.
log = logging.getLogger()


def weight(atmosphere, total_mass):
    ''' Weight (N) as a function of gropotential altitude (m) and mass (kg).
    '''
    return -atmosphere.grav_accel * total_mass


def buoyancy(atmosphere, balloon):
    ''' Buoyancy force (N) from air displaced by lift gas at a given 
    geometric altitude (m).
    '''
    balloon.lift_gas.match_ambient(atmosphere)
    density_diff = balloon.lift_gas.density - atmosphere.density
    displaced_air = balloon.lift_gas.volume * density_diff
    return -atmosphere.grav_accel * displaced_air


def drag(atmosphere, balloon, ascent_rate):
    ''' Drag force (N) from air against the windward cross-sectional area (m^2)
    at a given geometric altitude (m).
    '''
    Cd = balloon.spec['drag_coefficient']
    area = balloon.projected_area
    direction = -np.sign(ascent_rate)  # always oppose direction of motion
    return direction * (1/2) * Cd * area * (ascent_rate ** 2) * atmosphere.density
