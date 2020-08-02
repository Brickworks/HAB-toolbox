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

```bash
# clone the repo
git clone git@github.com:Brickworks/HAB-toolbox.git

# use pip to install local files (editable mode)
cd HAB-toolbox
pip install -e .

# run unit tests to prove it's working
pytest -vv tests
```

## Usage
```bash
# run the simulation defined by sim_config.json
python hab_toolbox/cli.py sim sim_config.json

# run the model with verbose output, plot and save results to a file
python hab_toolbox/cli.py -v sim sim_config.json -o test.csv -p
```
