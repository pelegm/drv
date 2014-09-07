#: Rolling special dice.
#####
#: The PMF of Cyborg Commando's d10x
#: figure::img/d10xpmf.png
import drv.dice.cyborg as cyborg
import drv.plot_tools as ptl

## We plot the PMF bar plot
filename = 'examples/img/d10xpmf.png'
kwargs = dict(filename=filename, dpi=70)
d10x = cyborg.d10x
print "Mean:", d10x.mean
print "STD:", d10x.std
ptl.plot_bars(d10x, d10x.pmf, **kwargs)
#####
#: The PMF of a fudge die
#: figure::img/fudgepmf.png
import drv.dice.fudge as fudge
import drv.plot_tools as ptl

## We plot the PMF bar plot
filename = 'examples/img/fudgepmf.png'
kwargs = dict(filename=filename, dpi=70,
              xkcd=True)
fdie = fudge.fudge_die
print "Mean:", fdie.mean
print "STD:", fdie.std
ptl.plot_bars(fdie, fdie.pmf, **kwargs)
#####
#: The PMF of Games Workshop's D66
#: figure::img/d66pmf.png
import drv.dice.gw as gw
import drv.plot_tools as ptl

## We plot the PMF bar plot
filename = 'examples/img/d66pmf.png'
kwargs = dict(filename=filename, dpi=70,
              xkcd=True)
d66 = gw.d66
print "Mean:", d66.mean
print "STD:", d66.std
ptl.plot_bars(d66, d66.pmf, **kwargs)

