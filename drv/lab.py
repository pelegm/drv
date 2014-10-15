"""
.. lab.py

Making the interpreter an easy to use computation environment.

Usage:

  >>> from drv.lab import *

"""

import numpy as np


###########################
## ----- Constants ----- ##
###########################

e = np.e
pi = np.pi


#######################
## ----- Sugar ----- ##
#######################

def E(rv):
    """ Return the expectation of *rv*. """
    return rv.mean


def H(rv):
    """ Return the (natural) entropy of *rv*. """
    return rv.entropy


def P(event):
    """ Return the probability of *event*. *event* is simply a boolean random
    variable. """
    return event.mean


def Var(rv):
    """ Return the variance of *rv*. """
    return rv.variance


## Distributions and shortcuts
from drv.dists import *
Bern = Bernoulli
B = Bin = Binomial

