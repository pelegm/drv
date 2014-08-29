#: Understanding a risk attack.
#####
#: Simulating risk attacks
import drv.core
drv.core.seed(2014)
import drv.game.risk as risk

## We define a random variable which represents
## the attack: 3 dice for the attacker, 2 for
## the defender
atk = risk.attack(3, 2)

## The following rolls 1000 attacks and finds
## out in how many the attacker wins
result = list(atk.rolls_gen(1000))
print "Win:", sum(r > 0 for r in result)
#####
#: Visualizing possible results
#: figure::img/riskpmf.png
import drv.game.risk as risk
import drv.plot_tools as ptl

## We define the attack random variable
atk = risk.attack(3, 2)

## We plot the PMF bar plot
filename = 'examples/img/riskpmf.png'
kwargs = dict(filename=filename, dpi=70,
              xkcd=True)
ptl.plot_pmf_bars(atk, **kwargs)

