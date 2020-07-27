import logging
from skaero.atmosphere import coesa
from ascent_model.ideal_physics import gravity
import numpy as np

# All forces assume positive up coordinate frame.
log = logging.getLogger()


def weight(altitude, total_mass):
    ''' Weight (N) as a function of gropotential altitude (m) and mass (kg).
    '''
    return gravity(altitude) * total_mass


def buoyancy(altitude, gas):
    ''' Buoyancy force (N) from air displaced by lift gas.
    '''
    gas.match_ambient(altitude)
    atmo_density = coesa.table(altitude)[3]
    density_diff = gas.density - atmo_density
    displaced_air = gas.volume * density_diff
    return gravity(altitude) * displaced_air


def drag(altitude, ascent_rate, gas, balloon):
    ''' Drag force (N) from air against the windward cross-sectional area (m^2)
    '''
    Cd = balloon.spec['drag_coefficient']
    area = balloon.projected_area(gas.volume)
    atmo_density = coesa.table(altitude)[3]
    direction = -np.sign(ascent_rate)  # always oppose direction of motion
    return direction * (1/2) * Cd * area * ascent_rate ** 2 * atmo_density
