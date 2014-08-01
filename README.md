# dice-rv

Dice random variables in Python made easy.

## Table of Contents

* [Documentation](#documentation)
* [Installation](#installation)

## Documentation

The module is fully documented in *sphinx* style.


## Installation

Simply download the module and put it either in your project's folder or in
your `$PYTHONPATH`.


### Dependencies

The package is built for Python 2.7.x, and is tested for that version only.

This package is essentialy a wrapper around SciPy's stats package, and uses
some NumPy code as well, so both are critical dependencies. Other than these,
the package uses Python standard libraries only.


## License

Please refer to [LICENSE](LICENSE).

## Usage

The reasonable way of using this module is as a python module; that is, with
```python
import drv
```
but see *examples*.


### Examples

Suppose I wish to plot the probability mass function of the common `3d6`
combination (which is the sum of three 6-sided dice).

