"""
dice package.
"""

## DRV framework
import drv.integer

## Tools
import collections as col


class Die(drv.integer.FIDRV):
    def __init__(self, k):
        name = "d{k}".format(k=k)
        xs = range(1, k + 1)
        ps = [1] * len(xs)
        super(Die, self).__init__(name, xs, ps)


def dk(k):
    return Die(k)


class Dice(drv.integer.FIDRV):
    def __init__(self, *nks):
        """ *nks* is a list of (n,k) pairs. """
        ## Aggregate and sort
        agg_nks = col.defaultdict(int)
        for n, k in nks:
            agg_nks[k] += n
        sorted_nks = sorted(agg_nks.viewitems(), reverse=True)
        names = ["{n}d{k}".format(n=n, k=k) for k, n in sorted_nks]
        name = " + ".join(names)

        ## TODO: re-implement sum of random variables in a binary method and
        ## use the new implementation here
        xs = [1]
        ps = [1]
        super(Dice, self).__init__(name, xs, ps)


def ndk(n, k):
    if n > 1:
        return Dice((n, k))
    else:
        return Die(k)

