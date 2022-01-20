[![CodeFactor](https://www.codefactor.io/repository/github/vialdj/gs4worldbuilding/badge)](https://www.codefactor.io/repository/github/vialdj/gs4worldbuilding)
[![Build Status](https://app.travis-ci.com/vialdj/gs4worldbuilding.svg?branch=master)](https://app.travis-ci.com/vialdj/gs4worldbuilding)
[![Coverage Status](https://coveralls.io/repos/github/vialdj/gs4worldbuilding/badge.svg?branch=master)](https://coveralls.io/github/vialdj/gs4worldbuilding?branch=master)

# gs4worldbuilding (WIP, unstable!)
gs4worldbuilding implement the model defined in the GURPS Space (4th Edition) design sequence. It allows you to randomly generates worlds, stars and star systems. Once an object is generated through any of the available methods, you can then tune some of its properties while keeping the model consistent.

## Dice rolls to random numbers
### Roll for continuous variable
When a discrete value generated through n d6 rolls is used in some continuous variable definition, a value is drawn from a continuous probability distribution instead. The distribution law is picked to fit the roll's specifics as such:

| N d6 | Distribution |
|:-:|:-:|
| 1 | uniform |
| 2 | triangular |
| 3 | truncated normal |

examples include:
* (1d6 + 2) / 10 becomes a draw from an uniform distribution with a=.3 and b=.8
* max(2d6 - 7, 0) / 10 becomes max(x, 0) where x is drawn from a triangular distribution with a=-.5, b=0 and c=.5.
* 3d6 / 10 becomes a draw from a truncated normal / 10 with mu=10.5, sigma=2.958040, a=(3 - 10.5) / sigma and b=(18 - 10.5) / sigma

Some complex continuous variable definition procedures distributions have been fitted through various method and are demonstrated in [individual notebooks here](https://github.com/vialdj/gs4worldbuilding_notebooks).

### Roll on a table with discrete outcomes & roll for condition
When a discrete value generated through n d6 rolls is used to match some population of discrete values on a table or to test some condition, n randint(1, 6) draws are summed.

## Model extensions
### Orbital parameters
For completeness, some orbital elements can be added to the GURPS generated semimajor-axis and eccentricity.

#### Inclination i 
The orbital inclination (in degrees) of objects in respect to the generated star system's reference plane is drawn from a Rayleigh distribution with a mode of 2.

#### Longitude of the ascending node Ω
The longitude of the ascending node (in degrees) is drawn from a uniform distribution between -180 and 180.

#### Argument of periapsis ω
The argument of periapsis (in degrees) is drawn from a uniform distribution between 0 and 360.

#### Mean anomaly at epoch M0
The mean anomaly at epoch (in degrees) is drawn from a uniform distribution between 0 and 360.
