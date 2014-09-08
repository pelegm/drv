"""
.. drv.py

Discrete random variables; these are discrete (integer-valued) finite random
variables.

This module provides a simple (quite thin) wrapper around the extensive
scipy.stats module.
"""

## SciPy's random variable framework
import scipy.stats as ss

## Math
import numpy as np
inf = np.inf

## Randomization
seed = np.random.seed

## Data containers
import collections as col

## Python basics
import functools as fn
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


##################################
## ----- Operator Classes ----- ##
##################################

class Operator(object):
    """ An :class:`Operator` is a class which acts efficiently on a pool of
    random variables, returning a random variable. """
    def __init__(self, operator, unpack=False):
        if not unpack:
            self.operator = operator
        else:
            self.operator = lambda x: operator(*x)

    def __call__(self, pool, name):
        return self._operate(pool, name)

    def _operate(self, pool, name, force_int=True):
        """ This method is intended to be overwritten by subclasses, for more
        efficient calculations. If not overwritten, a naive calculation is
        being executed, which may take exponential time. """
        DRV = type(pool.drvs[0])

        d = col.defaultdict(float)

        for xp in it.product(*(drv.values for drv in pool.drvs)):
            xs, ps = unzip(xp)
            val = self.operator(xs)
            if force_int:
                ival = int(val)
                if ival != val:
                    raise ValueError("Output is not an integer.")
                val = ival
            d[val] += reduce(op.mul, ps)

        formatter = dict(("_{i}".format(i=i), drv) for i, drv in
                         enumerate(pool.drvs))
        _name = name.format(**formatter)

        _xs = d.keys()
        _ps = d.values()
        return DRV(_name, xs=_xs, ps=_ps)


class ReduceOperator(Operator):
    """ This is a class of operators which may be reduced to simple memoryless
    binary operators. """
    def __init__(self, operator, identity=None, unpack=False):
        super(ReduceOperator, self).__init__(operator, unpack=unpack)
        self.identity = identity

    def _operate(self, pool, name):
        if not pool:
            if self.identity:
                return constant(self.identity)
            raise ValueError

        drvs = self._prepare(pool)
        return self._reduce(drvs, name)

    def _prepare(self, pool):
        return pool.drvs

    def _pack(self, drv, name):
        return drv

    force_int = True

    def _reduce(self, drvs, name):
        ## This is the naive implementation, but binary implementation won't be
        ## too difficult, and may be more efficient
        res = drvs[0]
        for rv in drvs[1:]:
            _pool = RandomVariablePool(res, rv)
            res = super(ReduceOperator, self)._operate(
                _pool, name, force_int=self.force_int)

        return self._pack(res, name)


class MemoryReduceOperator(ReduceOperator):
    """ A class of operators which may be reduced to binary operators, keeping
    state. """
    def __init__(self, cast, uncast, operator, identity=None, unpack=False):
        super(MemoryReduceOperator, self).__init__(operator, identity=identity,
                                                   unpack=unpack)
        self.cast = cast
        self.uncast = uncast

    def _prepare(self, pool):
        drvs = []
        for drv in pool.drvs:
            xs = [self.cast(x) for x in drv.xs]
            ps = drv.ps
            drvs.append(BareDiscreteRandomVariable(xs, ps))

        return drvs

    def _pack(self, drv):
        xs = [int(self.uncast(x)) for x in drv.xs]
        ps = drv.ps
        return DiscreteRandomVariable(drv.name, xs=xs, ps=ps)

    force_int = False


class IndexedOperator(Operator):
    """ This is a class of operators which work only on a pre-defined set of
    indices of random variables from the pool. """
    def __init__(self, operator, indices, unpack=False):
        super(IndexedOperator, self).__init__(operator, unpack=unpack)
        self.indices = indices

    def _operator(self, pool):
        drvs = pool.drvs
        _drvs = [drvs[i] for i in self.indices]
        _pool = drv.RandomVariablePool(*_drvs)
        return super(IndexedOperator, self)._operate(_pool, name)


###########################
## ----- Operators ----- ##
###########################

## Simple arithmetic
sum_op = ReduceOperator(sum, 0)
neg_op = IndexedOperator(op.neg, [0])
sub_op = IndexedOperator(op.sub, [0, 1], unpack=True)
mul_op = ReduceOperator(np.prod, 1)

## Max/Min
max_op = ReduceOperator(max)
min_op = ReduceOperator(min)

## Comparison
ge_op = IndexedOperator(op.ge, [0, 1], unpack=True)
gt_op = IndexedOperator(op.gt, [0, 1], unpack=True)
le_op = IndexedOperator(op.le, [0, 1], unpack=True)
lt_op = IndexedOperator(op.lt, [0, 1], unpack=True)
cmp_op = IndexedOperator(cmp, [0, 1], unpack=True)


## n'th highest
def _tuple(n):
    """ Return a function which casts a value into a padded tuple.count """
    def helper(x, n=n):
        return tuple([x] + [None] * (n - 1))
    return helper


def _get_n_highest(n):
    """ Return a function which gets two n-tuples and return one n-tuple which
    contains the highest values. Ignore Nones. """
    def n_highest(a, b):
        merged = [x for x in a + b if x is not None]
        highest = sorted(merged)[-n:]
        if len(highest) < n:
            highest += [None] * (n - len(highest))
        return highest


def nth_highest(n):
    """ Return an operator which returns the n'th highest result. """
    mro = MemoryReduceOperator(cast=_tuple(n), uncast=min,
                               operator=_get_n_highest(n), unpack=True)


##############################
## ----- Main Classes ----- ##
##############################

class BareDiscreteRandomVariable(object):
    """ A general discrete random variables with no calculation methods, whose
    values may be any values, and which provides no data checks. """
    def __init__(self, name, xs, ps):
        self.name = name
        self.xs = xs
        self.ps = ps


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
        """ The median of the random variable. Following SciPy's convention,
        this is simply the PPF of 0.5 (hence it is unique). """
        ## TODO: think of something smarter...
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

    def graph(self, method):
        """ Return a graph (that is, a pair of x's and y's) of a given method
        as a function of the random variable's range. """
        x = self.range
        y = [method(a) for a in x]
        return x, y

    ## ----- Arithmetic ----- ##

    def unop(self, operator, name):
        """ Return a new discrete random variable, which is the result of
        *operator* on *self*. """
        pool = RandomVariablePool(self)
        return operator(pool, name)

    def binop(self, other, operator, name):
        """ Return a new discrete random variable, which is the result of
        *operator* on *self* and *other*. *other* may be an integer, in which
        case we treat it as a constant random variable. """
        ## Turn the integer into a constant random variable
        if isinstance(other, int):
            other = constant(other)

        pool = RandomVariablePool(self, other)
        return operator(pool, name)

    def __add__(self, other):
        return self.binop(other, sum_op, "({_0.name})+({_1.name})")

    def __and__(self, other):
        return self.binop(other, min_op, "({_0.name})&({_1.name})")

    def __ge__(self, other):
        return self.binop(other, ge_op, "({_0.name})>=({_1.name})")

    def __gt__(self, other):
        return self.binop(other, gt_op, "({_0.name})>({_1.name})")

    def __le__(self, other):
        return self.binop(other, le_op, "({_0.name})<=({_1.name})")

    def __lt__(self, other):
        return self.binop(other, lt_op, "({_0.name})<({_1.name})")

    def __mul__(self, other):
        return self.binop(other, mul_op, "{_0.name})*({_1.name})")

    def __neg__(self):
        return self.unop(neg_op, "-({_0.name})")

    def __or__(self, other):
        return self.binop(other, max_op, "({_0.name})|({_1.name})")

    def __sub__(self, other):
        return self.binop(other, sub_op, "({_0.name})-({_1.name})")

    def compare(self, other):
        return self.binop(other, cmp_op, "({_0.name})<>({_1.name})")


class RandomVariablePool(object):
    """ A "pool" is an array of discrete random variables, which may be rolled
    simultaneously to retrieve an array of results. """
    def __init__(self, *drvs):
        self.drvs = drvs

    def __len__(self):
        return len(self.drvs)

    @property
    def xs(self):
        pool_xs = []
        n = len(self.drvs)
        for i, drv in enumerate(self.drvs):
            drv_xs = drv.xs
            m = len(drv_xs)
            shape = [1 if j != i else m for j in xrange(n)]
            pool_xs.append(drv.xs.reshape(shape))
        return pool_xs

    @property
    def ps(self):
        pool_ps = []
        n = len(self.drvs)
        for i, drv in enumerate(self.drvs):
            drv_ps = drv.ps
            m = len(drv_ps)
            shape = [1 if j != i else m for j in xrange(n)]
            pool_ps.append(drv.ps.reshape(shape))
        return pool_ps

    def max(self, name):
        """ Return the random variable of the maximum of the outcomes. """
        return max_op(self, name)

    def median(self, name):
        """ Return the median of the outcomes; this works only if the number of
        rolls is even. """
        raise NotImplementedError

    def nlargest(self, name, n):
        """ Return the random variable of the sum of the *n* largest outcomes.
        """
        raise NotImplementedError

    def nsmallest(self, name, n):
        """ Return the random variable of the sum of the *n* smallest outcomes.
        """
        raise NotImplementedError

    def sum(self, name):
        """ Return the random variable of the sum of the pool. """
        return sum_op(self, name)


##################################
## ----- Random Variables ----- ##
##################################

def constant(n):
    """ Return the constant random variable *n*. """
    return DiscreteRandomVariable(name=str(n), xs=[n], ps=[1.0])

