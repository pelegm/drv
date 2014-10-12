"""
.. pspace.py

Probability spaces.
"""

## Tools
import drv.tools

import itertools as it
import numpy as np
import sympy
import warnings


## Messages
INF_PROB = "Cannot instantiate PSpace with diverging probability."
NEG_PROB = "Cannot instantiate PSpace with negative probability."
NIE_PROB = "Could not determine if p is nonnegative."
ZERO_PROB = "Cannot instantiate PSPace with zero-sum probabilities."


## Tools
def _normalize(p, precision, strict=False):
    """ Return a normalized version of *p*, up to the given *precision*.

    We use SymPy tools to verify and normalize p. """
    ## This is an attempt to verify that p is always positive
    ## In many cases, this does not work. If this is such a case, raise
    ## ValueError if strict, or assume the minimum is 0 otherwise.
    ##
    ## See for example https://github.com/sympy/sympy/issues/8221 
    k = sympy.Symbol('k', integer=True, nonnegative=True)
    try:
        nonneg = sympy.solve(p(k) >= 0)
    except NotImplementedError:
        if strict:
            raise ValueError(NIE_PROB)
        else:
            nonneg = True
    if not nonneg in (True,):
        raise ValueError(NEG_PROB)

    n = sympy.Symbol('n', integer=True, nonnegative=True)
    sym_sum = sympy.Sum(p(n), (n, 0, sympy.oo)).doit()

    ## The following does not always work, as there are some SymPy bugs
    ## See for example https://github.com/sympy/sympy/issues/8219
    ## In case it fails with an AttributeError, we warn but assume p is ok as
    ## is.
    try:
        _sum = sym_sum.evalf(n=precision)
        if _sum.is_infinite:
            raise ValueError(INF_PROB)
        f_sum = float(_sum)
    except AttributeError:
        warnings.warn("SymPy bug #8219; assumes p is normalized.")
        return p

    ## Don't allow 0 total probability
    if not f_sum:
        raise ValueError(ZERO_PROB)

    def _p(k, p=p, f_sum=f_sum):
        return p(k) / f_sum

    return _p


def _f_normalize(ps):
    """ Return a normalized version of *ps*. """
    ## Verify none of the ps is negative
    if min(ps) < 0:
        raise ValueError(NEG_PROB)

    psum = sum(ps)
    if not psum:
        raise ValueError(ZERO_PROB)

    return [1.0 * p / psum for p in ps]


class DPSpace(object):
    """ A general discrete probability space.

    A probability space, in its most general settings, is a triple (Omega,F,P),
    in which O is a sample space (any set), F is a set of events which is a
    sigma-algebra (closed under complement and countable unions and
    intersections), and P is a probability function which assigns a real number
    from 0 to 1 to each event. The probability function P must return 0 for the
    empty set, 1 for the whole set, and have the countable additivity property.

    In practice, this module considers only discrete (countable) probability
    spaces, so for this class the following assumptions are made:

    1. The sample space Omega is the set of natural numbers (including 0)
    2. The events set is the power set of Omega; however, we allow the
       probability function P raise NotImplementedError for events for which
       the probability calculation is difficult
    3. The probability function P is described (by default) by the probability
       function p which is a defined as p(k) = P({k}).

    Thus, to create a :class:`DPSpace`, one only needs to provide the
    probability function p. """
    finite = False

    def __init__(self, p, precision=10):
        """ Keep the probability function p, but normalize it first, using the
        given *precision*. """
        self.p = _normalize(p, precision=precision, strict=False)
        self.pspaces = self,

    def P(self, event):
        """ Return the probability of *event*.

        It is assumed that *event* is a finite iterable of naturals. """
        ## TODO: implement infinite events
        return sum(self.p(k) for k in event)


class FDPSpace(DPSpace):
    """ A finite (general) discrete probability space.

    The following assumptions are made:

    1. The sample space Omega is the set {0,...,n-1}, where n is the length of
       the given iterable of probabilities
    2. The events set is the power set of Omega
    3. The probability function P is described (by default) by the probability
       function p which is a defined as p(x) = P({x}).

    Thus, to create a :class:`FDPSpace`, one only needs to provide the
    probability function p. For practical purposes, that function is passed as
    a finite iterable of values, which correspond to the probabilities of
    Omega. """
    finite = True

    def __init__(self, ps):
        self.ks, self.ps = drv.tools.unzip(enumerate(_f_normalize(ps)))
        self.pks = [(k,) for k in self.ks]
        self.pspaces = self,

    def p(self, k):
        try:
            return self.ps[k]
        except IndexError:
            return 0
        except TypeError:
            return 0


class ProductDPSpace(DPSpace):
    """ A product space of (general) discrete probability spaces. """
    def __init__(self, *pspaces):
        self.pspaces = pspaces
        self.finite = all(pspace.finite for pspace in pspaces)

        ## If finite, should also have a list of packed ks
        if self.finite:
            self.pks = list(it.product(*(pspace.ks for pspace in pspaces)))

    def p(self, *ks):
        if len(ks) != len(self.pspaces):
            return 0.
        return np.prod([psp.p(k) for psp, k in zip(self.pspaces, ks)])

