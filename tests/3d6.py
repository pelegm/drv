#: Rolling three 6-sided dice, checking the results.
#####
#: Basic properties of 3d6
import drv.dice.base

## We define a random variable which represents
## 3d6
dice = drv.dice.base.ndk(3, 6)

## The following prints its minumum and maximum
## values
print "Min:", dice.min
print "Max:", dice.max

## The following  calculates and prints
## basic statistical results
print "Mean:", dice.mean
print "STD:", dice.std
print "Variance:", dice.variance
print "Median:", dice.median
#####
#: Probability of getting at least 13
import drv.dice.base

## Again, define the random variable
dice = drv.dice.base.ndk(3, 6)

## Define a "hit" function
hit = lambda d: d >= 13

## Calculate and print the probability
print "Probability: {:.2%}".format(dice.pr(hit))
#####
#: Roll 3d6 a couple of times
import drv.core
drv.core.seed(2014)
import drv.dice.base

## Define the random variable and roll
dice = drv.dice.base.ndk(3, 6)
print [dice.roll() for _ in xrange(6)]
#####
#: Plot the PMF graph of 3d6
#: figure::img/3d6pmf.png
import drv.dice.base
import drv.plot_tools as ptl

## Define the random variable
dice = drv.dice.base.ndk(3, 6)

## Plot the PMF graph
filename = 'examples/img/3d6pmf.png'
kwargs = dict(filename=filename, mean=True,
              std=True, dpi=70, xkcd=True)
ptl.plot_curve(dice, dice.pmf, **kwargs)
#####
#: Plot the CDF graph of 3d6
#: figure::img/3d6cdf.png
import drv.dice.base
import drv.plot_tools as ptl

## Define the random variable
dice = drv.dice.base.ndk(3, 6)

## Plot the CDF graph
filename = 'examples/img/3d6cdf.png'
kwargs = dict(filename=filename, mean=True,
              std=True, dpi=70, xkcd=True)
ptl.plot_curve(dice, dice.cdf, **kwargs)
#####
#: Plot the Log-PMF graph of 3d6
#: figure::img/3d6logpmf.png
import drv.dice.base
import drv.plot_tools as ptl

## Define the random variable
dice = drv.dice.base.ndk(3, 6)

## Plot the Log-PMF graph
## If this is like a parabola, then the
## distribution resembles normal...
filename = 'examples/img/3d6logpmf.png'
kwargs = dict(filename=filename, mean=True,
              std=True, dpi=70, xkcd=True)
ptl.plot_curve(dice, dice.logpmf, **kwargs)

