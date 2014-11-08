"""
.. pspace.py

Probability spaces.
"""

## Tools
import drv.tools

import itertools as it
import numpy as np
import warnings

## Symbolic
import sympy
import sympy.mpmath
sympify = sympy.sympify


## Messages
INF_PROB = "Cannot instantiate PSpace with diverging probability."
NEG_PROB = "Cannot instantiate PSpace with negative probability."
NIE_PROB = "Could not determine if p is nonnegative."
ZERO_PROB = "Cannot instantiate PSPace with zero-sum probabilities."
INTEGRATE_GENERAL = "Cannot integrate a general PSpace."


## Constants
oo = sympy.oo


## Tools
def _normalize(p, precision, strict=False):
    """ Return a normalized version of *p*, up to the given *precision*.

    We use SymPy tools to verify and normalize p. """
    ## This is an attempt to verify that p is always positive
    ## In many cases, this does not work. If this is such a case, raise
    ## ValueError if strict, or assume the minimum is 0 otherwise.
    ##
    ## See for example https://github.com/sympy/sympy/issues/8221 
    w = sympy.Symbol('w', integer=True, nonnegative=True)
    try:
        nonneg = sympy.solve(p(w) >= 0)
    except NotImplementedError:
        if strict:
            raise ValueError(NIE_PROB)
        else:
            nonneg = True
    if not nonneg in (True,):
        raise ValueError(NEG_PROB)

    n = sympy.Symbol('n', integer=True, nonnegative=True)
    summand = p(n)
    _sum = sympy.Sum(summand, (n, 0, oo)).doit()

    ## Sum is infinite, we should raise
    if _sum.is_infinite:
        raise ValueError(INF_PROB)

    ## Sum is zero, we should raise
    if _sum.is_zero:
        raise ValueError(ZERO_PROB)

    return sympy.Lambda(w, p(w) / _sum)


def _f_normalize(ps):
    """ Return a normalized version of *ps*. """
    ## Verify none of the ps is negative
    if min(ps) < 0:
        raise ValueError(NEG_PROB)

    ## Sympify
    s_ps = sympify(ps)

    psum = sum(s_ps)
    if not psum:
        raise ValueError(ZERO_PROB)

    return [p / psum for p in s_ps]


class DPSpace(object):
    """ A general discrete probability space.

    A probability space, in its most general settings, is a triple (Omega,F,P),
    in which O is a sample space (any set), F is a set of events which is a
    sigma-algebra (closed under complement and countable unions and
    intersections), and P is a probability function which assigns a real number
    from 0 to 1 to each event. The probability function P must return 0 for the
    empty set, 1 for the whole set, and have the countable additivity property.

    The following assumptions are made:

    1. The sample space is some discrete countable space
    2. The events set is the power set of Omega; however, we allow the
       probability function P raise NotImplementedError for events for which
       the probability calculation is difficult
    3. The probability function P is described (by default) by the probability
       function p which is a defined as p(k) = P({k}).

    """
    is_finite = False

    @property
    def Omega(self):
        raise NotImplementedError

    @property
    def F(self):
        raise NotImplementedError

    def P(self, event):
        """ Return the probability of *event*.

        It is assumed that *event* is a finite iterable of elements from the
        support. """
        ## TODO: implement infinite events
        return sum(self.p(w) for w in event)

    def p(self, w):
        """ Return the probability of the outcome *w*. """
        raise NotImplementedError

    @property
    def pspaces(self):
        return self,

    def integrate(self, func):
        """ Integrate *func* with respect to the probability measure
        represented by the probability space. """
        raise NotImplementedError(INTEGRATE_GENERAL)


class CDPSpace(DPSpace):
    """ A general countable discrete probability space.

    A probability space, in its most general settings, is a triple (Omega,F,P),
    in which O is a sample space (any set), F is a set of events which is a
    sigma-algebra (closed under complement and countable unions and
    intersections), and P is a probability function which assigns a real number
    from 0 to 1 to each event. The probability function P must return 0 for the
    empty set, 1 for the whole set, and have the countable additivity property.

    In practice, this class considers only discrete (countable) probability
    spaces having the naturals as their sample space, so for this class the
    following assumptions are made:

    1. The sample space Omega is the set of natural numbers (including 0)
    2. The events set is the power set of Omega; however, we allow the
       probability function P raise NotImplementedError for events for which
       the probability calculation is difficult
    3. The probability function P is described (by default) by the probability
       function p which is a defined as p(k) = P({k}).

    Thus, to create a :class:`CDPSpace`, one only needs to provide the
    probability function p. """
    def __init__(self, p, precision=10):
        """ Keep the probability function p, but normalize it first, using the
        given *precision*. """
        self.precision = precision
        self.p = _normalize(p, precision=self.precision, strict=False)
        # self.p = p

    def integrate(self, func):
        """ Integrate *func* with respect to the probability measure
        represented by the probability space.

        It is assumed that *func* is a function of natural numbers. If it is
        not, its restriction to the naturals is taken into consideration. """
        ## We need to return \int_{\Omega} f dp
        ## In the countable discrete case, this is simply the following
        ## infinite sum: \sum_{n=0}^\infty f(n)p(n)

        ## We try a symbolic summation
        n = sympy.Symbol('n', integer=True, nonnegative=True)
        summand = func(n) * self.p(n)
        _sum = sympy.Sum(summand, (n, 0, oo)).doit()

        ## Sum is still a sum, we need to evalf it
        if type(_sum) is sympy.Sum:

            ## This occasionaly fails due to various SymPy bugs
            ## See for example https://github.com/sympy/sympy/issues/8254
            try:
                _sum = sym_sum.evalf()
            except TypeError:
                raise NotImplementedError("SymPy bug #8254.")

        ## Sum is infinite, we should return it
        if _sum.is_infinite:
            return _sum

        ## Sum is real, we should return it
        if _sum.is_real:
            return _sum

        if sympy.mpmath.isnan(float(_sum)):
            raise NotImplementedError("nan bug. Tried to sum: {}".format(
                summand))

        raise NotImplementedError("Couldn't integrate. Got: {}".format(_sum))

    @property
    def entropy(self):
        """ The (natural) entropy of the probability space. """
        ## We try a symbolic summation
        n = sympy.Symbol('n', integer=True, nonnegative=True)
        p = self.p(n)
        sym_sum = -sympy.Sum(p * sympy.log(p), (n, 0, sympy.oo)).doit()
        _sum = sym_sum.evalf(n=self.precision)
        f_sum = float(_sum)
        return f_sum


class FDPSpace(CDPSpace):
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
    is_finite = True

    def __init__(self, ps):
        self._Omega, self.ps = drv.tools.unzip(enumerate(_f_normalize(ps)))

    @property
    def Omega(self):
        return set((w,) for w in self._Omega)

    @property
    def F(self):
        return set(drv.tools.powerset(self.Omega))

    def p(self, w):
        """ Return the probability of the outcome *w*. """
        try:
            return self.ps[w]
        except IndexError:
            return 0

    @property
    def entropy(self):
        """ The (natural) entropy of the probability space. """
        ## When taken from a finite sample, the entropy can be explicitly
        ## written as H(X) = -\sum_i p(i) \log{p(i)}
        return -sum(p * sympy.log(p) for p in self.ps).doit()

    def integrate(self, func):
        """ Integrate *func* with respect to the probability measure
        represented by the probability space.

        It is assumed that *func* is a function of natural numbers. If it is
        not, its restriction to the naturals is taken into consideration. """
        ## We need to return \int_{\Omega} f dp
        ## In the finite discrete case, this is simply the following finite
        ## sum: \sum_{w=0}^{n-1} f(w)p(w), where n is the length of 'ps'
        try:
            return sum(func(*w) * self.p(*w) for w in self.Omega)
        except AttributeError:
            print func, func(0), func(sympify(0)), func(sympify(1))
            print self.p, self.p(0), self.p(sympify(0)), self.p(sympify(1))
            raise


class DegeneratePSpace(FDPSpace):
    """ A degenerate probability space, which supports the value 0 only. """
    def __init__(self):
        super(DegeneratePSpace, self).__init__([1.0])

    def p(self, w):
        """ Return the probability of the outcome *w*. """
        return 1.0 if w == 0 else 0.0


class ProductDPSpace(DPSpace):
    """ A product space of (general) discrete probability spaces. """
    pspaces = ()

    def __init__(self, *pspaces):
        self.pspaces = pspaces
        self.is_finite = all(pspace.is_finite for pspace in pspaces)

    @property
    def Omega(self):
        omegas = (psp.Omega for psp in self.pspaces)
        return {sum(wt, ()) for wt in it.product(*omegas)}

    @property
    def F(self):
        if not self.is_finite:
            raise NotImplementedError

        return set(drv.tools.powerset(self.Omega))

    def p(self, *ws):
        """ Return the probability of the outcome *w*. """
        if len(ws) != len(self.pspaces):
            return 0.
        return np.prod([pspace.p(w) for pspace, w in zip(self.pspaces, ws)])

    def integrate(self, func):
        """ Integrate *func* with respect to the probability measure
        represented by the probability space. """
        if not self.is_finite:
            raise NotImplementedError

        ## If the product pspace is finite, we integrate normally
        return sum(func(*w) * self.p(*w) for w in self.Omega)

