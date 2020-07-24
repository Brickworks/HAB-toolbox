import logging
from ideal_physics import gravity
import numpy as np

'''
All forces assume positive up coordinate frame.
'''


def weight(altitude, total_mass):
    ''' Weight (N) as a function of altitude (m) and mass (kg).
    '''
    return gravity(altitude) * total_mass


def buoyancy(altitude, gas):
    ''' Buoyancy force (N) from air displaced by lift gas.
    '''
    atmo_density = atmo_model.get_density(altitude)
    density_diff = gas.density - atmo_density
    displaced_air = gas.volume * density_diff
    return gravity(altitude) * displaced_air


def drag(altitude, ascent_rate, gas, balloon):
    Cd = balloon.spec['drag_coefficient']
    area = balloon.projected_area(gas.volume)
    atmo_density = atmo_model.get_density(altitude)
    direction = -np.sign(ascent_rate)  # always oppose direction of motion
    return direction * (1/2) * Cd * area * ascent_rate ** 2 * atmo_density
