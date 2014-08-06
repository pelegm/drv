"""
.. utils.py
"""


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

