"""
.. test_rv.py

Testing the random variables module.
"""

## Test tools
import pytest

## Testee
import drv.pspace
import drv.rv

## Symbolic
import sympy


## Set data sets
cfunc2 = lambda n: 1 / (n + 1) ** 2
fdata = [range(1, 6), range(2, 5), [1, 1, 2, 3, 5, 8, 13, 21, 34, 55],
         [1, 1, 2, 0, 5, 8, 13, 0, 34, 0]]
cat_data = [None, (1,), False, frozenset([2, 3]), int]


## Set probability spaces
dps = drv.pspace.DPSpace()
cdps = drv.pspace.CDPSpace(cfunc2)
fdps = [drv.pspace.FDPSpace(ps) for ps in fdata]
ddps = drv.pspace.DegeneratePSpace()
pdps = [drv.pspace.ProductDPSpace(*pss) for pss in
        [(), fdps[:1], fdps[:2], fdps[2:]]]


## Set random variables
I = lambda x: x
f = lambda x: (x % 5) ** 2
cat_f = lambda w: cat_data[w]
drv_ = drv.rv.DRV('drv', dps, I)
fdrv = [drv.rv.FDRV('fdrv{}'.format(n), ps, I) for n, ps in enumerate(fdps)]
fdrv_f = [drv.rv.FDRV('fdrv{}'.format(n), ps, f) for n, ps in enumerate(fdps)]
cat_rv = drv.rv.FDRV('cat_rv', fdps[0], cat_f)


################################################
## ----- Testing Probability Properties ----- ##
################################################


def test_categorial_pdf():
    ## Finite, categorial
    n = sum(fdata[0])
    for i, cat in enumerate(cat_data):
        assert cat_rv.pmf(cat) == sympy.Rational(i + 1, n)


def test_categorial_cdf():
    ## Finite, categorial
    p = sympy.Rational(1, 5)
    ## TODO: these still fail
    ## This needs decision; see #17
    #assert cat_rv.cdf(-1) == 0
    #for i in xrange(6):
        #    assert cat_rv.cdf(i) == p * (i + 1)
    #assert cat_rv.cdf(6) == 1


def test_mode():
    ## Infinite
    with pytest.raises(NotImplementedError):
        drv_.mode

    ## Finite
    for n, (data, rv, rvf) in enumerate(zip(fdata, fdrv, fdrv_f)):
        assert rv.mode == len(data) - (1 if n < 3 else 2)
        assert rvf.mode == f(len(data) - (1 if n < 3 else 2))


def test_pmf():
    ## Finite (I)
    s2 = sum(fdata[2])
    for w, p in enumerate(fdata[2]):
        assert fdrv[2].pmf(w) == 1.0 * p / s2


def test_sfunc():
    with pytest.raises(ValueError):
        drv_.sfunc({})


def test_support():
    ## Infinite
    with pytest.raises(NotImplementedError):
        drv_.support

    ## Finite
    assert fdrv[3].support == set(i for i, p in enumerate(fdata[3]) if p > 0)

