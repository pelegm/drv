"""
.. drv.py
"""

## Abstract layer
import abc

## General tools
import collections as col
import itertools as it
import operator as op
import numpy as np
import drv.tools as tools


## Messages
LIST_LENGTHS = "Value list and probability list must have the same lengths."
NEG_PROB = "Cannot instantiate DRV with negative probability."


class DRV(object):
    """ A general Discrete Random Variable. Treated as categorical. May have
    finite or infinite support.

    *name* is an identifier for the random variable. """
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    @property
    def _cls(self):
        """ The class name. """
        return self.__class__.__name__

    def __repr__(self):
        return "{self._cls}({self.name})".format(self=self)

    def __str__(self):
        return self.name

    ## ----- Roll Methods ----- ##

    def __call__(self):
        return self.roll()

    def _roll(self):
        """ Return a result of a single roll. """
        ## The 1 - x is in order to generate a number in (0,1]
        return self.ppf(1 - np.random.random())

    def roll(self, n=None):
        """ Roll *n* times, if *n* is given, or else a single time; return the
        results as a list, if *n* is given, or as a single value otherwise. """
        if n is None:
            return self._roll()

        return list(self.rolls_gen(n=n))

    def rolls_gen(self, n=None):
        """ Return a generator of rolls. If *n* is given, limit the number of
        rolls by *n*. """
        if n is None:
            n = inf
        c = 0
        while c < n:
            c += 1
            yield self._roll()

    ## ----- Probability Properties ----- ##

    @abc.abstractproperty
    def mode(self):
        """ The value at which the probability mass function takes its maximum
        value.

        .. warning:: the mode is not necessarily unique. If more than one mode
        exists, this is an arbitrary mode. """
        raise NotImplementedError

    @abc.abstractproperty
    def support(self):
        """ The values at which the probability mass function is positive. """
        raise NotImplementedError

    ## ----- Probability Methods ----- ##

    @abc.abstractmethod
    def pmf(self, k):
        """ Return the probability mass function at *k*. """
        raise NotImplementedError

    ## ----- Operations ----- ##

    @abc.abstractmethod
    def map(self, function, name, klass=None):
        """ Return a random variable whose values are the application of
        *function* to self's values. """
        raise NotImplementedError


class FDRV(DRV):
    """ A finite (general) Discrete Random Variable. Treated as categorical.

    *name* is an identifier for the random variable. *xs* are the possible
    values (categories), and *ps* are the distributions. *xs* and *ps* are
    checked for correctedness, and *ps* are normalized. """
    def __init__(self, name, xs, ps):
        self.name = name
        self._initialize(xs, ps)

    def _initialize(self, xs, ps):
        """ Set and check *xs* and *ps*, ignoring values with zero probability,
        normalizing the probabilities. """
        ## Check for equal list lengths
        if len(xs) != len(ps):
            raise ValueError(LIST_LENGTHS)

        ## Check for negative probabilities
        if min(ps) < 0:
            raise ValueError(NEG_PROB)

        ## Remove zero probabilities
        p_xs, p_ps = tools.unzip((x, p) for x, p in it.izip(xs, ps) if p > 0)

        ## Aggregate equal values
        d = col.defaultdict(float)
        for x, p in zip(p_xs, p_ps):
            d[x] += p
        ag_xs, ag_ps = tools.unzip(d.iteritems())

        ## Normalize probabilities
        s_ps = sum(ag_ps)
        n_ps = [p / s_ps for p in ag_ps]

        self.xs, self.ps = ag_xs, n_ps

    @property
    def items(self):
        return zip(self.xs, self.ps)

    ## ----- Probability Properties ----- ##

    @property
    def mode(self):
        """ The value at which the probability mass function takes its maximum
        value.

        .. warning:: the mode is not necessarily unique. If more than one mode
        exists, this is an arbitrary mode. """
        return max(self.items, key=lambda t: t[1])[0]

    @property
    def support(self):
        """ The values at which the probability mass function is positive. """
        return self.xs

    ## ----- Probability Methods ----- ##

    def _cdf(self, i):
        """ Return the cumulative distribution function at the category whose
        index is *i*. """
        return sum(p for j, (x, p) in enumerate(self.items) if j <= i)

    def cdf(self, k):
        """ Return the cumulative distribution function at *k*. """
        try:
            return self._cdf(self.xs.index(k))
        except ValueError:
            raise ValueError("Category '{}' is not supported.".format(k))

    def pmf(self, k):
        """ Return the probability mass function at *k*. """
        try:
            i = self.xs.index(k)
        except ValueError:
            return 0.
        return self.ps[i]

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

    def binop(self, other, operator, name, klass=None):
        """ return a new discrete random variable, which is the result of
        *operator* on *self* and *other*. """
        ## 'other' is not a random variable, we don't know how to handle that
        if not isinstance(other, DRV):
            return NotImplemented

        ## We may need to be able to handle it
        raise NotImplementedError

    def map(self, function, name, klass=None):
        """ Return a random variable whose values are the application of
        *function* to self's values. Assign *name* to the resulted random
        variable, whose class is *klass* or self's class. """
        f_name = name.format(self=self)
        m_xs = [function(x) for x in self.xs]
        klass = klass or self.__class__
        return klass(name, m_xs, self.ps)


class TDRV(DRV):
    """ A Discrete Random Variable whose values are all tuples of a fixed
    (finite) length. It is thought of as a tuple of (general) random variables.
    """
    def __init__(self, drvs, name=None):
        self.drvs = drvs

        if not name:
            if len(self.drvs) == 1:
                name = "({},)".format(self.drvs[0].name)
            else:
                name = "(" + ",".join(drv.name for drv in self.drvs) + ")"
        self.name = name

        self.formatter = dict(("_{i}".format(i=i), drv) for i, drv in
                              enumerate(self.drvs))

    ## ----- Data Model ----- ##

    def __len__(self):
        return len(self.drvs)

    def __getitem__(self, key):
        if isinstance(key, slice):
            slice_attrs = []
            slice_attrs.append(key.start)
            slice_attrs.append(key.stop)
            slice_attrs.append(key.step)
            name = "{}[{}]".format(self.name, tools.slice_repr(key))
            return self.subtuple(key, name)
        return self.drvs[key]

    ## ----- Probability Properties ----- ##

    @property
    def mode(self):
        """ The value at which the probability mass function takes its maximum
        value.

        .. warning:: the mode is not necessarily unique. If more than one mode
        exists, this is an arbitrary mode. """
        return tuple(drv.mode for drv in self.drvs)

    ## ----- Probability Methods ----- ##

    def pmf(self, t):
        """ Return the probability mass function at *t*. """
        try:
            if len(t) != len(self):
                return 0.0
        except TypeError:
            return 0.0

        pmfs = [drv.pmf(k) for drv, k in zip(self.drvs, t)]
        return reduce(op.mul, pmfs, 1.0)

    ## ----- Operations ----- ##

    def subtuple(self, indices, name):
        """ Return the sub-tuple containing only *indices*. """
        drvs = [self.drvs[i] for i in indices]
        return self.__class__(drvs, name=name)


class TFDRV(TDRV):
    """ A Discrete Random Variable whose values are all tuples of a fixed
    (finite) length. It is thought of as a tuple of (general) finite random
    variables.
    """
    @property
    def xs(self):
        return list(it.product(*(drv.xs for drv in self.drvs)))

    @property
    def ps(self):
        return [self.pmf(x) for x in self.xs]

    ## ----- Probability Properties ----- ##

    @property
    def support(self):
        """ The values at which the probability mass function is positive. """
        return list(it.product(drv.support for drv in self.drvs))

    ## ----- Operations ----- ##

    def map(self, function, name, klass=None, unpack=False):
        """ Return a random variable whose values are the application of
        *function* to self's values. Assign *name* to the resulted random
        variable, whose class is *klass* or self's class. """
        f_name = name.format(**self.formatter)
        xs = self.xs
        ps = [self.pmf(x) for x in xs]
        if unpack:
            m_xs = [function(*x) for x in xs]
        else:
            m_xs = [function(x) for x in xs]
        klass = klass or self.__class__
        return klass(f_name, m_xs, ps)

