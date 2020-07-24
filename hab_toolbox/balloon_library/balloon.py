import logging
import json
from collections import namedtuple
import os

log = logging.getLogger()


BALLOON_LIBRARY_DIR = os.path.dirname(__file__)


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


class Balloon():
    def __init__(self, spec_name):
        if is_valid_balloon(spec_name):
            config_filename = '%s.json' % spec_name
            config_path = os.path.join(BALLOON_LIBRARY_DIR, config_filename)
            with open(config_path) as config_json_data:
                config_data = json.load(config_json_data)
                self.convert_json(config_data)
        else:
            log.error('No valid balloon named %s' % spec_name)

    def convert_json(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
