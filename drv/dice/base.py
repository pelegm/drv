"""
.. base.py

Base game mechanics.
"""

## Framework
import drv.core
import scipy.stats as ss

## Sugar
DRV = drv.core.DiscreteRandomVariable
POOL = drv.core.RandomVariablePool


def dk(k, name=None):
    """ Return the random variable representing rolling a single *k*-sided die.
    """
    _name = name or "1d{k}"
    name = _name.format(k=k)
    return DRV(name, rv=ss.randint(1, k + 1))


def ndk(n, k, name=None):
    """ Return the random variable representing rolling *n* *k*-sided dice. """
    die = dk(k, name=name)
    if n == 1:
        return die

    _name = name or "{n}d{k}"
    name = _name.format(n=n, k=k)
    return POOL(*(die for _ in xrange(n))).sum(name=name)


## Percentile dice
dp = dk(100)
dp.name = 'd%'

