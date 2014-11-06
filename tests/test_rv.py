"""
.. test_rv.py

Testing the random variables module.
"""

## Test tools
import pytest

## Testee
import drv.rv


## Set data sets
cfunc2 = lambda n: 1 / (n + 1) ** 2
fdata1 = range(1, 6)
fdata2 = range(2, 5)
fdata3 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
fdata4 = [1, 1, 2, 0, 5, 8, 13, 0, 34, 0]


## Set probability spaces
dps = drv.pspace.DPSpace()
cdps = drv.pspace.CDPSpace(cfunc2)
fdps1 = drv.pspace.FDPSpace(fdata1)
fdps2 = drv.pspace.FDPSpace(fdata2)
fdps3 = drv.pspace.FDPSpace(fdata3)
fdps4 = drv.pspace.FDPSpace(fdata4)
ddps = drv.pspace.DegeneratePSpace()
pdps0 = drv.pspace.ProductDPSpace()
pdps1 = drv.pspace.ProductDPSpace(fdps1)
pdps2 = drv.pspace.ProductDPSpace(fdps1, fdps2)
pdps3 = drv.pspace.ProductDPSpace(fdps3, fdps4)


## Set random variables
I = lambda x: x
drv_ = drv.rv.DRV('drv', dps, I)
fdrv1 = drv.rv.FDRV('fdrv1', fdps1, I)
fdrv2 = drv.rv.FDRV('fdrv2', fdps2, I)
fdrv3 = drv.rv.FDRV('fdrv3', fdps3, I)
fdrv4 = drv.rv.FDRV('fdrv4', fdps4, I)


def test_sfunc():
    with pytest.raises(ValueError):
        drv_.sfunc({})


def test_support():
    ## TODO: infinite

    ## Finite
    assert fdrv4.support == set(i for i, p in enumerate(fdata4) if p > 0)

