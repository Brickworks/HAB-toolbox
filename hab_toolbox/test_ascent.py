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
payload_mass = 1 # [kg]
dt = 0.1
tspan = np.arange(1,10,step=dt)
h=0
v=0
a=gravity(h)

total_mass = balloon.spec['mass']['value'] + payload_mass

altitude=[]
ascent_rate=[]
ascent_accel=[]
for t in tspan:
    altitude.append(h)
    ascent_rate.append(v)
    ascent_accel.append(a)

    f_weight = weight(h, total_mass)
    f_buoyancy = buoyancy(h, lift_gas)
    f_drag = drag(h, v, lift_gas, balloon)
    f_net = f_weight + f_buoyancy + f_drag

    a = f_net/total_mass
    v += a*dt
    h += v*dt

plt.plot(tspan, altitude)
