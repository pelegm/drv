"""
.. drv.py

Dice random variables; these are discrete (integer-valued) finite random
variables.

This module provides a simple (quite thin) wrapper around the extensive
scipy.stats module.
"""

## SciPy's random variable framework
import scipy.stats as ss

## Math
import numpy as np
inf = np.inf

## Data containers
import collections as col

## Python basics
import itertools as it

## For arithmetic
import operator as op


##################################
## ----- Helper Functions ----- ##
##################################

def unzip(zipped):
    """ Return a :term:`generator` reverses the work of zip/izip.

    :param zipped: the iterable to unzip.
    :type zipped: :term:`iterable` of :term:`iterables <iterable>`.
    :rtype: :term:`generator`

    Examples:

    >>> list(unzip(zip(xrange(3), xrange(2, 5))))
    [(0, 1, 2), (2, 3, 4)]
    >>> list(unzip(izip(xrange(3), xrange(2, 5))))
    [(0, 1, 2), (2, 3, 4)]

    .. note:: The returned elements of the generator are always tuples. This is
        a result of how :func:`zip` works.
    """
    return it.izip(*zipped)


##############################
## ----- Main Classes ----- ##
##############################

class DiscreteRandomVariable(object):
    """ A ``DiscreteRandomVariable`` is a wrapper for a integer-valued discrete
    random variable. """
    def __init__(self, name, rv=None, xs=None, ps=None):
        """ A ``DiscreteRandomVariable`` may be initialized either with a SciPy
        random variable *rv*, or with a list of values *xs* with matching
        probabilities *ps*. """
        if rv:
            self._initialize_with_rv(name, rv)
            return

        self._initialize_with_xp(name, xs, ps)

    def _initialize_with_rv(self, name, rv):
        """ Initialize the DRV with a SciPy random variable *rv*. It is assumed
        that *rv* is discrete and integer-valued. """
        dist = rv.dist

        ## Uniform distribution
        if type(dist) is ss.distributions.randint_gen:
            xs = range(rv.args[0], rv.args[1])
            ps = [rv.pmf(x) for x in xs]
            self._initialize_with_xp(name, xs, ps)
            return

        ## Binomial distribution
        if type(dist) is ss.distributions.binom_gen:
            xs = range(rv.args[0] + 1)
            ps = [rv.pmf(x) for x in xs]
            self._initialize_with_xp(name, xs, ps)
            return

        raise ValueError("Unknown distribution for {rv}.".format(rv=rv))

    def _initialize_with_xp(self, name, xs, ps):
        """ Initialize the DRV with explicit values and probabilities. """
        ## Remove any zero-probability values
        nz_xs, nz_ps = unzip((x, p) for x, p in zip(xs, ps) if ps > 0)

        ## Aggregate equal values
        d = col.defaultdict(float)
        for x, p in zip(nz_xs, nz_ps):
            d[x] += p
        ag_xs, ag_ps = unzip(d.iteritems())

        ## Normalize the probabilities, in case we have some error here
        ar_ps = np.array(ag_ps, dtype=float)
        n_ps = ar_ps / ar_ps.sum()

        self._rv = ss.rv_discrete(name=name, values=(ag_xs, n_ps))

    @property
    def name(self):
        """ The name of the random variable. """
        return self._rv.name

    @name.setter
    def name(self, new_name):
        """ Set a new name. """
        self._rv.name = new_name

    @property
    def xs(self):
        """ The values (support) of the random variable. """
        return self._rv.xk

    @property
    def ps(self):
        """ The probabilities of the random variable. """
        return self._rv.pk

    @property
    def values(self):
        """ The (value, probability) pairs of the random variable. """
        return zip(self._rv.xk, self._rv.pk)

    @property
    def range(self):
        """ The range of the random variable; from the minimum to the maximum
        possible values, inclusive. """
        return range(self.min, self.max + 1)

    ## ----- Roll Methods ----- ##

    def __call__(self):
        return self.roll()

    def _roll(self):
        """ Return a result of a single roll. """
        return self._rv.rvs()

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

    ## ----- Probability Methods ----- ##

    def cdf(self, k):
        """ Return the cumulative distribution function at *k*. """
        return self._rv.cdf(k)

    def expectation(self, func):
        """ Return the expected value of a function *func* with respect to the
        distribution of the random variable. *func* should be a function of one
        argument. """
        return self._rv.expect(func=func)

    def interval(self, alpha):
        """ Return the symmetric confidence interval (with parameter *alpha*)
        around the median. *alpha* must be in [0,1]. """
        return self._rv.interval(alpha=alpha)

    def moment(self, n):
        """ Return the n'th non-central moment of the random variable. """
        return self._rv.moment(n)

    def pmf(self, k):
        """ Return the probability mass function at *k*. """
        return self._rv.pmf(k)

    def pr(self, event):
        """ Return the probability of *event*; *event* is a boolean function of
        the value of the random variable. This is a synonym of ``expectation``.
        """
        return self.expectation(event)

    def sf(self, k):
        """ Return the survival function at *k*. """
        return self._rv.sf(k)

    ## ----- Probability Inverse Methods ----- ##

    def isf(self, q):
        """ Return the inverse survival function at *q*. """
        return self._rv.isf(q)

    def ppf(self, q):
        """ Return the percent point function (inverse CDF) at *q*. """
        return self._rv.ppf(q)

    ## ----- Probability Log Methods ----- ##

    def logcdf(self, k):
        """ Return the log of the cumulative distribution function at *k*. """
        return self._rv.logcdf(k)

    def logpmf(self, k):
        """ Return the log of the probability mass function at *k*. """
        return self._rv.logpmf(k)

    def logsf(self, k):
        """ Return the log of the survival function at *k*. """
        return self._rv.logsf(k)

    ## ----- Probability Properties ----- ##

    @property
    def entropy(self):
        """ The entropy of the random variable. """
        return self._rv.entropy()

    @property
    def max(self):
        """ The maximum value of the random variable. """
        return max(self._rv.xk)

    @property
    def mean(self):
        """ The mean of the random variable. """
        return self._rv.mean()

    @property
    def median(self):
        """ The median of the random variable. """
        return self._rv.median()

    @property
    def min(self):
        """ The minimum value of the random variable. """
        return min(self._rv.xk)

    @property
    def std(self):
        """ The standard deviation of the random variable. """
        return self._rv.std()

    @property
    def variance(self):
        """ The variance of the random variable. """
        return self._rv.var()

    ## ----- Statistics ----- ##

    def _graph(self, method):
        """ Return a graph (that is, a pair of x's and y's) of a given method
        as a function of the random variable's range. """
        x = self.range
        y = [method(a) for a in x]
        return x, y

    def pmf_graph(self):
        """ Return the random variable's PMF graph. """
        return self._graph(self.pmf)

    ## ----- Arithmetic ----- ##

    def arith(self, other, operator, name):
        """ Return a new discrete random variable, which is the result of
        *operator* on *self* and *other*. *other* may be an integer, in which
        case we treat it as a constant random variable. Allowed operators are
        *add*, *sub*, *mul*, *max*, and *min*. """
        ## Turn the integer into a constant random variable
        if isinstance(other, int):
            other = constant(other)

        d = col.defaultdict(float)

        for (x, px), (y, py) in it.product(self.values, other.values):
            val = operator(x, y)
            ival = int(val)
            if not val == ival:
                raise ValueError("Operator must return integer values.")
            d[ival] += px * py

        new_name = name.format(x=self, y=other)
        new_xs = d.keys()
        new_ps = d.values()
        return DiscreteRandomVariable(new_name, xs=new_xs, ps=new_ps)

    def __add__(self, other):
        return self.arith(other, op.add, "({x.name})+({y.name})")

    def __and__(self, other):
        return self.arith(other, min, "({x.name})&({y.name})")

    def __ge__(self, other):
        return self.arith(other, op.ge, "({x.name})>=({y.name})")

    def __gt__(self, other):
        return self.arith(other, op.gt, "({x.name})>({y.name})")

    def __le__(self, other):
        return self.arith(other, op.le, "({x.name})<=({y.name})")

    def __lt__(self, other):
        return self.arith(other, op.lt, "({x.name})<({y.name})")

    def __mul__(self, other):
        return self.arith(other, op.add, "{x.name})*({y.name})")

    def __neg__(self):
        new_name = "-({})".format(self.name)
        new_xs = -self._rv.xk
        new_ps = self._rv.pk
        return DiscreteRandomVariable(new_name, xs=new_xs, ps=new_ps)

    def __or__(self, other):
        return self.arith(other, max, "({x.name})|({y.name})")


class RandomVariablePool(object):
    """ A "pool" is an array of discrete random variables, which may be rolled
    simultaneously to retrieve an array of results. """
    def __init__(self, *drvs):
        self.drvs = np.array(drvs)

    def sum(self, name=None):
        """ Return the random variable of the sum of the pool. """
        _sum = self.drvs[0]
        for drv in self.drvs[1:]:
            _sum = _sum + drv
        if name:
            _sum.name = name
        return _sum


##################################
## ----- Random Variables ----- ##
##################################

def constant(n):
    """ Return the constant random variable *n*. """
    return DiscreteRandomVariable(name=str(n), xs=[n], ps=[1.0])


######################
## ----- Dice ----- ##
######################


def ndk(n, k):
    """ Return the random variable representing rolling *n* *k*-sided dice. """
    name = "{n}d{k}".format(n=n, k=k)
    die = DiscreteRandomVariable(name, rv=ss.randint(1, k + 1))
    if n == 1:
        return die

    return RandomVariablePool(*(die for _ in xrange(n))).sum(name=name)


_pool_cache = {}


def pool(n, k, tn):
    """ Return the random variable counting the number of "successes" of *n*
    rolls of *k*-sided dice, against a target number *tn*. """
    try:
        return _pool_cache[n, k, tn]
    except KeyError:
        pass

    name = "{}p{}>={}".format(n, k, tn)
    if n == 1:
        drv = ndk(1, k) >= tn
        drv.name = name
        _pool_cache[n, k, tn] = drv
        return drv

    right = n // 2
    left = n - right
    drv = pool(left, k, tn) + pool(right, k, tn)
    drv.name = name
    _pool_cache[n, k, tn] = drv
    return drv

