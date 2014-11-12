"""
.. real.py
"""

## Tools
import operator as op
import drv.tools as tools

## Framework
import drv.pspace
import drv.rv

## Math
import numpy as np
import sympy


## Messages
EMPTY_SUPPORT = "The support may not be empty."
REAL_SUPPORT = "The support must contain reals only."
PPF_DOMAIN = "A PPF is defined on (0,1] only."


## Constants
Zero = sympy.S.Zero
Half = sympy.S.Half
One = sympy.S.One
inf = float('inf')


class RDRV(drv.rv.DRV):
    """ A real-valued Discrete Random Variable. May have finite or infinite
    support.

    *name* is an identifier for the random variable. """

    ## ----- Probability Properties ----- ##

    @property
    def entropy(self):
        """ The (natural) entropy of the random variable. """
        return self.pspace.entropy

    @property
    def kurtosis(self):
        """ The (excessive) kurtosis of the random variable. """
        return self.standardised_moment(4) - 3

    @property
    def max(self):
        """ The maximum of the random variable. """
        ## This may be difficult to implement in the general case
        raise NotImplementedError

    @property
    def mean(self):
        """ The mean of the random variable. """
        ## The mean is the first raw moment
        return self.moment(1)

    @property
    def median(self):
        """ The median of the random variable.

        .. warning:: the median is not necessarily unique. If more than one
        median exists, this is an arbitrary median (in fact, the PPF of 0.5 is
        returned). """
        return self.ppf(0.5)

    @property
    def min(self):
        """ The minimum of the random variable. """
        ## This may be difficult to implement for the general case
        raise NotImplementedError

    @property
    def skewness(self):
        """ The skewness of the random variable. """
        ## The skewness is the third standardised moment
        return self.standardised_moment(3)

    @property
    def std(self):
        """ The standard deviation of the random variable. """
        return self.variance ** Half

    @property
    def variance(self):
        """ The variance of the random variable. """
        ## The variance is the second central moment
        return self.central_moment(2)

    ## ----- Probability Methods ----- ##

    def cdf(self, k):
        """ Return the cumulative distribution function at *k*. """
        cumulative = lambda *w: indicator(self.func(*w) <= k)
        return self.pspace.integrate(cumulative)

    def central_moment(self, n):
        """ Return the *n*'th central moment. """
        return self.pspace.integrate(self._moment_func(n, self.mean))

    def mgf(self, t):
        """ Return the moment-generating function at *t*. """
        return self.pspace.integrate(lambda x: sympy.exp(t * self.func(x)))

    def _moment_func(self, n, c=Zero, s=One):
        def mfunc(*x):
            return ((self.func(*x) - c) / s) ** n
        return mfunc

    def moment(self, n):
        """ Return the *n*'th raw moment. """
        return self.pspace.integrate(self._moment_func(n))

    def sf(self, k):
        """ Return the survival function at *k*. """
        return 1 - self.cdf(k)

    def standardised_moment(self, n):
        """ Return the *n*'th standardised moment. """
        return self.pspace.integrate(self._moment_func(n, self.mean, self.std))

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
        ## If other is a scalar, we do a quicker unop instead
        if isinstance(other, (int, float)):

            ## Reverse if needed
            if reverse:
                _op = lambda x: operator(other, x)
            else:
                _op = lambda x: operator(x, other)

            return self.unop(_op, name, klass=klass, flatten=flatten)

        ## We don't know how to handle it
        if not isinstance(other, RDRV):
            raise NotImplementedError

        ## We know how to handle it
        ## Create the relevant product pspace
        pspaces = frozenset(self.pspace.pspaces + other.pspace.pspaces)
        pspace = drv.pspace.ProductDPSpace(*pspaces)

        ## Reverse if needed
        if reverse:
            a, b = other, self
        else:
            a, b = self, other

        ## Create the new func
        def func(*ks):
            if len(ks) != len(pspaces):
                raise ValueError("{} pspaces and {} ks".format(len(pspaces),
                    len(ks)))
            sample = dict(zip(pspace.pspaces, ks))
            return operator(a.sfunc(sample), b.sfunc(sample))

        klass = klass or self.__class__
        _drv = klass(name, pspace, func)
        if not flatten:
            return _drv
        return _drv.flatten()

    ## ----- Arithmetic ----- ##

    def abs(self, name, klass=None):
        return self.unop(op.abs, name, klass=klass)

    def __abs__(self, name="|{0}|", klass=None):
        return self.abs("|{0}|".format(self))

    def add(self, other, name, klass=None):
        ## When adding 0, do nothing
        ## TODO: rethink
        if not other:
            return self

        return self.binop(other, op.add, name, klass=klass)

    def __add__(self, other):
        return self.add(other, "({0})+({1})".format(self, other))

    def and_(self, other, name, klass=None):
        ## When other is self, this is actually doing nothing
        if other is self:
            return self

        return self.binop(other, min, name, klass=klass)

    def __and__(self, other, name):
        return self.and_(other, "({0})&({1})".format(self, other))

    def compare(self, other, name, klass=None):
        ## When other is self, this is constant 0
        if other is self:
            return degenerate_rdrv(0)

        return self.binop(other, cmp, name, klass=klass)

    def div(self, other, name, klass=None):
        ## When other is self, this is constant 1, unless self may be zero
        if other is self:
            if self.pmf(0) > 0:
                raise ZeroDivisionError
            return degenerate_rdrv(1)

        return self.binop(other, op.truediv, name, klass=klass)

    def __div__(self, other):
        return self.div(other, "({0})/({1})".format(self, other))

    def eq(self, other, name, klass=None):
        ## When other is self, this is constant True
        if other is self:
            return degenerate_rdrv(1)

        return self.binop(other, op.eq, name, klass=klass)

    def __eq__(self, other):
        return self.eq(other, "({0})=({1})".format(self, other))

    def floordiv(self, other, name, klass=None):
        ## When other is self, this is constant 1, unless self may be zero
        if other is self:
            if self.pmf(0) > 0:
                raise ZeroDivisionError
            return degenerate_rdrv(1)

        return self.binop(other, op.floordiv, name, klass=klass)

    def __floordiv__(self, other):
        return self.floordiv(other, "({0})//({1})".format(self, other))

    def ge(self, other, name, klass=None):
        ## When other is self, this is constant True
        if other is self:
            return degenerate_rdrv(1)

        return self.binop(other, op.ge, name, klass=klass)

    def __ge__(self, other, name):
        return self.ge(other, "({0})>=({1})".format(self, other))

    def gt(self, other, name, klass=None):
        ## When other is self, this is constant False
        if other is self:
            return degenerate_rdrv(0)

        return self.binop(other, op.gt, name, klass=klass)

    def __gt__(self, other):
        return self.gt(other, "({0})>({1})".format(self, other))

    def le(self, other, name, klass=None):
        ## When other is self, this is constant True
        if other is self:
            return degenerate_rdrv(1)

        return self.binop(other, op.le, name, klass=klass)

    def __le__(self, other):
        return self.le(other, "({0})<=({1})".format(self, other))

    def lt(self, other, name, klass=None):
        ## When other is self, this is constant False
        if other is self:
            return degenerate_rdrv(0)

        return self.binop(other, op.lt, name, klass=klass)

    def __lt__(self, other):
        return self.lt(other, "({0})<({1})".format(self, other))

    def mod(self, other, name, klass=None):
        ## When other is self, this is constant 0
        if other is self:
            return degenerate_rdrv(0)

        return self.binop(other, op.mod, name, klass=klass)

    def __mod__(self, other):
        return self.mod(other, "({0})%({1})".format(self, other))

    def mul(self, other, name, klass=None):
        return self.binop(other, op.mul, name, klass=klass)

    def __mul__(self, other):
        return self.mul(other, "({0})*({1})".format(self, other))

    def ne(self, other, name, klass=None):
        ## When other is self, this is constant False
        if other is self:
            return degenerate_rdrv(0)

        return self.binop(other, op.ne, name, klass=klass)

    def __ne__(self, other):
        return self.ne(other, "({0})!=({1})".format(self, other))

    def neg(self, name, klass=None):
        return self.unop(op.neg, name, klass=klass)

    def __neg__(self):
        return self.neg("-({0})")

    def or_(self, other, name, klass=None):
        ## When other is self, this is actually doing nothing
        if other is self:
            return self

        return self.binop(other, max, name, klass=klass)

    def __or__(self, other):
        return self.or_(other, "({0})|({1})".format(self, other))

    def __pos__(self):
        return self

    def pow(self, other, name, klass=None):
        ## Note that op.pow(0, 0) is 1 in Python! (and in sympy)
        return self.binop(other, op.pow, name, klass=klass)

    def __pow__(self, other):
        return self.pow(other, "({0})**({1})".format(self, other))

    def sub(self, other, name, klass=None):
        ## When other is self, this is constant 0
        if other is self:
            return degenerate_rdrv(0)

        return self.binop(other, op.sub, name, klass=klass)

    def __sub__(self, other):
        return self.sub(other, "({0})-({1})".format(self, other))

    __truediv__ = __div__


class FRDRV(drv.rv.FDRV, RDRV):

    ## ----- Probability Properties ----- ##

    @property
    def max(self):
        """ The maximum of the random variable. """
        return max(self.support)

    @property
    def min(self):
        """ The minimum of the random variable. """
        return min(self.support)

    ## ----- Probability Inverse Methods ----- ##

    def isf(self, q):
        """ Return the inverse survival function at *q*. """
        ## TODO: think of how to formalize this
        raise NotImplementedError

    ## ----- Reverse Arithmetic ----- ##

    def __radd__(self, other, name="({0})+({1})", klass=None):
        ## When adding 0, do nothing
        if other == 0:
            return self

        return self.binop(other, op.add, name, reverse=True, klass=klass)

    def __rand__(self, other, name="({0})&({1})", klass=None):
        return self.binop(other, min, name, reverse=True, klass=klass)

    def __rmul__(self, other, name="({0})*({1})", klass=None):
        ## When multiplying by 1, do nothing
        if other == 1:
            return self

        return self.binop(other, op.mul, name, reverse=True, klass=klass)

    def __ror__(self, other, name="({0})|({1})", klass=None):
        return self.binop(other, max, name, reverse=True, klass=klass)

    def __rpow__(self, other, name="({0})**({1})", klass=None):
        ## When other is self, we're not handling it properly yet...
        if other is self:
            raise NotImplementedError

        return self.binop(other, op.pow, name, reverse=True, klass=klass)

    def __rsub__(self, other, name="({0})-({1})", klass=None):
        return self.binop(other, op.sub, name, reverse=True, klass=klass)


class DegenerateRDRV(FRDRV):
    """ A degenerate RDRV is a finite RDRV which supports a single value. """


def degenerate_rdrv(value):
    """ Return a :class:`DegenerateRDRV` which supports *value*. """
    pspace = drv.pspace.DegeneratePSpace()
    func = lambda x: float(value)
    return DegenerateRDRV(str(value), pspace, func)

