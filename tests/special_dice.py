#: Rolling special dice.
#####
#: The PMF of Cyborg Commando's d10x
#: figure::img/d10xpmf.png
import drv.game.cyborg as cyborg
import drv.plot_tools as ptl

## We plot the PMF bar plot
filename = 'examples/img/d10xpmf.png'
kwargs = dict(filename=filename, dpi=70)
print "Mean:", cyborg.d10x.mean
print "STD:", cyborg.d10x.std
ptl.plot_pmf_bars(cyborg.d10x, **kwargs)
#####
#: The PMF of a fudge die
#: figure::img/fudgepmf.png
import drv.game.fudge as fudge
import drv.plot_tools as ptl

## We plot the PMF bar plot
filename = 'examples/img/fudgepmf.png'
kwargs = dict(filename=filename, dpi=70,
              xkcd=True)
print "Mean:", fudge.fudge_die.mean
print "STD:", fudge.fudge_die.std
ptl.plot_pmf_bars(fudge.fudge_die, **kwargs)
#####
#: The PMF of Games Workshop's D66
#: figure::img/d66pmf.png
import drv.game.gw as gw
import drv.plot_tools as ptl

## We plot the PMF bar plot
filename = 'examples/img/d66pmf.png'
kwargs = dict(filename=filename, dpi=70,
              xkcd=True)
print "Mean:", gw.d66.mean
print "STD:", gw.d66.std
ptl.plot_pmf_bars(gw.d66, **kwargs)

