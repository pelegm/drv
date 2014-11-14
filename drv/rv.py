"""
.. core.py

Discrete random variables - core module.
"""

import collections as col
import drv.tools
import drv.pspace

## Symbolic
import sympy


## Symbolic tools
from drv.functions import x, Lambda, Piecewise, indicator
x = sympy.Symbol('x')
Lambda = sympy.Lambda
Piecewise = sympy.Piecewise


def cumulative(v):
    return Lambda(x, sympy.Piecewise((1, x <= v, (0, True))))


class DRV(object):
    """ A general Discrete Random Variable. Treated as categorical. May have
    finite or infinite support.

    A discrete random variable is simply a probability space equipped with a
    function from that probability space into some outcome set, which is
    usually, but not always, the set of reals.

    A DRV comes with a *name*, which identifies the variable. In the future,
    this may be required to be unique. A DRV construction also involves a
    *pspace*, a relevant probability space, and a *func*, which is a symbolic
    expression, involving (possibly) the pspace's symbol. """
    def __init__(self, name, pspace, func):
        self.name = name
        self.pspace = pspace

        ## The expression may be a basic python type; we make sure it is a
        ## symbolic expression
        try:
            self.func = sympy.sympify(func)
        except sympy.SympifyError:
            raise ValueError("Could not sympify {}".format(func))

    def eval(self, sample):
        """ Return the substitution result of the sample *s* (which is an
        pair of (symbols,outcomes) iterables) in self's func. """
        return self.func.subs(zip(*sample))

    def sfunc(self, sample):
        """ Return the result of ``func`` on the sampled data, where *sample*
        must contain all coordinates of self's probability space, but may also
        contain coordinates of other probability spaces, which should be
        ignored. In case not all coordinates are included in *sample*, raise
        ``ValueError``.

        *sample* is a dictionary pointing probability spaces to contained
        outcomes. """
        ws = []
        for pspace in self.pspace.pspaces:
            try:
                ws.append(sample[pspace])
            except KeyError:
                raise ValueError("Missing coordinates.")
        return self.func(*ws)

    ## ----- Representation ----- ##

    @property
    def _cls(self):
        """ The class name. """
        return self.__class__.__name__

    def __repr__(self):
        return "{self._cls}({self.name})".format(self=self)

    def __str__(self):
        return self.name

    ## ----- Probability Properties ----- ##

    @property
    def mode(self):
        """ The value at which the probability mass function takes its maximum
        value.

        .. warning:: the mode is not necessarily unique. If more than one mode
        exists, this is an arbitrary mode. """
        raise NotImplementedError

    @property
    def support(self):
        """ The values at which the probability mass function is positive. """
        raise NotImplementedError

    ## ----- Probability Methods ----- ##

    def pmf(self, k):
        """ Return the probability mass function at *k*. """
        # ind = lambda w: indicator(self.eval(w) == k)
        # return self.pspace.integrate(ind)
        return self.pspace.integrate(indicator(k)(self.func))

    ## ----- Operations ----- ##

    def binop(self, other, operator, name, klass=None, flatten=False):
        """ return a new discrete random variable, which is the result of
        *operator* on *self* and *other*. """
        ## 'other' is not a random variable, we don't know how to handle that
        if not isinstance(other, DRV):
            return NotImplemented

        ## We may need to be able to handle it
        raise NotImplementedError

    def flatten(self):
        """ Return a random variable with a new probability space whose sample
        set is the inverse image of func. """
        raise NotImplementedError

    def map(self, function, name, klass=None, flatten=False):
        """ Return a random variable whose values are the application of
        *function* to self's values. """
        klass = klass or self.__class__
        # func = lambda x: function(self.func(x))
        func = function(self.func)
        _drv = klass(name, self.pspace, func)
        if not flatten:
            return _drv
        return _drv.flatten()


class FDRV(DRV):
    """ A finite (general) Discrete Random Variable. Treated as categorical.

    *name* is an identifier for the random variable. *xs* are the possible
    values (categories), and *ps* are the distributions. *xs* and *ps* are
    checked for correctedness, and *ps* are normalized. """
    def __init__(self, name, pspace, func):
        if not pspace.is_finite:
            raise ValueError("The probability space must be finite.")

        super(FDRV, self).__init__(name, pspace, func)

    ## ----- Probability Properties ----- ##

    @property
    def mode(self):
        """ The value at which the probability mass function takes its maximum
        value.

        .. warning:: the mode is not necessarily unique. If more than one mode
        exists, this is an arbitrary mode. """
        return max(self.support, key=lambda k: self.pmf(k))

    @property
    def support(self):
        """ The values at which the probability mass function is positive. """
        ## The probability space provides a .samples method which returns all
        ## samples; each sample is a pair of (symbols,outcomes) iterables
        sup = set()
        for w in self.pspace.Omega:
            if self.pspace.p(*w) > 0:
                sup.add(self.eval((self.pspace.symbols, w)))
        return frozenset(sup)

    ## ----- Probability Inverse Methods ----- ##

    def ppf(self, q):
        """ Return the percent point function (inverse CDF) at *q* Formally,
        this is the infimum over all x's in the real line for which *q* is at
        most the CDF of x. """
        if not 0 < q <= 1:
            raise ValueError(PPF_DOMAIN)

        ## TODO: This is extremely inefficient (o(n^2)) when the set of xs is
        ## large; we should probably consider using bisect here, to make it
        ## o(nlog(n))
        for x in self.xs:
            if self.cdf(x) >= q:
                return x

        ## Just to make sure some value is returned; may be bugged in case of
        ## rounding errors
        return self.xs[-1]

    ## ----- Probability Log Methods ----- ##

    def logpmf(self, k):
        """ Return the log of the probability mass function at *k*. """
        return np.log(self.pmf(k))

    ## ----- Operations ----- ##

    def flatten(self, name=None):
        """ Return a random variable with a new probability space whose sample
        set is the inverse image of func. """
        ks = sorted(self.support)
        ps = [self.pmf(k) for k in ks]

        name = name or self.name
        pspace = drv.pspace.FDPSpace(ps)
        func = lambda w: ks[w]
        return self.__class__(name, pspace, func)

