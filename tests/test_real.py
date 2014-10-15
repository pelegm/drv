"""
.. real.py

Testing the real module.
"""

## Testee
import drv.real

## Background
import drv.pspace


def equal(a, b, p=8):
    return abs(a - b) < 10 ** (-p)


def test_moments():
    ## Infinite
    p = lambda n: 1. / (n + 1) ** 2
    cp = drv.pspace.CDPSpace(p)
    r = drv.real.RDRV('r', cp, lambda x: x ** 2)

    ## MGF at 0 is always 1
    assert equal(r.mgf(0), 1)

    ## Finite
    ps = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp = drv.pspace.FDPSpace(ps)
    fr = drv.real.FRDRV('fr', fp, lambda x: x ** 2)

    ## MGF at 0 is always 1
    assert equal(fr.mgf(0), 1)

