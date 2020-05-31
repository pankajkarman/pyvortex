### About

The module `pyvortex` consists of functions to calculate the equivalent latitude and edge of a polar vortex using Nash criteria.

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
#### Southern Hemisphere

Multiply pv and uwind by -1, and all other things will be the same.

Example:

![Polar Vortex](ex.png)