# Reference

<!-- CONTRIBUTING --
This repo uses mkdocstrings (pawamoy/mkdocstrings) to render function comments
as API documentation.

To get your functions to be automatically documented and included in the API
Reference section, simply follow Google-style docstring conventions for python.

You can see examples of Google-style docstrings in 
[Napolion's documentation](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

The full mkdocstrings documentation is available at 
(pawamoy.github.io/mkdocstrings) and includes descriptions, API reference, and
helpful examples.
-->

## Command Line Interface

### Simple 1-D ascent simulation
```shell
# run the simulation defined by sim_config.json
poetry run hab-toolbox simple-ascent sim_config.json

# run the model with verbose output, plot and save results to a file
poetry run hab-toolbox -v simple-ascent sim_config.json -o test.csv -p
```

---

## API Reference

::: hab_toolbox
