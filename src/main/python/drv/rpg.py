"""
.. rpg.py

Role-playing game dice mechanisms.
"""

## Framework
import drv.core
import scipy.stats as ss
import functools as fn


## Sugar
DRV = drv.core.DiscreteRandomVariable
POOL = drv.core.RandomVariablePool


########################
## ----- Basics ----- ##
########################

def dk(k, name=None):
    """ Return the random variable representing rolling a single *k*-sided die.
    """
    _name = name or "1d{k}"
    name = _name.format(k=k)
    return DRV(name, rv=ss.randint(1, k + 1))


def ndk(n, k, name=None):
    """ Return the random variable representing rolling *n* *k*-sided dice. """
    die = dk(k, name=name)
    if n == 1:
        return die

    _name = name or "{n}d{k}"
    name = _name.format(n=n, k=k)
    return POOL(*(die for _ in xrange(n))).sum(name=name)


#####################
## ----- D20 ----- ##
#####################

def d20_test(skill, target):
    """ Return a random variable which rolls a d20, adds it to *skill*, and
    checks whether it is at least *target*. """
    die = dk(20)
    test = (die + skill) >= target
    test.name = "d20 test: skill {} against target {}".format(skill, target)
    test.mask = {1: 'Success', 0: 'Failure'}
    return test


def d20_opposed_test(skill_a, skill_b):
    """ Return a random variable which rolls two d20, adds each skill to a die,
    and compare whether the first a higher result. """
    die = dk(20)
    test = (die + skill_a).compare(die + skill_b)
    test.name = "d20 opposed test: A ({}) against B ({})".format(skill_a,
                                                                 skill_b)
    test.mask = {-1: "B", 0: "Tie", 1: "A"}
    return test


#######################
## ----- Fudge ----- ##
#######################

fudge_die = dk(3) - 2
fudge_die.name = 'fudge'


def fudge_test(skill, target):
    """ Return a random variable which rolls 4 fudge die, adds it to *skill*,
    and checks whether it is at least *target*. """
    fudge_sum = POOL(*([fudge_die] * 4)).sum('fudge_sum')
    test = (fudge_sum + skill) >= target
    test.mask = {1: 'Success', 0: 'Failure'}
    return test


#############################
## ----- Harn Master ----- ##
#############################

def _harn_master_operator(r, t):
    success = 1 if r < t else -1
    critical = 1 if r % 5 else 2
    return success * critical


def harn_master_test(skill):
    """ Return a random variable which rolls a d100 under *skill* (rounded to
    nearest 5), and if the results divides by 5, the success/failure is
    critical. """
    die = dk(100)
    name = "HarnMaster test"
    test = die.unop(fn.partial(_harn_master_operator, t=skill), name)
    test.mask = {-2: "Critical Failure", -1: "Failure", 1: "Success", 2:
                 "Critical Success"}
    return test


############################
## ----- Talislanta ----- ##
############################

## TODO: action table
## TODO: test


##########################
## ----- West End ----- ##
##########################


def west_end_test(skill, target):
    """ Return a random variable which rolls a *skill* d6 dice, sums it, and
    checks whether it is at least *target*. """
    dice = ndk(skill, 6)
    test = (dice + skill) >= target
    test.name("d6 test: skill {} against target {}".format(skill, target))
    test.mask = {1: 'Success', 0: 'Failure'}
    return test

