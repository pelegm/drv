"""
.. core_tests.py
"""

## Testing framework
import unittest

## Testing tools
import numpy as np
import utils

## Testing target
import drv.core

## Auxiliary
import itertools as it
import scipy.stats as ss


class UnzipTest(unittest.TestCase):
    def test_unzips_zip_properly(self):
        test_a, test_b = drv.core.unzip(zip(xrange(3), xrange(2, 5)))
        self.assertEqual(test_a, (0, 1, 2))
        self.assertEqual(test_b, (2, 3, 4))

    def test_unzips_izip_properly(self):
        test_a, test_b = drv.core.unzip(it.izip(xrange(3), xrange(2, 5)))
        self.assertEqual(test_a, (0, 1, 2))
        self.assertEqual(test_b, (2, 3, 4))


class DiscreteRandomVariableTest(object):
    attrs = {
        'name': 'test_randint',
        'max': 100,
        'mean': None,
        'median': None,
        'min': -50,
        'std': None,
        'variance': None,
    }


class DiscreteRandomVariableConstantTest(unittest.TestCase,
                                         DiscreteRandomVariableTest):
    attrs = {
        'max': 17,
        'std': 0,
        'variance': 0,
    }

    def setUp(self):
        n = self.attrs['max']
        self.attrs['name'] = str(n)
        self.attrs['mean'] = n
        self.attrs['median'] = n
        self.attrs['min'] = n

        self.drv = drv.core.constant(n)


class DiscreteRandomVariableRandintTest(unittest.TestCase,
                                        DiscreteRandomVariableTest):
    attrs = {
        'name': 'test_randint',
        'max': 100,
        'min': -50,
    }

    def setUp(self):
        rng = np.arange(self.attrs['min'], self.attrs['max'] + 1)
        self.attrs['mean'] = rng.mean()
        self.attrs['median'] = np.median(rng)
        self.attrs['std'] = rng.std()
        self.attrs['variance'] = rng.var()

        self.rv = ss.randint(self.attrs['min'], self.attrs['max'] + 1)
        self.drv = drv.core.DiscreteRandomVariable('test_randint', rv=self.rv)


for key in DiscreteRandomVariableTest.attrs:
    test = utils.test_gen(key)
    test_name = "test_{}".format(key)
    setattr(DiscreteRandomVariableTest, test_name, test)

