import logging
from balloon_library import Balloon
from ascent_model.ideal_physics import Gas, gravity

LOGFORMAT = '%(asctime)-15s %(levelname)+8s: %(message)s'
logging.basicConfig(format=LOGFORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z")
log = logging.getLogger()

balloon = Balloon('HAB-3000')
lift_gas = Gas(balloon.spec['lifting_gas'])
