"""
.. real.py

Testing the real module.
"""

## Test tools
import pytest
bench = pytest.mark.bench
slow = pytest.mark.slow

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
    square = fp.symbol ** 2
    fr = drv.real.FRDRV('fr', fp, square)
    assert equal(fr.max, (len(ps) - 1) ** 2)

    ## Finite, tricky
    ps = [1, 1, 2, 3, 5, 0, 13, 21, 34, 0]
    fp = drv.pspace.FDPSpace(ps)
    square = fp.symbol ** 2
    fr = drv.real.FRDRV('fr', fp, square)
    assert equal(fr.max, (len(ps) - 2) ** 2)


## TODO: test mean
def test_mean():
    ## Infinite, but actually finite
    ## This doesn't work: see #9
    p = lambda n: 1 if n == 0 else 0
    cp = drv.pspace.CDPSpace(p)
    r = drv.real.RDRV('r', cp, 12 - cp.symbol)
    assert equal(r.mean, 12)

    ## Infinite, but constant
    p = lambda n: 1. / (n + 1) ** 2
    cp = drv.pspace.CDPSpace(p)
    r = drv.real.RDRV('r', cp, 7)
    assert equal(r.mean, 7)

    ## TODO: add relevant tests



## TODO: test median


def test_min():
    ## We don't test min for infinite rvs, as this is not implemented

    ## Finite, non-tricky
    ps = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp = drv.pspace.FDPSpace(ps)
    x = fp.symbol
    fr = drv.real.FRDRV('fr', fp, x ** 2 + 7)
    assert equal(fr.min, 7)

    ## Finite, tricky
    ps = [0, 1, 2, 3, 5, 0, 13, 21, 34, 0]
    fp = drv.pspace.FDPSpace(ps)
    x = fp.symbol
    fr = drv.real.FRDRV('fr', fp, x ** 2 + 7)
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
    x = cp.symbol
    r = drv.real.RDRV('r', cp, x ** 2)

    ## MGF at 0 is always 1
    assert equal(r.mgf(0), 1)

    ## Finite
    ps = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp = drv.pspace.FDPSpace(ps)
    x = fp.symbol
    fr = drv.real.FRDRV('fr', fp, x ** 2)

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
    x = cp.symbol
    r = drv.real.RDRV('r', cp, x ** 3 - 15 * x)
    abs_r = abs(r)
    assert surely(-abs_r <= r)
    assert surely(r <= abs_r)

def test_linearity_of_expectation():
    ## Infinite + Infinite
    p1 = lambda n: 1. / (n + 1) ** 2
    cp1 = drv.pspace.CDPSpace(p1)
    x = cp1.symbol
    r1 = drv.real.RDRV('r', cp1, x ** 2)
    p2 = lambda n: 1. / (n + 11) ** 2
    cp2 = drv.pspace.CDPSpace(p2)
    x = cp2.symbol
    r2 = drv.real.RDRV('r', cp2, x ** 3 - 7)
    assert equal((r1 + r2).mean, r1.mean + r2.mean)

    ## Infinite + Finite
    ps1 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp1 = drv.pspace.FDPSpace(ps1)
    x = fp1.symbol
    fr1 = drv.real.FRDRV('fr', fp1, x ** 2 + 7)
    assert equal((r1 + fr1).mean, r1.mean + fr1.mean)

    ## Finite + Finite
    ps2 = [1, 1, 2, 0, 5, 8, 13, 0, 34, 0]
    fp2 = drv.pspace.FDPSpace(ps2)
    x = fp2.symbol
    fr2 = drv.real.FRDRV('fr', fp2, x ** 3 - 6)
    assert equal((fr1 + fr2).mean, fr1.mean + fr2.mean)


def test_independence_expectation():
    ## Infinite * Infinite
    p1 = lambda n: 1. / (n + 1) ** 2
    cp1 = drv.pspace.CDPSpace(p1)
    x = cp1.symbol
    r1 = drv.real.RDRV('r', cp1, x ** 2)
    p2 = lambda n: 1. / (n + 11) ** 2
    cp2 = drv.pspace.CDPSpace(p2)
    x = cp2.symbol
    r2 = drv.real.RDRV('r', cp2, x ** 3 - 7)
    ## TODO: not implemented
    #assert equal((r1 * r2).mean, r1.mean * r2.mean)

    ## Infinite * Finite
    ps1 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    fp1 = drv.pspace.FDPSpace(ps1)
    x = fp1.symbol
    fr1 = drv.real.FRDRV('fr', fp1, x ** 2 + 7)
    ## TODO: something doesn't work here
    #assert equal((r1 + fr1).mean, r1.mean + fr1.mean)

    ## Finite * Finite
    ps2 = [1, 1, 2, 0, 5, 8, 13, 0, 34, 0]
    fp2 = drv.pspace.FDPSpace(ps2)
    x = fp2.symbol
    fr2 = drv.real.FRDRV('fr', fp2, x ** 3 - 6)
    assert equal((fr1 * fr2).mean, fr1.mean * fr2.mean)


##################################
## ----- Testing Concrete ----- ##
##################################

Zero = sympy.S.Zero
Half = sympy.S.Half
One = sympy.S.One
exp = sympy.exp
ln = sympy.ln


binomial = sympy.binomial
factorial = sympy.factorial
sqrt = sympy.sqrt
Symbol = sympy.Symbol
Lambda = sympy.Lambda


I = lambda x: x
n = Symbol('n', integer=True, nonnegative=True)
t = Symbol('t', real=True)


## Each of the following tests should do the following:
## - run over 2-3 options for each distribution param
## - build an appropriate pspace
## - build a relevant func (possibly the identity)
## - build a random variable
## - for RDRV, assert each of the following properties:
##   - entropy
##   - kurtosis
##   - max
##   - mean
##   - median
##   - min
##   - skewness
##   - std
##   - variance
## - for RDRV, assert each of the following methods:
##   - cdf
##   - mgf
##   - pmf
## - for FRDRV, assert in addition the following properties:
##   - mode
##   - support


def test_real_bernoulli():
    ## Params
    p_s = [Half / 2, Half, Half + Half / 2]

    for p in p_s:

        ## Deduced params
        q = 1 - p

        ## PSpace
        ps = [q, p]
        pspace = drv.pspace.FDPSpace(ps)

        ## RV
        rv = drv.real.FRDRV('bernoulli', pspace, pspace.symbol)

        ## Properties
        assert rv.entropy == -q * ln(q) - p * ln(p)
        assert rv.kurtosis == (1 - 6 * p * q) / (p * q)
        assert rv.max == One
        assert rv.mean == p
        ## TODO: this test fails
        ## We need to re-implement median and/or ppf
        #assert rv.median == Zero if q > p else One if q < p else Half
        assert rv.min == Zero
        if q > p:
            assert rv.mode == Zero
        elif q < p:
            assert rv.mode == One
        else:
            assert rv.mode == Zero or rv.mode == One
        assert rv.skewness == (q - p) / sqrt(p * q)
        assert rv.std == sqrt(p * q)
        assert rv.support == set([0, 1])
        assert rv.variance == p * q

        ## Methods
        ## TODO: re-implement cdf for FRDRV
        # assert rv.cdf(-One) == Zero
        # assert rv.cdf(-Half) == Zero
        # assert rv.cdf(Zero) == q
        # assert rv.cdf(Half) == q
        # assert rv.cdf(One) == One
        # assert rv.cdf(One + Half) == One
        assert rv.mgf(t).equals(q + p * exp(t))


#@bench("drv.real.FRDRV", iterations=1)
def test_real_binomial():
    ns = sympy.sympify([1, 5, 100])
    ps = [Half / 2, Half, Half + Half / 2]
    for n, p in it.product(ns, ps):
        q = 1 - p
        pmf = lambda k: binomial(n, k) * p ** k * q ** (n - k)
        pspace = drv.pspace.FDPSpace([pmf(k) for k in xrange(n + 1)])
        rv = drv.real.FRDRV('binomial', pspace, pspace.symbol)

        ## Entropy is too complex so we skip it
        assert rv.kurtosis == (1 - 6 * p * q) / (n * p * q)
        assert rv.max == n
        assert rv.mean == n * p
        ## We need to re-implement median and/or ppf
        # assert rv.median == floor(np) or rv.median == ceiling(np)
        assert rv.min == 0
        assert rv.skewness == (1 - 2 * p) / (n * p * q) ** Half
        assert rv.std == (n * p * q) ** Half
        assert rv.variance == n * p * q
        ## TODO: build appropriate tests for binomial CDF
        assert rv.mgf(0) == One
        ## TODO: thes fail
        # assert rv.mgf(1) == (q + p * exp(1)) ** n
        # assert rv.mgf(3) == (q + p * exp(3)) ** n


def test_real_uniform():
    lefts = sympy.sympify([-3, 0, 2])
    ns = sympy.sympify([3, 7])
    for a, n in it.product(lefts, ns):
        b = a + n - 1
        ps = [1] * n
        pspace = drv.pspace.FDPSpace(ps)
        func = pspace.symbol + a
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


## TODO: check what's so slow about it
@slow
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

