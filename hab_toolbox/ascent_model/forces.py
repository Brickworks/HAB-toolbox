import logging
from ascent_model.ideal_physics import gravity
import numpy as np

# All forces assume positive up coordinate frame.
log = logging.getLogger()


def weight(altitude, total_mass):
    ''' Weight (N) as a function of gropotential altitude (m) and mass (kg).
    '''
    return gravity(altitude) * total_mass


def buoyancy(altitude, gas, atmosphere):
    ''' Buoyancy force (N) from air displaced by lift gas at a given 
    geometric altitude (m).
    '''
    gas.match_ambient(atmosphere)
    density_diff = gas.density - atmosphere.density
    displaced_air = gas.volume * density_diff
    return gravity(altitude) * displaced_air


def drag(ascent_rate, gas, balloon, atmosphere):
    ''' Drag force (N) from air against the windward cross-sectional area (m^2)
    at a given geometric altitude (m).
    '''
    Cd = balloon.spec['drag_coefficient']
    area = balloon.projected_area(gas.volume)
    direction = -np.sign(ascent_rate)  # always oppose direction of motion
    return direction * (1/2) * Cd * area * (ascent_rate ** 2) * atmosphere.density
