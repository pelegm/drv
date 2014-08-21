"""
.. risk.py

Rules can be found here:
    http://www.hasbro.com/common/instruct/risk.pdf

"""

## Framework
import drv.core
import drv.game.base

## Sugar
POOL = drv.core.RandomVariablePool
dk = drv.game.base.dk


def _risk_op(a, d):
    def _op(args, a=a, d=d):
        attack = sorted(args[:a], reverse=True)
        defense = sorted(args[-d:], reverse=True)
        at, dt = 0, 0
        for ar, dr in zip(attack, defense):
            if ar > dr:
                dt += 1
            else:
                at += 1
        return -at + dt
    return drv.core.Operator(_op)


def attack(attacker, defender):
    """ Return an attack random variable, considering the attacker has
    *attacker* rolls and the defender has *defender* rolls. """
    if not 1 <= attacker <= 3:
        raise ValueError("Attacker should roll 1, 2 or 3 dice.")
    if not 1 <= defender <= 2:
        raise ValueError("Defender should roll 1 or 2 dice.")
    _op = _risk_op(attacker, defender)
    pool = POOL(*(dk(6) for _ in xrange(attacker + defender)))
    atk = _op(pool, "Risk attack: {} attack {}".format(attacker, defender))
    atk.mask = {-2: 'attacker loses 2', -1: 'attacker loses 1',
                0: 'both lose 1', 1: 'defender loses 1', 2: 'defender loses 2'}
    return atk


## Todo: a whole battle, perhaps?

