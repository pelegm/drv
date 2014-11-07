"""
.. test_pspace.py

Testing the probability spaces module.
"""

## Test tools
import itertools as it
import drv.tools

## Testee
import drv.pspace


def equal(a, b, p=8):
    """ Verify that *a* and *b* are more or less equal (up to precision *p*).
    """
    return abs(a - b) < 10 ** (-p)


##########################################
## ----- Testing Basic Properties ----- ##
##########################################

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


def test_Omega_property():
    ## An Omega property must exist, but may return NotImplementedError
    for ps in [dps, cdps]:
        try:
            omega = ps.Omega
        except NotImplementedError:
            pass

    ## Special attention for the finite cases:
    assert fdps1.Omega == {(i,) for i in xrange(len(fdata1))}
    assert ddps.Omega == {(0,)}
    product = set(it.product(xrange(len(fdata1)), xrange(len(fdata2))))
    assert pdps2.Omega == product


def test_F_property():
    ## An Omega property must exist, but may return NotImplementedError
    for ps in [dps, cdps]:
        try:
            F = ps.F
        except NotImplementedError:
            pass

    ## Special attention for the finite cases:
    assert fdps1.F == set(drv.tools.powerset({(i,) for i in
                                              xrange(len(fdata1))}))
    assert ddps.F == {frozenset(), frozenset([(0,)])}
    product = set(it.product(xrange(len(fdata1)), xrange(len(fdata2))))
    assert pdps2.F == set(drv.tools.powerset(pdps2.Omega))


#########################################
## ----- Testing Product Pspaces ----- ##
#########################################

def test_product_pspace_integration():
    ## For infinite pspaces, this is not implemented
    func = lambda k1, k2: k1 + k2
    func_1 = lambda k1: k1 + fdps4.integrate(lambda k2: k2)
    func_2 = lambda k2: k2 + fdps3.integrate(lambda k1: k1)
    assert equal(fdps3.integrate(func_1), pdps3.integrate(func))
    assert equal(fdps4.integrate(func_2), pdps3.integrate(func))

