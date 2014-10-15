"""
.. real.py
"""

## Tools
import operator as op
import drv.tools as tools

## Framework
import drv.pspace
import drv.core

## Math
import numpy as np


## Messages
EMPTY_SUPPORT = "The support may not be empty."
REAL_SUPPORT = "The support must contain reals only."
PPF_DOMAIN = "A PPF is defined on (0,1] only."

inf = float('inf')


class RDRV(drv.core.DRV):
    """ A real-valued Discrete Random Variable. May have finite or infinite
    support.

    *name* is an identifier for the random variable. """

    ## ----- Data Model ----- ##

    def __nonzero__(self):
        ## TODO: rethink that
        if self.pmf(0) == 1:
            return False
        return True

    ## ----- Probability Properties ----- ##

    def entropy(self):
        """ The entropy of the random variable. """
        raise NotImplementedError

    def max(self):
        """ The maximum of the random variable. """
        raise NotImplementedError

    @property
    def mean(self):
        """ The mean of the random variable. """
        return self.pspace.integrate(self.func)

    @property
    def median(self):
        """ The median of the random variable.

        .. warning:: the median is not necessarily unique. If more than one
        median exists, this is an arbitrary median (in fact, the PPF of 0.5 is
        returned). """
        return self.ppf(0.5)

    def min(self):
        """ The minimum of the random variable. """
        raise NotImplementedError

    @property
    def std(self):
        """ The standard deviation of the random variable. """
        return self.variance ** 0.5

    @property
    def variance(self):
        """ The variance of the random variable. """
        mean = self.mean
        return self.pspace.integrate(lambda x: (self.func(x) - mean) ** 2)

    ## ----- Probability Methods ----- ##

    def cdf(self, k):
        """ Return the cumulative distribution function at *k*. """
        raise NotImplementedError

    def expectation(self, function):
        """ Return the expected value of a function *function* with respect to
        the distribution of the random variable. *function* should be a
        function of one argument. """
        raise NotImplementedError

    def _dmgf(self, n=0):
        """ Return the *n*'th derivative of the moment-generating function. """
        ## Derivatives should be added per distribution
        if n > 0:
            raise NotImplementedError

        def mgf(t, rv=self):
            return (np.e ** (t * rv)).mean

        return mgf

    def mgf(self, t):
        """ Return the moment-generating function at *t*. """
        return self._dmgf(t)

    def moment(self, n):
        """ Return the *n*'th non-central moment of the random variable. """
        return self._dmgf(n)(0)

    def pr(self, event):
        """ Return the probability of *event*; *event* is a boolean function of
        the value of the random variable. This is in fact a synonym of
        ``expectation``.  """
        return self.expectation(event)

    def sf(self, k):
        """ Return the survival function at *k*. """
        return 1 - self.cdf(k)

    ## ----- Probability Inverse Methods ----- ##

    def isf(self, q):
        """ Return the inverse survival function at *q*. """
        ## TODO: think of how to formalize this
        raise NotImplementedError

    def ppf(self, q):
        """ Return the percent point function (inverse CDF) at *q*. Formally,
        this is the infimum over all x's in the real line for which *q* is at
        most the CDF of x. """
        raise NotImplementedError

    ## ----- Probability Log Methods ----- ##

    def logcdf(self, k):
        """ Return the log of the cumulative distribution function at *k*. """
        return np.log(self.cdf(k))

    def logsf(self, k):
        """ Return the log of the survival function at *k*. """
        return np.log(self.sf(k))


class FRDRV(drv.core.FDRV, RDRV):
    def _initialize(self, xs, ps):
        """ Set, sort and check *xs* and *ps*, ignoring values with zero
        probability, normalizing the probabilities. """
        ## Check for non-empty support
        if not xs:
            raise ValueError(EMPTY_SUPPORT)

        xs = tuple(xs)

        ## Make them floats
        f_xs = tuple(float(x) for x in xs)
        if not f_xs == xs:
            raise ValueError(REAL_SUPPORT)

        super(FRDRV, self)._initialize(f_xs, ps)

        ## Sort
        self.xs, self.ps = tools.unzip(sorted(zip(self.xs, self.ps)))

    ## ----- Probability Properties ----- ##

    @property
    def entropy(self):
        """ The (natural) entropy of the random variable. """
        return -sum(p * np.log(p) for p in self.ps)

    @property
    def max(self):
        """ The maximum of the random variable. """
        return self.xs[-1]

    @property
    def mean(self):
        """ The mean of the random variable. """
        return sum(x * p for x, p in self.items)

    @property
    def min(self):
        """ The minimum of the random variable. """
        return self.xs[0]

    @property
    def variance(self):
        """ The variance of the random variable. """
        return sum(p * x ** 2 for x, p in self.items) - self.mean ** 2

    ## ----- Probability Methods ----- ##

    def cdf(self, k):
        """ Return the cumulative distribution function at *k*. """
        return sum(p for x, p in self.items if x <= k)

    def expectation(self, function):
        """ Return the expected value of a function *function* with respect to
        the distribution of the random variable. *function* should be a
        function of one argument. """
        return sum(function(x) * p for x, p in self.items)

    ## ----- Probability Inverse Methods ----- ##

    def isf(self, q):
        """ Return the inverse survival function at *q*. """
        ## TODO: think of how to formalize this
        raise NotImplementedError

    ## ----- Operations ----- ##

    def unop(self, operator, name, klass=None, flatten=False):
        """ Return a new discrete random variable, which is the result of
        *operator* on *self*. This is in fact an alias for the map method. """
        return self.map(operator, name, klass=klass, flatten=flatten)

    def binop(self, other, operator, name, reverse=False, klass=None,
              flatten=False):
        """ return a new discrete random variable, which is the result of
        *operator* on *self* and *other* (or on *other* and *self*, if
        *reverse*). *other* may be a float, in which case we treat it as a
        constant real random variable.

        If the operation is not supported, raise ValueError. """
        ## 'other' is not a random variable, we try to make it such
        if not isinstance(other, drv.core.DRV):

            ## Try to turn the float into a constant random variable
            try:
                if other.real == other:
                    other = DegenerateRDRV(other)
            except AttributeError:
                pass

        ## We don't know how to handle it
        if not isinstance(other, FRDRV):
            return super(FRDRV, self).binop(other, operator, name, klass=klass,
                                            flatten=flatten)

        ## We know how to handle it
        ## Create the relevant product pspace
        pspaces = set(self.pspace.pspaces + other.pspace.pspaces)
        pspace = drv.pspace.ProductDPSpace(*pspaces)

        ## Reverse if needed
        if reverse:
            a, b = other, self
        else:
            a, b = self, other

        ## Create the new func
        def func(*ks):
            if len(ks) != len(pspaces):
                raise ValueError
            sample = dict(zip(pspace.pspaces, ks))
            return operator(a.pfunc(sample), b.pfunc(sample))

        klass = klass or FRDRV
        _drv = klass(name, pspace, func)
        if not flatten:
            return _drv
        return _drv.flatten()

    ## ----- Arithmetic ----- ##

    def __abs__(self, name="|{_0}|", klass=None):
        return self.unop(abs, name, klass=klass)

    def __add__(self, other, name="({_0})+({_1})", klass=None):
        ## When adding 0, do nothing
        if not other:
            return self

        return self.binop(other, op.add, name, klass=klass)

    def __and__(self, other, name="({_0})&({_1})", klass=None):
        ## When other is self, this is actually doing nothing
        if other is self:
            return self

        return self.binop(other, min, name, klass=klass)

    def __div__(self, other, name="({_0})//(_{1})", klass=None):
        ## When other is self, this is constant 1, unless self may be zero
        if other is self:
            if self.pmf(0) > 0:
                raise ZeroDivisionError
            return DegenerateRDRV(1)

        return self.binop(other, op.truediv, name, klass=klass)

    def __eq__(self, other, name="({_0})=({_1})", klass=None):
        ## When other is self, this is constant True
        if other is self:
            return DegenerateRDRV(1)

        return self.binop(other, op.eq, name, klass=klass)

    def __floordiv__(self, other, name="({_0})//(_{1})", klass=None):
        ## When other is self, this is constant 1
        if other is self:
            return DegenerateRDRV(1)

        return self.binop(other, op.floordiv, name, klass=klass)

    def __ge__(self, other, name="({_0})>=({_1})", klass=None):
        ## When other is self, this is constant True
        if other is self:
            return DegenerateRDRV(1)

        return self.binop(other, op.ge, name, klass=klass)

    def __gt__(self, other, name="({_0})>({_1})", klass=None):
        ## When other is self, this is constant False
        if other is self:
            return DegenerateRDRV(0)

        return self.binop(other, op.gt, name, klass=klass)

    def __le__(self, other, name="({_0})<=({_1})", klass=None):
        ## When other is self, this is constant True
        if other is self:
            return DegenerateRDRV(1)

        return self.binop(other, op.le, name, klass=klass)

    def __lt__(self, other, name="({_0})<({_1})", klass=None):
        ## When other is self, this is constant False
        if other is self:
            return DegenerateRDRV(0)

        return self.binop(other, op.lt, name, klass=klass)

    def __mod__(self, other, name="({_0})%(_{1})", klass=None):
        ## When other is self, this is constant 0
        if other is self:
            return DegenerateRDRV(0)

        return self.binop(other, op.mod, name, klass=klass)

    def __mul__(self, other, name="({_0})*({_1})", klass=None):
        ## When multiplying by 1, do nothing
        if isinstance(other, (float, int)):
            if other == 1:
                return self

        ## When multiplying by 0, this is constant 0
        if not other:
            return DegenerateRDRV(0)

        return self.binop(other, op.mul, name, klass=klass)

    def __ne__(self, other, name="({_0})!=({_1})", klass=None):
        ## When other is self, this is constant False
        if other is self:
            return DegenerateRDRV(0)

        return self.binop(other, op.ne, name, klass=klass)

    def __neg__(self, name="-({_0})"):
        return self.unop(op.neg, name)

    def __or__(self, other, name="({_0})|({_1})", klass=None):
        ## When other is self, this is actually doing nothing
        if other is self:
            return self

        return self.binop(other, max, name, klass=klass)

    def __pos__(self):
        return self

    def __pow__(self, other, name="({_0})**({_1})", klass=None):
        ## Note that op.pow(0, 0) is 1 in Python!
        return self.binop(other, op.pow, name, klass=klass)

    def __sub__(self, other):
        ## When other is self, this is constant 0
        if other is self:
            return DegenerateRDRV(0)

        return self.binop(other, op.sub, "({_0})-({_1})")

    __truediv__ = __div__

    def compare(self, other):
        ## When other is self, this is constant 0
        if other is self:
            return DegenerateRDRV(0)

        return self.binop(other, cmp, "({_0})<>({_1})")

    ## ----- Reverse Arithmetic ----- ##

    def __radd__(self, other, name="({_0})+({_1})", klass=None):
        ## When adding 0, do nothing
        if other == 0:
            return self

        return self.binop(other, op.add, name, reverse=True, klass=klass)

    def __rand__(self, other, name="({_0})&({_1})", klass=None):
        return self.binop(other, min, name, reverse=True, klass=klass)

    def __rmul__(self, other, name="({_0})*({_1})", klass=None):
        ## When multiplying by 1, do nothing
        if other == 1:
            return self

        return self.binop(other, op.mul, name, reverse=True, klass=klass)

    def __ror__(self, other, name="({_0})|({_1})", klass=None):
        return self.binop(other, max, name, reverse=True, klass=klass)

    def __rpow__(self, other, name="({_0})**({_1})", klass=None):
        ## When other is self, we're not handling it properly yet...
        if other is self:
            raise NotImplementedError

        return self.binop(other, op.pow, name, reverse=True, klass=klass)

    def __rsub__(self, other, name="({_0})-({_1})", klass=None):
        return self.binop(other, op.sub, name, reverse=True, klass=klass)


class DegenerateRDRV(FRDRV):
    def __init__(self, k):
        super(DegenerateRDRV, self).__init__(str(k), [k], [1])

