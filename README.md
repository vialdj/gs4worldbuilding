[![CodeFactor](https://www.codefactor.io/repository/github/vialdj/worldgen/badge/master?s=dce5f6dc560c4ed1e7f9a31a4bbb7231532176d1)](https://www.codefactor.io/repository/github/vialdj/worldgen/overview/master)
[![Build Status](https://travis-ci.com/vialdj/worldgen.svg?token=qyErTtyxDDzuR3xx3yks&branch=master)](https://travis-ci.com/vialdj/worldgen)
[![Coverage Status](https://coveralls.io/repos/github/vialdj/worldgen/badge.svg?branch=master&t=zTOnZw)](https://coveralls.io/github/vialdj/worldgen?branch=master)

# worldgen
Worldgen allows you to randomly generates worlds, stars and star systems based on the GURPS Space 4th Edition design sequence.

## Dice rolls to random numbers
### Roll for condition
When a value is generated through a dice roll to test some condition, a value is drawn from a continuous uniform probability distribution with a=0 and b=1. Then the drawn value is compared to the test success probability.

example: if 3d6 > 11 becomes if x < .375 where x is drawn from an uniform distribution with a=0 and b=1.

### Roll for continuous variable
When a discrete value generated through a dice roll is used in some continuous variable equation, a value is drawn from a continuous probability distribution instead. The distribution law is picked to fit the roll's specifics as such:

| N d6 | Distribution |
|:-:|:-:|
| 1 | uniform |
| 2 | triangular |
| 3 | truncated normal |

examples include:
* (1d6 + 2) / 10 becomes a draw from an uniform distribution with a=.3 and b=.8
* max(2d6 - 7, 0) / 10 becomes max(x, 0) where x is drawn from a triangular distribution with a=-.5, b=0 and c=.5.
* 3d6 / 10 becomes a draw from a truncated normal mu=1.05, sigma=2.958040, a=(.3 - 1.05) / sigma and b=(1.8 - 1.05) / sigma