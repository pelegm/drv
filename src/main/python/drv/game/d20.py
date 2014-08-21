"""
.. d20.py
"""

## Framework
import drv.game.base

## Sugar
dk = drv.game.base.dk


def test(skill, target):
    """ Return a random variable which rolls a d20, adds it to *skill*, and
    checks whether it is at least *target*. """
    die = dk(20)
    tst = (die + skill) >= target
    tst.name = "d20 test: skill {} against target {}".format(skill, target)
    tst.mask = {1: 'Success', 0: 'Failure'}
    return tst


def opposed_test(skill_a, skill_b):
    """ Return a random variable which rolls two d20, adds each skill to a die,
    and compare whether the first a higher result. """
    die = dk(20)
    tst = (die + skill_a).compare(die + skill_b)
    tst.name = "d20 opposed test: A ({}) against B ({})".format(skill_a,
                                                                skill_b)
    tst.mask = {-1: "B", 0: "Tie", 1: "A"}
    return tst

