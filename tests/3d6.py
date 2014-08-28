#: Rolling three 6-sided dice, checking the results.
#####
#: Mean and standard deviation of 3d6
import drv.game.base
dice = drv.game.base.ndk(3, 6)
print "Mean:", dice.mean
print "STD:", dice.std
#####
#: Minimum and maximum of 3d6
import drv.game.base
dice = drv.game.base.ndk(3, 6)
print "Min:", dice.min
print "Max:", dice.max
#####
#: Probability of getting at least 13
import drv.game.base
dice = drv.game.base.ndk(3, 6)
hit = lambda d: d >= 13
print "Probability: {:.2%}".format(dice.pr(hit))
