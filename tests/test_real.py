"""
.. real.py

Testing the real module.
"""

## Testee
import drv.real

## Background
import drv.pspace

## Tools
import itertools as it

## Symbolic
import sympy


def equal(a, b, p=8):
    """ Verify that *a* and *b* are more or less equal (up to precision *p*).
    """
    _a, _b = float(a), float(b)
    return abs(a - b) < 10 ** (-p)


def surely(event, p=8):
    """ Verify that *event* occurs with probability 1, up to precision *p*). If
    *event* is not really an event indicator, this may fail. """
    return equal(event.mean, 1.0)


####################################
## ----- Testing Data Model ----- ##
####################################


################################################
## ----- Testing Probability Properties ----- ##
################################################

## TODO: test entropy
## TODO: test kurtosis


def test_max():
    ## We don't test max for infinite rvs, as this is not implemented

    ## Finite, non-tricky
    ps = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp = drv.pspace.FDPSpace(ps)
    fr = drv.real.FRDRV('fr', fp, lambda x: x ** 2)
    assert equal(fr.max, (len(ps) - 1) ** 2)

    ## Finite, tricky
    ps = [1, 1, 2, 3, 5, 0, 13, 21, 34, 0]
    fp = drv.pspace.FDPSpace(ps)
    fr = drv.real.FRDRV('fr', fp, lambda x: x ** 2)
    assert equal(fr.max, (len(ps) - 2) ** 2)


## TODO: test mean
def test_mean():
    ## Infinite, but actually finite
    ## This doesn't work: see #9
    p = lambda n: 1 if n == 0 else 0
    cp = drv.pspace.CDPSpace(p)
    r = drv.real.RDRV('r', cp, lambda x: 12 - x)
    assert equal(r.mean, 12)

    ## Infinite, but constant
    p = lambda n: 1. / (n + 1) ** 2
    cp = drv.pspace.CDPSpace(p)
    r = drv.real.RDRV('r', cp, lambda x: 7)
    assert equal(r.mean, 7)

    ## TODO: add relevant tests



## TODO: test median


def test_min():
    ## We don't test min for infinite rvs, as this is not implemented

    ## Finite, non-tricky
    ps = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp = drv.pspace.FDPSpace(ps)
    fr = drv.real.FRDRV('fr', fp, lambda x: x ** 2 + 7)
    assert equal(fr.min, 7)

    ## Finite, tricky
    ps = [0, 1, 2, 3, 5, 0, 13, 21, 34, 0]
    fp = drv.pspace.FDPSpace(ps)
    fr = drv.real.FRDRV('fr', fp, lambda x: x ** 2 + 7)
    assert equal(fr.min, 8)


## TODO: test skewness
## TODO: test std
## TODO: test variance


#############################################
## ----- Testing Probability Methods ----- ##
#############################################

## TODO: test cdf
## TODO: test central moment
## TODO: test mgf


## TODO: add more subtests
def test_moment():
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


## TODO: test sf
## TODO: test standardised moment
## TODO: test isf
## TODO: test ppf
## TODO: test logcdf
## TODO: test logsf


####################################
## ----- Testing Operations ----- ##
####################################

## TODO: add tests for unop and binop


####################################
## ----- Testing Arithmetic ----- ##
####################################

def test_abs_properties():
    ## Infinite
    p = lambda n: 1. / (n + 1) ** 2
    cp = drv.pspace.CDPSpace(p)
    r = drv.real.RDRV('r', cp, lambda x: x ** 3 - 15 * x)
    abs_r = abs(r)
    assert surely(-abs_r <= r)
    assert surely(r <= abs_r)

def test_linearity_of_expectation():
    ## Infinite + Infinite
    p1 = lambda n: 1. / (n + 1) ** 2
    cp1 = drv.pspace.CDPSpace(p1)
    r1 = drv.real.RDRV('r', cp1, lambda x: x ** 2)
    p2 = lambda n: 1. / (n + 11) ** 2
    cp2 = drv.pspace.CDPSpace(p2)
    r2 = drv.real.RDRV('r', cp2, lambda x: x ** 3 - 7)
    assert equal((r1 + r2).mean, r1.mean + r2.mean)

    ## Infinite + Finite
    ps1 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp1 = drv.pspace.FDPSpace(ps1)
    fr1 = drv.real.FRDRV('fr', fp1, lambda x: x ** 2 + 7)
    assert equal((r1 + fr1).mean, r1.mean + fr1.mean)

    ## Finite + Finite
    ps2 = [1, 1, 2, 0, 5, 8, 13, 0, 34, 0]
    fp2 = drv.pspace.FDPSpace(ps2)
    fr2 = drv.real.FRDRV('fr', fp2, lambda x: x ** 3 - 6)
    assert equal((fr1 + fr2).mean, fr1.mean + fr2.mean)


def test_independence_expectation():
    ## Infinite * Infinite
    p1 = lambda n: 1. / (n + 1) ** 2
    cp1 = drv.pspace.CDPSpace(p1)
    r1 = drv.real.RDRV('r', cp1, lambda x: x ** 2)
    p2 = lambda n: 1. / (n + 11) ** 2
    cp2 = drv.pspace.CDPSpace(p2)
    r2 = drv.real.RDRV('r', cp2, lambda x: x ** 3 - 7)
    ## TODO: not implemented
    #assert equal((r1 * r2).mean, r1.mean * r2.mean)

    ## Infinite * Finite
    ps1 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp1 = drv.pspace.FDPSpace(ps1)
    fr1 = drv.real.FRDRV('fr', fp1, lambda x: x ** 2 + 7)
    ## TODO: something doesn't work here
    #assert equal((r1 + fr1).mean, r1.mean + fr1.mean)

    ## Finite * Finite
    ps2 = [1, 1, 2, 0, 5, 8, 13, 0, 34, 0]
    fp2 = drv.pspace.FDPSpace(ps2)
    fr2 = drv.real.FRDRV('fr', fp2, lambda x: x ** 3 - 6)
    assert equal((fr1 * fr2).mean, fr1.mean * fr2.mean)


##################################
## ----- Testing Concrete ----- ##
##################################

Half = sympy.S.Half
One = sympy.S.One
exp = sympy.exp
ln = sympy.ln


factorial = sympy.factorial
Symbol = sympy.Symbol
Lambda = sympy.Lambda


I = lambda x: x


def test_real_uniform():
    lefts = sympy.sympify([-3, 0, 2])
    ns = sympy.sympify([3, 7])
    for a, n in it.product(lefts, ns):
        b = a + n - 1
        ps = [1] * n
        pspace = drv.pspace.FDPSpace(ps)
        func = lambda w: w + a
        rv = drv.real.FRDRV('uniform', pspace, func)

        assert rv.entropy == ln(n)
        assert rv.kurtosis == -(6 * (n ** 2 + 1)) / (5 * (n ** 2 - 1))
        assert rv.max == b
        assert rv.mean == (a + b) / 2
        ## TODO: this test fails
        ## We need to re-implement median and/or ppf
        #assert rv.median == (a + b) / 2
        assert rv.min == a
        assert rv.skewness == 0
        assert rv.std == ((n ** 2 - 1) / 12) ** Half
        assert rv.variance == (n ** 2 - 1) / 12
        ## TODO: re-implement cdf for FRDRV
        #assert rv.cdf(-3) == (-2 - a) / n
        #assert rv.cdf(0) == (1 - a) / n
        #assert rv.cdf(2) == (3 - a) / n
        assert rv.mgf(0) == One
        ## TODO: this test fails
        #assert rv.mgf(1) == (exp(a) - exp(b+1)) / (n * (1 - exp(1)))


def test_real_poisson():
    lambdas = [One / 2, One, One * 2]
    k = Symbol('k', integer=True, nonnegative=True)
    for lam in lambdas:
        pmf = Lambda(k, lam ** k / factorial(k) * exp(-lam))
        pspace = drv.pspace.CDPSpace(pmf)
        rv = drv.real.RDRV('poisson', pspace, I)

        ## Entropy is too complicated, we skip
        assert rv.kurtosis == lam ** -1
        ## Max is not implemented, we skip
        assert rv.mean == lam
        ## Median is too complicated, we skip
        ## Min is not implemented, we skip
        assert rv.skewness == lam ** (-Half)
        assert rv.std == lam ** Half
        assert rv.variance == lam
        ## CDF is not implemented, we skip
        assert rv.mgf(0) == One
        assert equal(rv.mgf(1), exp(lam * (exp(1) - 1)))

