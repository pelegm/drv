"""
.. harn_master.py
"""

## Framework
import drv.game.base

## Tools
import functools as fn

## Sugar
dk = drv.game.base.dk


def _harn_master_operator(r, t):
    success = 1 if r < t else -1
    critical = 1 if r % 5 else 2
    return success * critical


def test(skill):
    """ Return a random variable which rolls a d100 under *skill* (rounded to
    nearest 5), and if the results divides by 5, the success/failure is
    critical. """
    die = dk(100)
    name = "HarnMaster test"
    tst = die.unop(fn.partial(_harn_master_operator, t=skill), name)
    tst.mask = {-2: "Critical Failure", -1: "Failure", 1: "Success", 2:
                "Critical Success"}
    return tst

