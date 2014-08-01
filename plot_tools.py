"""
.. plot_tools.py

This module provides plotting facilities for the discrete random variables.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def _y_of_path(xs, ys, x, n=100):
    """ Find the ``y`` coordinate of *line* in a given *x*. Do it as to
    precision *n*. """
    prev_a = prev_b = None
    for a, b in zip(xs, ys):
        if a > x:
            break
        prev_a, prev_b = a, b
    slope = (b - prev_b) / (a - prev_a)
    return prev_b + slope * (x - prev_a)


def _plot(x, y, mean=None, std=None, xlabel=None, ylabel=None, title=None):
    ## Set figure and axes
    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))

    plt.plot(x, y)

    ## Point to mean
    if (mean is not None) or (std is not None):
        mean_y = _y_of_path(x, y, mean)

        if mean:
            xy_mean_text = mean, mean_y * 1.2
            plt.annotate("Mean", xy=(mean, mean_y), xytext=xy_mean_text,
                         arrowprops=dict(arrowstyle='->', facecolor='green'),
                         color='green')

    ## Set x and y limits
    ax.set_xlim(min(x), max(x))
    ymin, ymax = ax.get_ylim()
    if mean:
        ymax = max(ymax, xy_mean_text[1] * 1.1)
    ax.set_ylim(ymin, ymax)

    ## Show standard deviation
    if mean and std:
        left_x = mean - std
        left_y = _y_of_path(x, y, left_x)
        plt.plot([left_x, left_x], [0, left_y], color='red')
        right_x = mean + std
        right_y = _y_of_path(x, y, right_x)
        plt.plot([right_x, right_x], [0, right_y], color='red')

        mid_y = mean_y * 0.5
        fancy = dict(head_length=0.4, head_width=0.4, tail_width=0.4)
        # arrow = patches.Arrow(mid_x, mid_y, std, 0, width=(ymax * 0.1))
        # ax.add_patch(arrow)
        xy_std_text = mean, mid_y
        ax.annotate("STD", xy=(right_x, mid_y), xytext=xy_std_text,
                    arrowprops=dict(arrowstyle='->'), color='purple')

        ## Turned off, as it does not fit the lines
        # std_x = [a for a in x if left_x <= a <= right_x]
        # std_y = [b for a, b in zip(x, y) if left_x <= a <= right_x]
        # ax.fill_between(std_x, 0, std_y, facecolor='yellow', alpha=0.25)

    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)


def _plot_xkcd(x, y, **kwargs):
    with plt.xkcd():
        line = _plot(x, y, **kwargs)


def plot_pmf(drv, filename=None, mean=False, std=False, xkcd=False):
    """ Plot the probability mass function of the random variable *rv*; if
    *filename* is given, save the figure, otherwise show it. If *xkcd*, plot it
    in ``xkcd`` style. """
    plot_func = _plot if not xkcd else _plot_xkcd
    x, y = drv.pmf_graph()
    xlabel = 'RESULT'
    ylabel = 'PROBABILITY'
    title = drv.name
    kwargs = dict(xlabel=xlabel, ylabel=ylabel, title=title)
    if mean:
        kwargs['mean'] = drv.mean
    if std:
        kwargs['std'] = drv.std
    plot_func(x, y, **kwargs)

    ## Show
    if not filename:
        plt.show()

    ## Save
    else:
        raise NotImplementedError

