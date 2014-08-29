"""
.. plot_tools.py

This module provides plotting facilities for the discrete random variables.
"""

import matplotlib.pyplot as plt


def _y_of_path(xs, ys, x, n=100):
    """ Find the ``y`` coordinate of *line* in a given *x*. Do it as to
    precision *n*. """
    prev_a = prev_b = None
    for a, b in zip(xs, ys):
        if a > x:
            break
        prev_a, prev_b = a, b
    if None in (prev_a, prev_b):
        return None
    slope = (b - prev_b) / (a - prev_a)
    return prev_b + slope * (x - prev_a)


def _plot_axes(xlabel=None, ylabel=None, title=None):
    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)

    return ax


def _plot_curve_mean(x, y, mean):
    mean_y = _y_of_path(x, y, mean)
    if mean_y is None:
        return

    xy_mean_text = mean, max(y) * 1.2
    plt.annotate("Mean", xy=(mean, mean_y), xytext=xy_mean_text,
                 arrowprops=dict(arrowstyle='->', facecolor='green'),
                 color='green')


def _plot_curve_std(x, y, mean, std):
    left_x = mean - std
    left_y = _y_of_path(x, y, left_x)
    if left_y is None:
        return
    plt.plot([left_x, left_x], [0, left_y], color='red')
    right_x = mean + std
    right_y = _y_of_path(x, y, right_x)
    if right_y is None:
        return
    plt.plot([right_x, right_x], [0, right_y], color='red')

    mid_y = min(left_y, right_y) * 0.5
    xy_std_text = mean, mid_y
    plt.annotate("STD", xy=(right_x, mid_y), xytext=xy_std_text,
                 arrowprops=dict(arrowstyle='->'), color='purple')


def _plot_curve(x, y, mean=None, std=None, xlabel=None, ylabel=None, mask=None,
                title=None):
    ## Set figure and axes
    ax = _plot_axes(xlabel=xlabel, ylabel=ylabel, title=title)

    ## Plot the curve itself
    plt.plot(x, y)

    ## Point to mean
    if mean is not None:
        _plot_curve_mean(x, y, mean)

    ## Set x and y limits
    ax.set_xlim(min(x), max(x))
    ymin, ymax = ax.get_ylim()
    if mean:
        ymax *= 1.2 * 1.1
    ax.set_ylim(ymin, ymax)

    ## Show standard deviation
    if mean and std:
        _plot_curve_std(x, y, mean, std)


def _plot_xkcd(plot_func, *args, **kwargs):
    """ Plot with *plot_func*, *args* and **kwargs*, but in xkcd style. """
    with plt.xkcd():
        plot_func(*args, **kwargs)


def _plot_pmf(plot_func, drv, filename=None, mean=False, std=False,
              xkcd=False):
    x, y = drv.pmf_graph()


    xlabel = 'RESULT'
    ylabel = 'PROBABILITY'
    title = drv.name
    kwargs = dict(xlabel=xlabel, ylabel=ylabel, title=title)

    ## Mask
    kwargs['mask'] = getattr(drv, 'mask', None)

    if mean:
        kwargs['mean'] = drv.mean
    if std:
        kwargs['std'] = drv.std
    if xkcd:
        _plot_xkcd(plot_func, x, y, **kwargs)
    else:
        plot_func(x, y, **kwargs)

    ## Show
    if not filename:
        plt.show()

    ## Save
    else:
        plt.savefig(filename)


def plot_pmf_curve(drv, filename=None, mean=False, std=False, xkcd=False):
    """ Plot the probability mass function of the random variable *rv*; if
    *filename* is given, save the figure, otherwise show it. If *xkcd*, plot it
    in ``xkcd`` style. """
    _plot_pmf(_plot_curve, drv, filename=filename, mean=mean, std=std,
              xkcd=xkcd)


def _plot_bars(x, y, xlabel=None, ylabel=None, mask=None, title=None):
    ## Set figure and axes
    ax = _plot_axes(xlabel=xlabel, ylabel=ylabel, title=title)

    ## Plot the curve itself
    plt.bar(x, y, align='center')

    ## Tick labels (mask)
    if mask:
        xticks = ax.get_xticks().tolist()
        new_xticks = [mask.get(xtick, '') for xtick in xticks]
        ax.set_xticklabels(new_xticks)


def plot_pmf_bars(drv, filename=None, xkcd=False):
    """ Plot the probability mass function of the random variable *drv* as a
    bar plot; if *filename* is given, save the figure, otherwise show it. If
    *xkcd*, plot it in ``xkcd`` style. """
    _plot_pmf(_plot_bars, drv, filename=filename, xkcd=xkcd)

