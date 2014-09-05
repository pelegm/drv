"""
.. dists.py

Standard discrete probability distributions.
"""

## Framework
import scipy.stats as ss


## The following explains the hierarchy of discrete probability distributions
## in general.
## - "discrete" may be "finite"
## - "discrete" may be either "integer-valued" (or simply "integer")
## - "integer" may be "non-negative"; relevant only for infinite rvs
##
## So we may mark and DRV as one of the following initials:
## - DRV - the most general discrete random variable
## - IDRV - integer-valued discrete random variable
## - NIDRV - non-negative integer-valued discrete random variable
## - FIDRV - finite integer-valued discrete random variable
##
## I am not entirely sure we need the non-negative variation.

## TODO: add the following distributions
## - Bernoulli :: FIDRV :: bernoulli
## - beta-binomial :: FIDRV :: ?
## - beta negative binomial :: NIDRV :: ?
## - binomial :: FIDRV :: binom
## - Boltzmann :: ? :: ?
##     (also: Gibbs)
## - Borel :: NIDRV :: ?
## - Conway-Maxwell-Poisson :: NIDRV :: ?
##     (also: CMP, COM-Poisson)
## - degenerate :: FIDRV :: ?
##     (also: deterministic)
## - displaced Poisson :: ? :: ?
##     (also: hyper-Poisson)
## - extended negative binomial :: ? :: ?
## - Fisher's noncentral hypergeometric :: FIDRV :: ?
## - geometric :: NIDRV :: geom
## - hypergeometric :: FIDRV :: hypergeom
## - logarithmic :: NIDRV :: ?
##     (also: logarithmic series, log-series)
## - negative binomial :: NIDRV :: nbinom
## - parabolic fractal :: ? :: ?
## - Poisson :: NIDRV :: poisson
## - Poisson binomial :: FIDRV :: ?
## - Rademacher :: FIDRV :: ?
## - Skellam :: IDRV :: ?
## - uniform :: FIDRV :: randint
## - Wallenius' noncentral hypergeometric :: FIDRV :: ?
## - Yule-Simon :: NIDRV :: ?
## - zero-truncated Poisson :: ? :: ?
##     (also: ZTP)
## - zeta :: NIDRV :: ?

## More:
## - Zipf's
## - Benford's

