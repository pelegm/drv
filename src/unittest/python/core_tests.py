"""
.. core_tests.py
"""

## Testing framework
import unittest

## Testing tools
import numpy as np

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
        'name': None,
        'max': 17,
        'mean': None,
        'median': None,
        'min': None,
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
        'mean': None,
        'median': None,
        'min': -50,
        'std': None,
        'variance': None,
    }

    def setUp(self):
        rng = np.arange(self.attrs['min'], self.attrs['max'] + 1)
        self.attrs['mean'] = rng.mean()
        self.attrs['median'] = np.median(rng)
        self.attrs['std'] = rng.std()
        self.attrs['variance'] = rng.var()

        self.rv = ss.randint(self.attrs['min'], self.attrs['max'] + 1)
        self.drv = drv.core.DiscreteRandomVariable('test_randint', rv=self.rv)


def test_gen(key):
    def test(self, key=key):
        expected = self.attrs[key]
        actual = getattr(self.drv, key)
        msg = "{} test has failed; expected {}, got {}".format(key, expected,
                                                               actual)
        if isinstance(expected, str):
            self.assertEqual(expected, actual, msg=msg)
        else:
            self.assertAlmostEqual(expected, actual, msg=msg)
    return test


for key in DiscreteRandomVariableTest.attrs:
    test = test_gen(key)
    test_name = "test_{}".format(key)
    setattr(DiscreteRandomVariableTest, test_name, test)

