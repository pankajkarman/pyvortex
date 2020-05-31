### About

The module `pyvortex` consists of functions to calculate the [equivalent latitude](https://journals.ametsoc.org/doi/citedby/10.1175/1520-0469%282003%29060%3C0287%3ATELADT%3E2.0.CO%3B2) and edge of a polar vortex using [Nash criteria](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/96JD00066).

### Installation

```
pip install pyvortex
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
![Arctic Vortex](arctic_polar_vortex_20110201.gif)

#### Southern Hemisphere

Multiply pv and uwind by -1, and all other things will be the same.

Example:

![Polar Vortex](ex.png)
