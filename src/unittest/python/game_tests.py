"""
.. game_tests.py
"""

## Testing framework
import unittest

## Testing tools
import numpy as np
import utils

## Testing targets
import drv.game.base as base
import drv.game.d20 as d20


class Test(object):
    attrs = {
        'name': None,
        'max': None,
        'mean': None,
        'median': None,
        'min': None,
        'std': None,
        'variance': None,
    }


class DKTest(Test, unittest.TestCase):
    attrs = {
        'k': 17,
    }

    def setUp(self):
        k = self.attrs['k']
        self.attrs['max'] = k
        self.attrs['name'] = "1d{k}".format(k=k)
        self.attrs['mean'] = (k + 1.0) / 2
        self.attrs['median'] = (k + 1.0) / 2
        self.attrs['min'] = 1
        self.attrs['std'] = np.sqrt((k ** 2 - 1.0) / 12)
        self.attrs['variance'] = (k ** 2 - 1.0) / 12

        self.drv = base.dk(k)


class NDKTest(Test, unittest.TestCase):
    attrs = {
        'n': 3,
        'k': 13,
    }

    def setUp(self):
        n = self.attrs['n']
        k = self.attrs['k'] / n
        self.attrs['min'] = n
        self.attrs['max'] = n * k
        self.attrs['name'] = "{n}d{k}".format(n=n, k=k)
        mean = n * ((k + 1.0) / 2)
        self.attrs['mean'] = mean
        self.attrs['median'] = int(mean)
        variance = n * ((k ** 2 - 1.0) / 12)
        self.attrs['std'] = np.sqrt(variance)
        self.attrs['variance'] = variance

        self.drv = base.ndk(n, k)


class D20Test(Test, unittest.TestCase):
    attrs = {
        'skill': 11,
        'target': 27,
    }

    name = "d20 test: skill {} against target {}"

    def setUp(self):
        s = self.attrs['skill']
        t = self.attrs['target']
        self.attrs['name'] = self.name.format(s, t)
        mean = min(max(1 - (t - s - 1) * 0.05, 0), 1)
        self.attrs['mean'] = mean

        ## Both success and failure are possible
        if 0 < t - s <= 20:
            _max = 1
            _min = 0
            median = 0

        ## Only failure is possible
        elif t - s > 20:
            _max = 0
            _min = 0
            median = 0

        ## Only success is possible
        else:
            _max = 1
            _min = 1
            median = 1

        self.attrs['max'] = _max
        self.attrs['min'] = _min
        self.attrs['median'] = median
        variance = mean - mean ** 2
        self.attrs['std'] = np.sqrt(variance)
        self.attrs['variance'] = variance

        self.drv = d20.test(s, t)


class D20OpposedTest(Test, unittest.TestCase):
    attrs = {
        'skill_a': 11,
        'skill_b': 17,
    }

    name = "d20 opposed test: A ({}) against B ({})"

    def _conv(self, n):
        """ Return the assumed probability of d20 - d20 = n. """
        return min(20 + n, 20 - n) / 400.

    def setUp(self):
        sa = self.attrs['skill_a']
        sb = self.attrs['skill_b']

        win_prob = sum(self._conv(n) for n in xrange(-19, sa - sb))
        loss_prob = sum(self._conv(n) for n in xrange(sa - sb + 1, 20))

        mean = self.attrs['mean'] = win_prob - loss_prob

        ## Win, tie and loss are all possible
        if -19 < sa - sb < 19:
            _max = 1
            _min = -1
            median = 0

        ## Only win and tie are possible
        elif sa - sb == 19:
            _max = 1
            _min = 0
            median = 1

        ## Only win is possible
        elif sa - sb >= 20:
            _max = 1
            _min = 1
            median = 1

        ## Only loss and tie are possible
        elif sa - sb == -19:
            _max = 0
            _min = -1
            median = -1

        ## Only loss is possible:
        elif sa - sb <= -20:
            _max = -1
            _min = -1
            median = -1

        self.attrs['max'] = _max
        self.attrs['min'] = _min
        self.attrs['median'] = median
        self.attrs['name'] = self.name.format(sa, sb)
        variance = mean - mean ** 2
        self.attrs['std'] = np.sqrt(variance)
        self.attrs['variance'] = variance

        self.drv = d20.opposed_test(sa, sb)


for key in Test.attrs:
    test = utils.test_gen(key)
    test_name = "test_{}".format(key)
    setattr(Test, test_name, test)

