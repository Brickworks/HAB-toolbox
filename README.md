# HAB-toolbox
Software to assist in mechanics calculations, and simulations of high altitude baloon payloads. 

## MaTHs

Lagrangian

![](https://wikimedia.org/api/rest_v1/media/math/render/svg/a189933b115e264a4f74e7be8d8b5ffeb6bcea0b)

Runge-Kutta

![](https://wikimedia.org/api/rest_v1/media/math/render/svg/94677d7c780034e883b6b3f3d832cb12356a2fcc)

[Spherical Pendulum](https://en.wikipedia.org/wiki/Spherical_pendulum)

[Runge-Kutta](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods)

## Balloon Library
A set of datasheets for [Kaymont high altitude balloons](https://www.kaymont.com/habphotography)
have been transposed into JSON format.

## Ascent Model
The HAB ascent model uses the 1976 US Standard Atmosphere (COESA)
atmosphere model from the [Ambiance](https://github.com/airinnova/ambiance/) Python package to simulate the vertical ascent of a HAB.

## Installation
_We don't have a PyPI package yet! For now use Poetry.)_

Configuration management is handled by [Poetry](https://python-poetry.org/).

1. Please [install Poetry](https://python-poetry.org/docs/#installation) to use
   the HAB-toolbox.
2. Clone this repository: `git clone git@github.com:Brickworks/HAB-toolbox.git`
3. Install the package and its dependencies with Poetry: `poetry install`

## Usage (with Poetry)
```bash
# run the simulation defined by sim_config.json
poetry run hab-toolbox sim sim_config.json

# run the model with verbose output, plot and save results to a file
poetry run hab-toolbox -v sim sim_config.json -o test.csv -p
```