"""
.. cyborg.py

Cyborg Commando is a science fiction role-playing game (RPG) published by New
Infinities Productions, Inc in 1987. This module provides some of its dice
mechanics.
"""

## Framework
import drv.game.base

## Sugar
dk = drv.game.base.dk


## This dice is used, according to Wikipedia, in Necromunda and Mordheim
d10x = dk(10) * dk(10)
d10x.name = 'd10x'

