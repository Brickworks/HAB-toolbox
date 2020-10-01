''' Balloon and Gas properties.

This module defines Balloon objects and Gas objects for use in high altitude
balloon simulations.

Balloon objects are initialized from a specification definition file, which
is a JSON that lives in the same directory as this module. These definition
files are generated from high altitude balloon specification datasheets
provided by the balloon's manufacturer. It includes attributes such as the
size, mass, volume limits, approximate drag coefficient, and other useful
metrics. The Balloon object has class methods
'''

import logging
import json
import os
import math

# Logger (initialized by cli.py)
log = logging.getLogger()

# Constants
PI = math.pi
BALLOON_LIBRARY_DIR = os.path.dirname(__file__)
BOLTZMANN_CONSTANT = 1.38e-23  # [J/K]
AVOGADRO_CONSTANT = 3.022e23  # [1/mol]
R = BOLTZMANN_CONSTANT * AVOGADRO_CONSTANT  # [J / K mol] Ideal Gas Constant
STANDARD_TEMPERATURE_K = 273.15
STANDARD_PRESSURE_Pa = 101.325e3

# Known properties of common gasses
GAS_PROPERTIES_CONFIG = {
    "units": "kg/mol",
    "gas_properties": [
        {
            "species": ["air"],
            "molar_mass": 0.02897
        },
        {
            "species": ["he", "helium"],
            "molar_mass": 0.0040026
        },
        {
            "species": ["h2", "hydrogen"],
            "molar_mass": 0.00201594
        },
        {
            "species": ["n2", "nitrogen"],
            "molar_mass": 0.0280134
        },
        {
            "species": ["o2", "oxygen"],
            "molar_mass": 0.0319988
        },
        {
            "species": ["ar", "argon"],
            "molar_mass": 0.039948
        },
        {
            "species": ["co2", "carbon dioxide"],
            "molar_mass": 0.04400995
        },
        {
            "species": ["ne", "neon"],
            "molar_mass": 0.020183
        },
        {
            "species": ["kr", "krypton"],
            "molar_mass": 0.08380
        },
        {
            "species": ["xe", "xenon"],
            "molar_mass": 0.13130
        },
        {
            "species": ["ch4", "methane"],
            "molar_mass": 0.01604303
        }
    ]
}
''' Dictionary of gasses species and their special properties.

Source: US Standard Atmosphere, 1976

Key| Species          | Molar Weight (kg/mol)
---|----------------- | ---------------------
Air| Air              | 0.02897
He | Helium           | 0.0040026
H2 | Hydrogen         | 0.00201594
N2 | Nitrogen         | 0.0280134
O2 | Oxygen           | 0.0319988
Ar | Argon            | 0.039948
CO2| Carbon Dioxide   | 0.04400995
Ne | Neon             | 0.020183
Kr | Krypton          | 0.08380
Xe | Xenon            | 0.13130
CH4| Methane          | 0.01604303

Note: All properties are measured from dry gasses at sea level.
'''


def get_gas_properties():
    ''' Return the dictionary of gas species and their molar mass (kg/mol).
    '''
    gas_properties = GAS_PROPERTIES_CONFIG['gas_properties']
    units = GAS_PROPERTIES_CONFIG['units']

    known_species = {}
    for gas in gas_properties:
        for gas_name in gas['species']:
            known_species[gas_name] = gas['molar_mass']
    log.debug('Known gas species: %s' % known_species)
    return known_species, units


def list_known_species():
    ''' Return all species listed in `get_gas_properties`.
    
    Returns:
        list: Keys of valid gas species.
    '''
    known_species, _ = get_gas_properties()
    return list(known_species.keys())


def is_valid_gas(species):
    ''' Return True if there is a known molecular weight for the input 
    `species`.

    Args:
        species (string): Name or abbreviation of a gas (i.e. `he` or `helium`)

    Returns:
        bool: Returns `True` if `species` is in the known list of gas species.
    '''
    return species in list_known_species()


def is_valid_balloon(spec_name):
    ''' Returns True if `spec_name` matches the name of a known balloon 
    definition.

    Balloon definition files are JSON files in the `balloon_library` directory.
    
    Args:
        spec_name (string): Name of the balloon spec to use. Case sensitive and
            does not include the file (i.e. `HAB-3000` corresponds to 
            `ballon_library/HAB-3000.json`).

    Returns:
        bool: Returns True if `spec_name` matches the name of a known balloon 
        definition.
    '''
    known_balloons = []
    for f in os.listdir(BALLOON_LIBRARY_DIR):
        if os.path.isfile(os.path.join(BALLOON_LIBRARY_DIR, f)):
            fileparts = os.path.splitext(f)
            if fileparts[1] == '.json':
                known_balloons.append(fileparts[0])
    log.debug('Known balloons: %s' % known_balloons)
    return spec_name in known_balloons


def get_balloon(spec_name):
    ''' Get balloon spec sheet definitions as a dictionary.

    Balloon definition files are JSON files in the `balloon_library` directory.
    
    Args:
        spec_name (string): Name of the balloon spec to use. Case sensitive and
            does not include the file (i.e. `HAB-3000` corresponds to 
            `ballon_library/HAB-3000.json`).

    Returns:
        dict: Dictionary of balloon specification parameters.
    '''
    if is_valid_balloon(spec_name):
        config_filename = '%s.json' % spec_name
        config_path = os.path.join(BALLOON_LIBRARY_DIR, config_filename)
        with open(config_path) as config_json_data:
            config_data = json.load(config_json_data)
        return config_data
    else:
        raise ValueError('No valid balloon named %s' % spec_name)


def _radius_from_volume(volume):
    ''' Return the volume of a sphere given its radius.
    '''
    if volume < 0:
        raise ValueError('Cannot have negative volume! (%s)' % volume)
    return (volume / (4/3 * PI)) ** (1/3)


class Gas():
    def __init__(self, species, mass=0):
        species = species.lower()
        if is_valid_gas(species):
            self.species = species
        else:
            raise ValueError(
                '"%s" is not a member of the list of known gases: %s' % (
                    species, list_known_species()))
        self.molar_mass = self._set_molar_mass()  # get molar mass from config
        self.temperature = STANDARD_TEMPERATURE_K  # [K] standard temperature
        self.pressure = STANDARD_PRESSURE_Pa  # [Pa] standard pressure
        self.mass = mass  # [kg] mass

    def _set_molar_mass(self):
        ''' Get the molecular weight (kg/mol) of a dry gas.
        '''
        known_species, _ = get_gas_properties()

        species_of_interest = self.species.lower()
        if species_of_interest in known_species.keys():
            return known_species[species_of_interest]
        else:
            log.error('Species %s is not defined!' % self.species)

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

    def match_conditions(self, temperature, pressure):
        ''' Update temperature (K), pressure (Pa) to match specific values.
        '''
        log.debug('Matching %s temperature and pressure to %s K, %s Pa' % (
            self.species, temperature, pressure
        ))
        self.temperature = temperature
        self.pressure = pressure


class Balloon():
    def __init__(self, spec_name, lift_gas=None):
        config_data = get_balloon(spec_name)
        self.name = config_data['name']
        self.datasheet = config_data['datasheet']
        self.part_number = config_data['part_number']
        self.spec = config_data['spec']
        if lift_gas is None:
            self.lift_gas = Gas(self.spec['lifting_gas'])
        else:
            self.lift_gas = lift_gas  # Gas object
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
        burst_diameter = self.spec['diameter_burst']['value']
        self.diameter = 2 * _radius_from_volume(self.volume)
        log.debug('Balloon diameter is %s (burst at %s)' % (
            self.diameter, burst_diameter))
        return self.diameter >= burst_diameter

    def match_ambient(self, atmosphere):
        ''' Update temperature (K), pressure (Pa), and density (kg/m^3) to
        match ambient air conditions at a given geopotential altitude (m).
        '''
        self.lift_gas.match_ambient(atmosphere)

    def match_conditions(self, temperature, pressure):
        ''' Update temperature (K), pressure (Pa) to match specific values.
        '''
        self.lift_gas.match_conditions(temperature, pressure)


class Payload():
    ''' The thing carried by a balloon.
    '''

    def __init__(self, dry_mass=2, ballast_mass=0):
        self.dry_mass = dry_mass  # [kg] cannot change in flight
        self.ballast_mass = ballast_mass  # [kg] can be dropped in flight

    @property
    def total_mass(self):
        return self.dry_mass + self.ballast_mass
