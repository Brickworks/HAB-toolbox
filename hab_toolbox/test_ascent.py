import logging

from balloon_library import Balloon


LOGFORMAT = '%(asctime)-15s %(levelname)+8s: %(message)s'
logging.basicConfig(format=LOGFORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z")
log = logging.getLogger()

