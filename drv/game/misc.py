"""
.. misc.py
"""

## Framework
import drv.core
import drv.game.base

## Sugar
POOL = drv.core.RandomVariablePool
dk = drv.game.base.dk


def test(skill, target, die=20):
    """ Return a random variable which rolls *skill* dice, each of *die* faces,
    and test them against *target*. The result is called "number of successes.
    """
    _die = dk(die)
    pool = POOL(*(_die >= target for _ in xrange(skill)))
    name = "Misc. test: skill {} against target {}, die=d{}"
    return pool.sum(name.format(skill, target, die))

