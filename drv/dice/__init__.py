"""
dice package.
"""

## DRV framework
import drv.core
import drv.integer

## Tools
import collections as col
import operator as op


class Die(drv.integer.FIDRV):
    def __init__(self, k):
        if k > 0:
            name = "d{k}".format(k=k)
            xs = range(1, k + 1)
            ps = [1] * len(xs)
        elif k < 0:
            name = "-d{k}".format(k=-k)
            xs = range(k, 0)
            ps = [1] * len(xs)
        else:
            raise ValueError("k should be a positive or a negative integer.")

        super(Die, self).__init__(name, xs, ps)

        self.k = k
        self.nks = [(1, k)]

    ## ----- Arithemtic ----- ##

    def __add__(self, other):
        if isinstance(other, int):
            other = Dice((other, 1))

        if isinstance(other, (Die, Dice)):
            nks = self.nks + other.nks
            return Dice(*nks)

        return super(Die, self).__add__(self, other)

    def __neg__(self):
        return Die(-self.k)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Dice((other, 1))

        if isinstance(other, (Die, Dice)):
            return self + (-other)

        return super(Die, self).__sub__(self, other)


def dk(k):
    return Die(k)


class DicePool(drv.core.TFDRV):
    def __init__(self, *nks):
        """ *nks* is a list of (n,k) pairs. """
        ## Aggregate and sort
        _nks = col.defaultdict(int)
        for n, k in nks:

            ## Skip 0-sided dice
            if not k:
                continue

            ## Handle negative constant dice
            if k == -1:
                _nks[-k] += -n

            else:
                _nks[k] += n

        self.nks = [(n, k) for (k, n)
                    in sorted(_nks.viewitems(), reverse=True)]
        name = ''

        ## Append positive non-constant names
        if max(_nks) > 0:
            names = ["{n}D{k}".format(n=n, k=k) for n, k in self.nks if k > 1]
            name += " + ".join(names)

        ## Append negative non-constant names
        if min(_nks) < 0:
            names = ["{n}D{k}".format(n=n, k=-k) for n, k in self.nks
                     if k < -1]
            if not name:
                name = '-'
            else:
                name += ' - '
            name += " - ".join(names)

        ## Append a constant name
        if 1 in _nks:
            if name:
                name += " "
            name += "{:+}".format(_nks[1])

        ## Construct drvs
        drvs = []
        for n, k in self.nks:
            if k == 1 and n < 0:
                drvs.extend(Die(-k) for _ in xrange(-n))
            else:
                drvs.extend(Die(k) for _ in xrange(n))

        ## Initialize tuple DRV
        super(DicePool, self).__init__(drvs, name=name)

    ## ----- Operations ----- ##

    def subtuple(self, indices, name, klass=None):
        """ Return the sub-tuple containing only *indices*. """
        klass = klass or drv.core.TFDRV
        return super(DicePool, self).subtuple(indices, name, klass=klass)

    ## ----- Arithmetic ----- ##

    def __add__(self, other):
        if isinstance(other, int):
            nks = self.nks + [(other, 1)]
            return DicePool(*nks)

        if isinstance(other, (Die, DicePool)):
            nks = self.nks + other.nks
            return DicePool(*nks)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, int):
            return self + (-other)

        return NotImplemented

    @property
    def max(self):
        return self.reduce(op.or_, "Max({})".format(self),
                           klass=drv.integer.FIDRV)

    @property
    def min(self):
        return self.reduce(op.and_, "Min({})".format(self),
                           klass=drv.integer.FIDRV)

    @property
    def prod(self):
        return self.reduce(op.mul, "Prod({})".format(self),
                           klass=drv.integer.FIDRV)

    @property
    def sum(self):
        return Dice(*self.nks)


class Dice(drv.integer.FIDRV):
    def __init__(self, *nks):
        """ *nks* is a list of (n,k) pairs. """
        ## Construct underlying pool
        self.pool = DicePool(*nks)
        self.nks = self.pool.nks

        name = self.pool.name.replace('D', 'd')

        ## Calculate distribution
        # add = lambda a, b: a.__add__(b, raw=True)
        add = drv.integer.FIDRV.__add__
        rv = self.pool.reduce(add, '', klass=drv.integer.FIDRV)
        xs, ps = rv.xs, rv.ps
        super(Dice, self).__init__(name, xs, ps)

    ## ----- Arithemtic ----- ##

    def __add__(self, other):
        if isinstance(other, int):
            other = Dice((other, 1))

        if isinstance(other, (Die, Dice)):
            nks = self.nks + other.nks
            return Dice(*nks)

        return super(Die, self).__add__(self, other)

    def __neg__(self):
        return Dice(*((-n, k) for n, k in self.nks))

    def __sub__(self, other):
        if isinstance(other, int):
            other = Dice((other, 1))

        if isinstance(other, (Die, Dice)):
            return self + (-other)

        return super(Die, self).__sub__(self, other)


def ndk(n, k):
    """
    .. note:: this function is more or less O(n^2 * k^2). You may wish to
    remain in the range nk<1000 for sane running times. """
    if n > 1:
        return Dice((n, k))
    else:
        return Die(k)


__all__ = ['Die', 'dk', 'DicePool', 'Dice', 'ndk']\
    + ['cyborg', 'd20', 'fudge']

