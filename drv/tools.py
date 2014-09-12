"""
.. tools.py
"""

## Python tools
import itertools as it


def gcs(*objects):
    """ Return the 'greatest common superclass' of objects. """
    classes = [type(o) for o in objects]
    mros = [c.mro() for c in classes]
    n = min(len(mro) for mro in mros)
    i = 0
    while i < n:
        for mro in mros:
            candidate = mro[i]
            if all(candidate in m for m in mros):
                return candidate
        i += 1
    return None


def unzip(zipped):
    """ Return a :term:`generator` reverses the work of zip/izip.

    :param zipped: the iterable to unzip.
    :type zipped: :term:`iterable` of :term:`iterables <iterable>`.
    :rtype: :term:`generator`

    Examples:

    >>> list(unzip(zip(xrange(3), xrange(2, 5))))
    [(0, 1, 2), (2, 3, 4)]
    >>> list(unzip(izip(xrange(3), xrange(2, 5))))
    [(0, 1, 2), (2, 3, 4)]

    .. note:: The returned elements of the generator are always tuples. This is
        a result of how :func:`zip` works.
    """
    return it.izip(*zipped)

