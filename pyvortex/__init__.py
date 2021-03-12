"""

This module consists of functions to calculate the [equivalent latitude](https://journals.ametsoc.org/doi/citedby/10.1175/1520-0469%282003%29060%3C0287%3ATELADT%3E2.0.CO%3B2) and edge of a polar vortex using [Nash criteria](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/96JD00066).

### Installation

```
pip install -U pyvortex
```

install the latest version using 
```
pip install git+https://github.com/pankajkarman/pyvortex.git
```

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
#### Southern Hemisphere

Flip pv and uwind along latitude dimension and multiply pv by -1. All other things will be the same.

"""

from .pyvortex import PolarVortex
