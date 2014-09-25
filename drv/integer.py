"""
.. integer.py
"""

## Abstract layer
import abc

## General tools
import drv.tools as tools

## Framework
import numpy as np
import drv.real


## Messages
EMPTY_SUPPORT = "The support may not be empty."
INT_SUPPORT = "The support must contain integers only."


class IDRV(drv.real.RDRV):
    """ An integer-valued Discrete Random Variable. May have finite or infinite
    support.

    *name* is an identifier for the random variable. """


class FIDRV(drv.real.FRDRV, IDRV):
    """ An finite integer-valued Discrete Random Variable.

    *name* is an identifier for the random variable. *xs* are the possible
    values (categories), and *ps* are the distributions. *xs* and *ps* are
    checked for correctedness, and *ps* are normalized. """
    def _initialize(self, xs, ps):
        """ Set, sort and check *xs* and *ps*, ignoring values with zero
        probability, normalizing the probabilities. """
        ## Check for non-empty support
        if not xs:
            raise ValueError(EMPTY_SUPPORT)

        xs = tuple(xs)

        ## Make them integers
        i_xs = tuple(int(x) for x in xs)
        if not i_xs == xs:
            raise ValueError(INT_SUPPORT)

        super(FIDRV, self)._initialize(i_xs, ps)

        ## Make them integers again
        self.xs = [int(x) for x in self.xs]

    @property
    def range(self):
        """ The minimal list of integers containing the support. """
        return range(self.xs[0], self.xs[-1] + 1)

    def graph(self, method):
        """ Return a graph (that is, a pair of x's and y's) of a given method
        as a function of the random variable's range. """
        x = self.range
        try:
            _method = getattr(self, method)
        except TypeError:
            _method = method
        y = [_method(a) for a in x]
        return x, y

    ## ----- Operations ----- ##

    def unop(self, operator, name, klass=None):
        """ Return a new discrete random variable, which is the result of
        *operator* on *self*. """
        klass = klass or FIDRV
        return super(FIDRV, self).unop(operator, name, klass=klass)

    def binop(self, other, operator, name, reverse=False, klass=None):
        """ return a new discrete random variable, which is the result of
        *operator* on *self* and *other*. *other* may be a integer, in which
        case we treat it as a constant random variable. """
        ## 'other' is not a random variable, we try to make it such
        if not isinstance(other, drv.core.DRV):

            ## turn the integer into a constant random variable
            if isinstance(other, int):
                other = DegenerateIDRV(other)

        ## We don't know how to handle it
        if not isinstance(other, FIDRV):
            return super(FIDRV, self).binop(other, operator, name,
                                            reverse=reverse, klass=klass)

        ## We know how to handle it
        if reverse:
            tfdrv = drv.core.TFDRV([other, self])
        else:
            tfdrv = drv.core.TFDRV([self, other])
        klass = klass or FIDRV
        return tfdrv.map(operator, name=name, klass=klass, unpack=True)


class DegenerateIDRV(FIDRV):
    def __init__(self, k):
        super(DegenerateIDRV, self).__init__(str(k), [k], [1])

