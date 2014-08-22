"""
.. fudge.py
"""

## Framework
import drv.core
import drv.game.base

## Sugar
POOL = drv.core.RandomVariablePool
dk = drv.game.base.dk


## Fudge dice notation is according to Wikipedia
fudge_die = dk(3) - 2
fudge_die.name = 'dF'


def test(skill, target):
    """ Return a random variable which rolls 4 fudge die, adds it to *skill*,
    and checks whether it is at least *target*. """
    fudge_sum = POOL(*([fudge_die] * 4)).sum('4dF')
    tst = (fudge_sum + skill) >= target
    tst.mask = {1: 'Success', 0: 'Failure'}
    return tst

