"""
.. rpg_tests.py
"""

## Testing framework
import unittest

## Testing tools
import numpy as np
import utils

## Testing target
import drv.rpg

## Auxiliary
import itertools as it
import scipy.stats as ss


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

        self.drv = drv.rpg.dk(k)


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

        self.drv = drv.rpg.ndk(n, k)


class D20Test(Test, unittest.TestCase):
    attrs = {
        'skill': 11,
        'target': 27,
    }

    name = "d20 test: skill {} against target {}"

    def setUp(self):
        s = self.attrs['skill']
        t = self.attrs['target']
        self.attrs['min'] = 0
        self.attrs['max'] = 1
        self.attrs['name'] = self.name.format(s, t)
        mean = min(max(1 - (t - s - 1) * 0.05, 0), 1)
        self.attrs['mean'] = mean
        if 0 < t - s:
            median = 0
        else:
            median = 1
        self.attrs['median'] = median
        variance = mean - mean ** 2
        self.attrs['std'] = np.sqrt(variance)
        self.attrs['variance'] = variance

        self.drv = drv.rpg.d20_test(s, t)


for key in Test.attrs:
    test = utils.test_gen(key)
    test_name = "test_{}".format(key)
    setattr(Test, test_name, test)

