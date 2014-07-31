"""
.. plot_tools.py

This module provides plotting facilities for the discrete random variables.
"""

import matplotlib.pyplot as plt


def _plot(x, y, xlabel=None, ylabel=None, title=None):
    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.set_xlim(min(x), max(x))
    plt.plot(x, y)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)


def _plot_xkcd(x, y, xlabel=None, ylabel=None, title=None):
    with plt.xkcd():
        _plot(x, y, xlabel=xlabel, ylabel=ylabel, title=title)


def plot_pmf(rv, filename=None, xkcd=False):
    """ Plot the probability mass function of the random variable *rv*; if
    *filename* is given, save the figure, otherwise show it. If *xkcd*, plot it
    in ``xkcd`` style. """
    plot_func = _plot if not xkcd else _plot_xkcd


