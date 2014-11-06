"""
.. tools.py
"""

## Python tools
import itertools

## Infinity
inf = float('inf')


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


def powerseq(iterable, minsize=0, maxsize=inf):
    """ Return the generator of all ordered subsets of *iterable* whose size is
    at least *minsize* and at most *maxsize*, ordered by size.

    :param iterable: the iterable to extract subsets from.
    :type iterable: iterable
    :param minsize: the minimum size of sets to yield.
    :type minsize: :class:`int`
    :param maxsize: the maximum size of sets to yield.
    :type maxsize: :class:`int` or `inf`

    Examples:

    >>> list(powerseq(xrange(3)))
    [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
    >>> list(powerseq(()))
    [()]
    """
    _maxsize = min(maxsize, len(list(iterable)))
    _chain = itertools.chain.from_iterable
    _range = xrange(minsize, _maxsize + 1)
    return _chain(itertools.combinations(iterable, r) for r in _range)


def powerset(aset, maxsize=inf):
    """ Yield all subsets of *aset* of size up to *maxsize*.

    Examples:
    >>> list(powerset((1,)))
    [set([]), set([1])]
    >>> list(powerset((1, 2)))
    [set([]), set([1]), set([2]), set([1, 2])]
    >>> list(powerset('', maxsize=7))
    [set([])]
    """
    return (set(t) for t in powerseq(aset, maxsize=maxsize))


def unzip(zipped):
    """ Return a generator reverses the work of zip/izip.

    :param zipped: the iterable to unzip.
    :type zipped: iterable of :term:`iterables <iterable>`.
    :rtype: generator

    Examples:

    >>> list(unzip(zip(xrange(3), xrange(2, 5))))
    [(0, 1, 2), (2, 3, 4)]
    >>> list(unzip(itertools.izip(xrange(3), xrange(2, 5))))
    [(0, 1, 2), (2, 3, 4)]
    >>> list(unzip(zip([1], [])))
    []
    >>> list(unzip(zip([], [])))
    []

    .. note:: The returned elements of the generator are always tuples.
              This is a result of how :func:`itertools.izip` works.
    """
    return itertools.izip(*zipped)

