# HAB-toolbox
Software to assist in mechanics calculations, and simulations of high altitude baloon payloads.

## Installation
_We don't have a PyPI package yet! For now use Poetry._

Configuration management is handled by [Poetry](https://python-poetry.org/).

1. Please [install Poetry](https://python-poetry.org/docs/#installation) to use
   the HAB-toolbox.
2. Clone this repository: `git clone git@github.com:Brickworks/HAB-toolbox.git`
3. Install the package and its dependencies with Poetry: `poetry install`

## Usage (with Poetry)

### Simple 1-D ascent simulation
```bash
# run the simulation defined by sim_config.json
poetry run hab-toolbox simple-ascent sim_config.json

# run the model with verbose output, plot and save results to a file
poetry run hab-toolbox -v simple-ascent sim_config.json -o test.csv -p
```

---

## Balloon Library
A set of datasheets for [Kaymont high altitude balloons](https://www.kaymont.com/habphotography)
have been transposed into JSON format.

## Ascent Model
The HAB ascent model uses the 1976 US Standard Atmosphere (COESA)
atmosphere model from the [Ambiance](https://github.com/airinnova/ambiance/)
Python package to simulate the vertical ascent of a HAB.

See also: [Nucleus/1D Atmospheric Flight Model](https://brickworks.github.io/Nucleus/habtoolbox_1d-ascent-model/)

## Other experiments
In addition to  helpful development tools, this repository contains
experiments that were done to aid in HAB systems design.

### Kinematic Model

The kinematics model attempts to emulate the motion of the HAB bus from the
reference point of the balloon. Information from this model can be used to
estimate the performance of future payloads such as active stabilization.

For the first implementation of the kinematics model a spherical pendulum was
used to simulate the box.  A spherical pendulum was selected as it is a simple
demonstrator of the motion of the HAB from the reference frame of the balloon.

The method used for solving the equation of motion was the Runge Kutta method.
A home brewed function was created for this toolbox (instead of using the
ode45) function for educational purposes.

The method for determining the equations of motion for a spherical pendulum was
the Lagrange equations of motion.

**[Spherical Pendulum](https://en.wikipedia.org/wiki/Spherical_pendulum)**

**Lagrangian**

![](https://wikimedia.org/api/rest_v1/media/math/render/svg/a189933b115e264a4f74e7be8d8b5ffeb6bcea0b)

**[Runge-Kutta](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)**

![](https://wikimedia.org/api/rest_v1/media/math/render/svg/94677d7c780034e883b6b3f3d832cb12356a2fcc)

### Flight Simulation with PID Altitude Control
The same 1D atmospheric flight model was implemented in Simulink and
integrated with a PID control system to simulate an open-loop altitude
control system that bleeds gas from the balloon and drops ballast to
maintain a set point altitude.
