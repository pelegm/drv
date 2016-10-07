"""
.. d6.py

D6 System: a universal RPG system published by West End Games in 1996.

https://en.wikipedia.org/wiki/D6_System
"""

from drv.dice import d6, ndk


def ndp(n, p):
    s = ndk(n, 6) + p
    s.name = "{n}D+{p}".format(n=n, p=p)
    return s


## TODO: Wild die
