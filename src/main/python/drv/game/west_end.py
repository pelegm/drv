"""
.. west_end.py
"""

## Framework
import drv.game.base

## Sugar
ndk = drv.game.base.ndk


def test(skill, target):
    """ Return a random variable which rolls a *skill* d6 dice, sums it, and
    checks whether it is at least *target*. """
    dice = ndk(skill, 6)
    tst = (dice + skill) >= target
    tst.name("d6 test: skill {} against target {}".format(skill, target))
    tst.mask = {1: 'Success', 0: 'Failure'}
    return tst

