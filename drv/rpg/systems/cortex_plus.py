"""
.. cortex_plus.py

Cortex Plus is a roll and keep system.  In full generality, a pool is any
sequence of dice-types from {4, 6, 8, 10, 12}, of length at least 2.  The
result of a roll is always the sum of the two highest results.  Results of 1 do
not count, but instead are 0 (and in fact cause complications).  """


from drv.core import RandomVariablePool as POOL
from drv.dice.base import custom_die


def dk(k):
    name = "d{k}".format(k=k)
    return custom_die([0] + range(2, k + 1), name)


d4 = dk(4)
d6 = dk(6)
d8 = dk(8)
d10 = dk(10)
d12 = dk(12)


def roll_and_keep(*dice):
    pool = POOL(*(dk(k) for k in dice))
    return pool.nlargest_sum(2, ",".join("d{}".format(k) for k in dice))
