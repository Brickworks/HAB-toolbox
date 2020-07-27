import logging
import json
import os
from skaero.atmosphere import coesa


log = logging.getLogger()
GAS_PROPERTIES_CONFIG = os.path.join(
    os.path.dirname(__file__), 'gas_properties.json')

BOLTZMANN_CONSTANT = 1.38e-23  # [J/K]
AVOGADRO_CONSTANT = 3.022e23  # [1/mol]
R = BOLTZMANN_CONSTANT * AVOGADRO_CONSTANT  # [J / K mol] Ideal Gas Constant

STANDARD_GRAVITY = 9.80665  # [m/s^2] Standard acceleration from gravity (g0)
MEAN_EARTH_RADIUS = 6371007.2  # [m] mean radius of Earth


class Gas():
    def __init__(self, species, mass=0):
        self.species = species
        self.molar_mass = self._set_molar_mass()  # get molar mass from config
        self.temperature = 273.15  # [K] standard temperature
        self.pressure = 101.325e3  # [Pa] standard pressure
        self.mass = mass  # [kg] mass

    def _set_molar_mass(self):
        ''' Get the molecular weight (kg/mol) of a dry gas.
        '''
        with open(GAS_PROPERTIES_CONFIG) as config_json_data:
            config_data = json.load(config_json_data)
        gas_properties = config_data['gas_properties']
        known_species = {}
        for gas in gas_properties:
            for gas_name in gas['species']:
                known_species[gas_name] = gas['molar_mass']
            log.debug('Known gas species: %s' % known_species)

        species_of_interest = self.species.lower()
        if species_of_interest in known_species.keys():
            return known_species[species_of_interest]
        else:
            log.error('Species %s is not defined in %s' %
                      (self.species, GAS_PROPERTIES_CONFIG))

    @property
    def volume(self):
        ''' Ideal gas volume (m^3) from temperature (K) and pressure (Pa) for
            a given mass (kg) of gas. 
        '''
        moles = (self.mass / self.molar_mass)
        return moles * (self.temperature / self.pressure)
    
    @property
    def density(self):
        ''' Ideal gas density (kg/m^3) from temperature (K) and pressure (Pa).
        '''
        return (self.molar_mass * self.pressure) / (R * self.temperature)
    
    def match_ambient(self, altitude):
        ''' Update temperature (K), pressure (Pa), and density (kg/m^3) to
        match ambient air conditions at a given geopotential altitude (m).
        '''
        self.temperature = coesa.table(altitude)[1]
        self.pressure = coesa.table(altitude)[2]

    def get_properties(self):
        ''' Return all gas properties as a tuple.
        '''
        return self.temperature, self.pressure, self.density, self.volume

def gravity(altitude):
    ''' Acceleration due to gravity (m/s^2) as a function of geopotential
    altitude (m).
    
    Gravity is negative because it assumes positive up coordinate frame.
    '''
    return -STANDARD_GRAVITY * (
        MEAN_EARTH_RADIUS / (altitude + MEAN_EARTH_RADIUS)
    ) ** 2
