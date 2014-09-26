"""
.. cyborg.py

Cyborg Commando is a science fiction role-playing game (RPG) published by New
Infinities Productions, Inc in 1987. This module provides some of its dice
mechanics.
"""

## Framework
import drv.dice


## This dice are used, according to Wikipedia, in Necromunda and Mordheim
def d10x():
    rv = drv.dice.dk(10) * drv.dice.dk(10)
    rv.name = 'd10x'
    return rv

