"""
.. plot_tools.py

This module provides plotting facilities for the discrete random variables.
"""

## Tools
import functools as fn
import textwrap as tw

## Plot library
import matplotlib.pyplot as plt


#######################
## ----- Utils ----- ##
#######################

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


########################################
## ----- General Plot Functions ----- ##
########################################

def _plot_axes(xlabel=None, ylabel=None, title=None, figsize=None, dpi=None):
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)

    return fig, ax


def _plot_xkcd(plot_func, *args, **kwargs):
    """ Plot with *plot_func*, *args* and **kwargs*, but in xkcd style. """
    with plt.xkcd():
        fig = plot_func(*args, **kwargs)
    return fig


def _plot_graph(plot_func, drv, method, mean=False, std=False, filename=None,
                xkcd=False, **kwargs):
    x, y = drv.graph(method)

    xlabel = 'RESULT'
    ylabel = 'PROBABILITY'
    title = "{name} ({meth})".format(name=drv.name,
                                     meth=method.im_func.func_name)
    kwargs.update(xlabel=xlabel, ylabel=ylabel, title=title)

    ## Mask
    kwargs['mask'] = getattr(drv, 'mask', None)

    if mean:
        kwargs['mean'] = drv.mean
    if std:
        kwargs['std'] = drv.std

    ## Make figure
    if xkcd:
        plot_func = fn.partial(_plot_xkcd, plot_func)
    fig = plot_func(x, y, **kwargs)

    ## Show
    if not filename:
        fig.show()

    ## Save
    else:
        fig.savefig(filename, dpi=fig.dpi)

    return fig


def _format_tick(mask, tick):
    return "\n".join(tw.wrap(mask.get(tick, ''), width=10))


######################################
## ----- Curve Plot Functions ----- ##
######################################

def _plot_curve_mean(x, y, mean):
    mean_y = _y_of_path(x, y, mean)
    if mean_y is None:
        return

    dy = max(y) - min(y)
    xy_mean_text = mean, max(y) + dy * 0.2
    plt.annotate("Mean", xy=(mean, mean_y), xytext=xy_mean_text,
                 arrowprops=dict(arrowstyle='->', facecolor='green'),
                 color='green')


def _plot_curve_std(x, y, mean, std):
    left_x = mean - std
    left_y = _y_of_path(x, y, left_x)
    if left_y is None:
        return
    ymin = min(y)
    plt.plot([left_x, left_x], [ymin, left_y], color='red')
    right_x = mean + std
    right_y = _y_of_path(x, y, right_x)
    if right_y is None:
        return
    plt.plot([right_x, right_x], [ymin, right_y], color='red')

    mid_y = min(left_y - ymin, right_y - ymin) * 0.5 + ymin
    xy_std_text = mean, mid_y
    plt.annotate("STD", xy=(right_x, mid_y), xytext=xy_std_text,
                 arrowprops=dict(arrowstyle='->'), color='purple')


def _plot_curve(x, y, mean=None, std=None, mask=None, **kwargs):
    ## Set figure and axes
    fig, ax = _plot_axes(**kwargs)

    ## Plot the curve itself
    plt.plot(x, y)

    ## Point to mean
    if mean is not None:
        _plot_curve_mean(x, y, mean)

    ## Set x and y limits
    ax.set_xlim(min(x), max(x))
    dy = max(y) - min(y)
    ymin = min(y)
    if mean:
        ymax = max(y) + dy * 0.3
    else:
        ymax = max(y) + dy * 0.1
    ax.set_ylim(ymin, ymax)

    ## Show standard deviation
    if mean and std:
        _plot_curve_std(x, y, mean, std)

    return fig


def plot_curve(drv, method, mean=False, std=False, **kwargs):
    """ Plot a curve which contains the data returned by *method* which
    correspond to *drv*. If *mean*, annotate the mean. If *std*, in addition,
    annotate the standard deviation.

    This function accepts any plot-related kwargs.
    """
    return _plot_graph(_plot_curve, drv, method, mean=mean, std=std, **kwargs)


#####################################
## ----- Bars Plot Functions ----- ##
#####################################

def _plot_bars(x, y, mask=None, **kwargs):
    ## Set figure and axes
    fig, ax = _plot_axes(**kwargs)

    ## Set x limits
    ax.set_xlim(min(x), max(x))

    ## Plot the curve itself
    plt.bar(x, y, align='center')

    ## Tick labels (mask)
    if mask:
        xticks = ax.get_xticks().tolist()
        new_xticks = [_format_tick(mask, xtick) for xtick in xticks]
        ax.set_xticklabels(new_xticks)

    return fig


def plot_bars(drv, method, **kwargs):
    """ Plot a bar plot which contains the data returned by *method* which
    correspond to *drv*. If *mean*, annotate the mean. If *std*, in addition,
    annotate the standard deviation.

    This function accepts any plot-related kwargs.
    """
    return _plot_graph(_plot_bars, drv, method, **kwargs)

