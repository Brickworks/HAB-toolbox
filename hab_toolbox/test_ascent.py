import logging
import numpy as np
from balloon_library import Balloon
from ascent_model.ideal_physics import Gas, gravity
from ascent_model.forces import weight, buoyancy, drag
from matplotlib import pyplot as plt


LOGFORMAT = '%(asctime)-15s %(levelname)+8s: %(message)s'
logging.basicConfig(format=LOGFORMAT, datefmt="%Y-%m-%dT%H:%M:%S%z")
log = logging.getLogger()

balloon = Balloon('HAB-3000')
lift_gas = Gas(balloon.spec['lifting_gas'], mass=2.0)
altitude = np.linspace(0,10)

props = []
for h in altitude:
    lift_gas.match_ambient(h)
    print(lift_gas.get_properties())
