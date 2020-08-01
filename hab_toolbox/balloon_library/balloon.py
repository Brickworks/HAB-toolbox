import logging
import json
import os
import math


log = logging.getLogger()
PI = math.pi
BALLOON_LIBRARY_DIR = os.path.dirname(__file__)
GAS_PROPERTIES_CONFIG = os.path.join(
    os.path.dirname(__file__), 'gas_properties.json')
BOLTZMANN_CONSTANT = 1.38e-23  # [J/K]
AVOGADRO_CONSTANT = 3.022e23  # [1/mol]
R = BOLTZMANN_CONSTANT * AVOGADRO_CONSTANT  # [J / K mol] Ideal Gas Constant


def get_gas_properties():
    with open(GAS_PROPERTIES_CONFIG) as config_json_data:
        config_data = json.load(config_json_data)
    return config_data['gas_properties']


def is_valid_balloon(spec_name):
    known_balloons = []
    for f in os.listdir(BALLOON_LIBRARY_DIR):
        if os.path.isfile(os.path.join(BALLOON_LIBRARY_DIR, f)):
            fileparts = os.path.splitext(f)
            if fileparts[1] == '.json' and fileparts[0] != 'gas_properties':
                known_balloons.append(fileparts[0])
    log.debug('Known balloons: %s' % known_balloons)
    return spec_name in known_balloons


def get_balloon(spec_name):
    if is_valid_balloon(spec_name):
        config_filename = '%s.json' % spec_name
        config_path = os.path.join(BALLOON_LIBRARY_DIR, config_filename)
        with open(config_path) as config_json_data:
            config_data = json.load(config_json_data)
        return config_data
    else:
        raise ValueError('No valid balloon named %s' % spec_name)


def _radius_from_volume(volume):
    return (volume / (4/3 * PI)) ** (1/3)


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
        known_species = {}
        gas_properties = get_gas_properties()
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
        V = moles * R * self.temperature / self.pressure
        return V

    @property
    def density(self):
        ''' Ideal gas density (kg/m^3) from temperature (K) and pressure (Pa).
        '''
        return (self.molar_mass * self.pressure) / (R * self.temperature)

    def match_ambient(self, atmosphere):
        ''' Update temperature (K), pressure (Pa), and density (kg/m^3) to
        match ambient air conditions at a given geopotential altitude (m).
        '''
        log.debug('Matching %s temperature and pressure to ambient at %s meters (geometric altitude)' % (
            self.species, atmosphere.h
        ))
        self.temperature = atmosphere.temperature
        self.pressure = atmosphere.pressure


class Balloon():
    def __init__(self, spec_name, lift_gas=None):
        config_data = get_balloon(spec_name)
        self.name = config_data['name']
        self.datasheet = config_data['datasheet']
        self.part_number = config_data['part_number']
        self.spec = config_data['spec']
        if lift_gas is None:
            self.lift_gas = Gas(self.spec['lifting_gas'])
        self.cd = self.spec['drag_coefficient']
        self.mass = self._get_value_from_spec('mass')
        self.burst_diameter = self._get_value_from_spec('diameter_burst')

    def _get_value_from_spec(self, key):
        return self.spec[key]['value']
    
    def _get_unit_from_spec(self, key):
        return self.spec[key]['unit']

    @property
    def volume(self):
        ''' Ideal gas volume (m^3) from temperature (K) and pressure (Pa) for
            a given mass (kg) of gas. 
        '''
        return self.lift_gas.volume

    @property
    def projected_area(self):
        ''' Projected cross-sectional area of the balloon (m^2) for use in drag
        calculations assuming the balloon is a sphere with volume (m^3).
        '''
        self.radius = _radius_from_volume(self.volume)
        return PI * (self.radius ** 2)

    @property
    def burst_threshold_exceeded(self):
        ''' Check if the given volume (m^3) is greater than or equal to the 
        burst volume (m^3) from the spec sheet.
        '''
        self.diameter = 2 * _radius_from_volume(self.volume)
        return self.diameter >= self.spec['diameter_burst']['value']

    def match_ambient(self, atmosphere):
        ''' Update temperature (K), pressure (Pa), and density (kg/m^3) to
        match ambient air conditions at a given geopotential altitude (m).
        '''
        self.lift_gas.match_ambient(atmosphere)


class Payload():
    ''' The thing carried by a balloon.
    '''

    def __init__(self, dry_mass=2, ballast_mass=0):
        self.dry_mass = dry_mass  # [kg] cannot change in flight
        self.ballast_mass = ballast_mass  # [kg] can be dropped in flight

    @property
    def total_mass(self):
        return self.dry_mass + self.ballast_mass
