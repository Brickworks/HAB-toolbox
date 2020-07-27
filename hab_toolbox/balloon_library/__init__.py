import logging
import json
from collections import namedtuple
import os
import math

log = logging.getLogger()


BALLOON_LIBRARY_DIR = os.path.dirname(__file__)
PI = math.pi


def is_valid_balloon(spec_name):
    known_balloons = []
    for f in os.listdir(BALLOON_LIBRARY_DIR):
        if os.path.isfile(os.path.join(BALLOON_LIBRARY_DIR, f)):
            fileparts = os.path.splitext(f)
            if fileparts[1] == '.json':
                known_balloons.append(fileparts[0])
    log.debug('Known balloons: %s' % known_balloons)
    return spec_name in known_balloons


def _json_object_hook(data):
    return namedtuple('Balloon', data.keys())(*data.values())


def json2obj(json_data):
    return json.load(json_data, object_hook=_json_object_hook)


def _radius_from_volume(volume):
    return (volume / (4/3 * PI)) ** (1/3)


class Balloon():
    def __init__(self, spec_name):
        if is_valid_balloon(spec_name):
            config_filename = '%s.json' % spec_name
            config_path = os.path.join(BALLOON_LIBRARY_DIR, config_filename)
            with open(config_path) as config_json_data:
                config_data = json.load(config_json_data)
            self.name = config_data['name']
            self.datasheet = config_data['datasheet']
            self.part_number = config_data['part_number']
            self.spec = config_data['spec']
        else:
            raise ValueError('No valid balloon named %s' % spec_name)
    
    def projected_area(self, volume):
        ''' Projected cross-sectional area of the balloon (m^2) for use in drag
        calculations assuming the balloon is a sphere with volume (m^3).
        '''
        self.radius = _radius_from_volume(volume)
        return PI * (self.radius ** 2)

    def burst_threshold_exceeded(self, volume):
        ''' Check if the given volume (m^3) is greater than or equal to the 
        burst volume (m^3) from the spec sheet.
        '''
        self.diameter = 2 * _radius_from_volume(volume)
        return self.diameter >= self.spec['diameter_burst']['value']
