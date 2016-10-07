"""
dice package.
"""

from drv.dice.base import dk, ndk


for k in [1, 2, 3, 4, 5, 6, 8, 10, 12, 20, 100]:
    locals()['d{}'.format(k)] = dk(k)
