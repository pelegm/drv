"""
.. gw.py

Games Workshop is a British game production and retailing company. This module
provides some of its dice mechanics.
"""

## Framework
import drv.game.base

## Sugar
dk = drv.game.base.dk


## This dice is used, according to Wikipedia, in Necromunda and Mordheim
d66 = dk(6) * 10 + dk(6)
d66.name = 'D66'


## This is introduced, according to Wikipedia, in Blood Bowl
def db(x):
    """ Return a random variable which rolls a "block die" *x* times. """
    ## This is usually marked Xdb, where x is one of 3, 2, 1 (usually omitted),
    ## -2 or -3.
    raise NotImplementedError

