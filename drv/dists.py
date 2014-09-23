"""
.. dists.py
"""

## Framework
import drv.integer

## Math
import scipy.misc


#######################
## ----- Tools ----- ##
#######################

choose = lambda n, k: scipy.misc.comb(n, k, exact=True)


###############################
## ----- Distributions ----- ##
###############################


prob_open = lambda v: 0 < v < 1
prob_closed = lambda v: 0 <= v <= 1
integer = lambda v: v == int(v)
natural_0 = lambda v: integer(v) and v >= 0


class ParameteredDist(object):
    def __str__(self):
        return "{self._scls}({self.name})".format(self=self)

    def set_params(self, *args, **kwargs):
        params = dict()
        params.update(zip(self._params, args))
        params.update(kwargs)
        self.argcheck(params)
        for p, v in params.viewitems():
            setattr(self, p, v)
        self.pstr = ",".join(str(getattr(self, p)) for p in self._params)

    def argcheck(self, params):
        for p, v in params.viewitems():
            try:
                i = self._params.index(p)
            except ValueError:
                raise ValueError("Unknown parameter '{}'".format(p))
            if not self._params_allowed[i](v):
                raise ValueError("Parameter '{}' not in range.".format(p))


class Bernoulli(ParameteredDist, drv.integer.FIDRV):
    _params = 'p',
    _params_allowed = prob_open,
    _scls = "Bern"

    def __init__(self, p):
        self.set_params(p=p)
        self.q = 1 - self.p
        super(Bernoulli, self).__init__(self.pstr, [0, 1], [1-p, p])

    ## ----- Arithmetic ----- ##

    def __add__(self, other):
        ## Cast
        if isinstance(other, (Binomial, Hypergeometric)):
            if other.n == 1:
                other = Bernoulli(other.p)

        if isinstance(other, Bernoulli):
            if other is not self:
                if other.p == self.p:
                    return Binomial(2, self.p)
                else:
                    ## TODO: Poisson binomial distribution
                    pass

        return super(Bernoulli, self).__add__(other)

    def __and__(self, other):
        ## Cast
        if isinstance(other, (Binomial, Hypergeometric)):
            if other.n == 1:
                other = Bernoulli(other.p)

        if isinstance(other, Bernoulli):
            if other is not self:
                return Bernoulli(self.p * other.p)

        return super(Bernoulli, self).__and__(other)

    def __mul__(self, other):
        ## Cast
        if isinstance(other, (Binomial, Hypergeometric)):
            if other.n == 1:
                other = Bernoulli(other.p)

        if isinstance(other, Bernoulli):
            if other is not self:
                return Bernoulli(self.p * other.p)

        return super(Bernoulli, self).__mul__(other)

    def __or__(self, other):
        ## Cast
        if isinstance(other, (Binomial, Hypergeometric)):
            if other.n == 1:
                other = Bernoulli(other.p)

        if isinstance(other, Bernoulli):
            if other is not self:
                return Bernoulli(1 - (self.q * other.q))

        return super(Bernoulli, self).__or__(other)


class Binomial(ParameteredDist, drv.integer.FIDRV):
    _params = 'n', 'p',
    _params_allowed = natural_0, prob_closed
    _scls = "Bin"

    ## TODO: allow n to be a Binomial (conditional binomials)

    def __init__(self, n, p):
        self.set_params(n=n, p=p)
        xs = range(n + 1)
        ps = [self._pmf(k) for k in xs]
        super(Binomial, self).__init__(self.pstr, xs, ps)

    def _pmf(self, k):
        n, p = self.n, self.p
        return 1.0 * choose(n, k) * p ** k * (1 - p) ** (n - k)

    ## ----- Arithmetic ----- ##

    def __add__(self, other):
        if isinstance(other, Bernoulli):
            if other.p == self.p:
                return Binomial(self.n + 1, self.p)

        if isinstance(other, Binomial):
            if other is not self:
                if other.p == self.p:
                    return Binomial(self.n + other.n, self.p)

        return super(Binomial, self).__add__(other)


class Hypergeometric(ParameteredDist, drv.integer.FIDRV):
    _params = 'N', 'K', 'n'
    _params_allowed = natural_0, natural_0, natural_0
    _scls = "Hypergeometric"

    def __init__(self, N, K, n):
        self.set_params(N=N, K=K, n=n)
        xs = range(max(0, n + K - N), min(K, n) + 1)
        ps = [self._pmf(k) for k in xs]
        super(Hypergeometric, self).__init__(self.pstr, xs, ps)

    def argcheck(self, params):
        if params['K'] > params['N']:
            raise ValueError("Parameter 'K' not in range.")

        if params['n'] > params['N']:
            raise ValueError("Parameter 'n' not in range.")

        super(Hypergeometric, self).argcheck(params)

    def _pmf(self, k):
        N, K, n = self.N, self.K, self.n
        return 1.0 * choose(K, k) * choose(N - K, n-k) / choose(N, n)

    @property
    def p(self):
        return 1.0 * self.K / self.N


class Rademacher(ParameteredDist, drv.integer.FIDRV):
    _params = ()
    _params_allowed = ()
    _scls = 'Rademacher'

    ## TODO: check why the median of Rademacher is -1

    def __init__(self):
        self.set_params()
        xs = [-1, 1]
        ps = [0.5, 0.5]
        super(Rademacher, self).__init__(self.pstr, xs, ps)

