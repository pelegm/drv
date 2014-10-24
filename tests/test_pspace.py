"""
.. test_pspace.py

Testing the probability spaces module.
"""

## Testee
import drv.pspace


def equal(a, b, p=8):
    """ Verify that *a* and *b* are more or less equal (up to precision *p*).
    """
    return abs(a - b) < 10 ** (-p)


#########################################
## ----- Testing Product Pspaces ----- ##
#########################################

def test_product_pspace_integration():
    ## For infinite pspaces, this is not implemented
    ps1 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp1 = drv.pspace.FDPSpace(ps1)
    ps2 = [1, 1, 2, 0, 5, 8, 13, 0, 34, 0]
    fp2 = drv.pspace.FDPSpace(ps2)

    ppspace = drv.pspace.ProductDPSpace(fp1, fp2)
    func = lambda k1, k2: k1 + k2
    func_1 = lambda k1: k1 + fp2.integrate(lambda k2: k2)
    func_2 = lambda k2: k2 + fp1.integrate(lambda k1: k1)
    assert equal(fp1.integrate(func_1), ppspace.integrate(func))
    assert equal(fp2.integrate(func_2), ppspace.integrate(func))

