_________________

[![PyPI version](https://badge.fury.io/py/pyvortex.svg)](http://badge.fury.io/py/pyvortex)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/pyvortex/)
[![Downloads](https://pepy.tech/badge/pyvortex)](https://pepy.tech/project/pyvortex)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
_________________

### About

The module `pyvortex` consists of functions to calculate the [equivalent latitude](https://journals.ametsoc.org/doi/citedby/10.1175/1520-0469%282003%29060%3C0287%3ATELADT%3E2.0.CO%3B2) and edge of a polar vortex using [Nash criteria](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/96JD00066).

### Installation

```
pip install pyvortex
```

install the latest version using 
```
pip install git+https://github.com/pankajkarman/pyvortex.git

```

## Documentation

Latest documentation is available [here](https://pankajkarman.github.io/pyvortex/).


### Usage

`pyvortex` is easy to use. Just import:

```python
import pyvortex as vr
```

#### Northern Hemisphere

Instantiate the `PolarVortex` class using: 
```python
pol = PolarVortex(pv, uwind)
```
Get equivalent lqtitude for the provided vorticity data as:
```python
eql = pol.get_eql()
```
If you want to get both equivalent latitude and Vortex edge, just use:
```python
eql = pol.get_edge(min_eql=30)
```
Example:
![Arctic Vortex](./example/arctic_polar_vortex_20110201.gif)

#### Southern Hemisphere

Flip pv and uwind along latitude dimension and multiply pv by -1. All other things will be the same.

Example:

![Polar Vortex](./example/antarctic.gif)
