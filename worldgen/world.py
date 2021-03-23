# -*- coding: utf-8 -*-

import numpy as np
import random
from collections import namedtuple
from math import sqrt, floor, exp
from cst_random import truncated_normal

"""dependent to worldtype given in gurps space 4th edition Size Constraints
Table"""
SizeConstraint = namedtuple('SizeConstraint', ['minimum','maximum'])

class World(object):
    """The world model. Each World Types is build using a proccess close to the
    World Design Sequence from gurps space 4th edition step 2 to step 5.
    World Types are represented by the World subclasses"""
    def __init__(self, avg_srf_temperature, absorption_factor,
                 size_constraint=SizeConstraint(0, 0),
                 core='Unapplicable', density=.0, ocean_coverage=.0,
                 relative_atm_mass=.0, atm_key_elems=[],
                 greenhouse_factor=.0, pressure_factor=.0):
        # The proportion of surface occupied by liquid elements
        self.ocean_coverage = ocean_coverage
        # relative supply of gaseous volatiles to other worlds of the same type
        self.relative_atm_mass = relative_atm_mass
        # atm composition as a list of elements
        self.atm_key_elems = atm_key_elems
        # The average temperature in kelvins K
        self.avg_srf_temperature = avg_srf_temperature
        # The density of the world in earth densities d⊕
        self.density = density
        # The blackbody temperature in kelvin
        blackbody_temperature = self.__blackbody_temperature(absorption_factor,
                                                             greenhouse_factor,
                                                             relative_atm_mass,
                                                             avg_srf_temperature)
        self.blackbody_temperature = blackbody_temperature
        # The world diameter in D⊕
        diameter = self.__diameter(size_constraint,
                                   blackbody_temperature,
                                   density) if density > 0 else .0
        self.diameter = diameter
        # The surface gravity in G⊕ as S = d * D with density d and diameter D
        surface_gravity = density * diameter
        self.surface_gravity = surface_gravity
        # The mass in M⊕ as m = d * D^3 with density d and diameter D
        self.mass = density * diameter**3
        """The world atmospheric pressure in atm⊕ as P = M * F * S with A the
        relative supply of gaseous volatiles to other worlds of the same type,
        F the given pressure factor according to gurps space 4th edition
        Pressure Factors Table and the surface gravity S"""
        self.atm_pressure = relative_atm_mass * pressure_factor * surface_gravity

        # A string describing the core
        self.core = core
        # A string corresponding to the gurps projected climate
        self.climate = self.__climate(avg_srf_temperature)

    def __str__(self):
        return '{self.__class__.__name__} (ocean coverage= {self.ocean_coverage:.2f}, \
atmosphere composition= {self.atm_key_elems}, \
atmosphere pressure= {self.atm_pressure:.2f} atm⊕, \
average surface temperature= {self.avg_srf_temperature} K, \
climate= {self.climate}, \
blackbody temperature= {self.blackbody_temperature:.2f} K, \
density= {self.density:.2f} d⊕, \
core= {self.core}, \
diameter= {self.diameter:.2f} D⊕, \
gravity= {self.surface_gravity:.2f} G⊕, \
mass= {self.mass:.2f} M⊕)'.format(self=self)

    """associate proper climate from given average surface temperature in K
    based on gurps space 4th edition World Climate Table"""
    def __climate(self, temperature):
        if temperature < 244:
            return 'Frozen'
        elif 244 <= temperature < 255:
            return 'Very Cold'
        elif 255 <= temperature < 266:
            return 'Cold'
        elif 266 <= temperature < 278:
            return 'Chilly'
        elif 278 <= temperature < 289:
            return 'Cool'
        elif 289 <= temperature < 300:
            return 'Normal'
        elif 300 <= temperature < 311:
            return 'Warm'
        elif 311 <= temperature < 322:
            return 'Tropical'
        elif 322 <= temperature < 333:
            return 'Hot'
        elif 333 <= temperature < 344:
            return 'Very Hot'
        else:
            return 'Infernal'

    """ From gurps space 4th edition as blackbody temperature B = T / C where
    C = A * [1 + (M * G)] with A the absorption factor, M the relative
    atmospheric mass and G the greenhouse factor (A and G given in the
    Temperature Factors Table)"""
    def __blackbody_temperature(self,
                                absorption_factor,
                                greenhouse_factor,
                                relative_atm_mass,
                                avg_srf_temperature):
        return avg_srf_temperature / (absorption_factor * floor(1 + relative_atm_mass * greenhouse_factor))

    """ Select a diameter at random from gurps space 4th edition as diameter
    range in [Dmin, Dmax] as Dmin = sqrt(B / K) * size_constraint.minimum and
    Dmax = sqrt(B / K) * size_constraint.maximum with B is blackbody_temperature
    and K is density"""
    def __diameter(self, size_constraint, blackbody_temperature, density):
        dmin = sqrt(blackbody_temperature / density) * size_constraint.minimum
        dmax = sqrt(blackbody_temperature / density) * size_constraint.maximum
        """random value between 0 and 1 using normal distribution
        with mean of .5 and standard deviation of .2"""
        f = truncated_normal(loc=.5, scale=.2, low=.0, up=1.0)
        return dmin + f * (dmax - dmin)

class TinySulfur(World):
    def __init__(self):
        """density between .3 and .7 using normal distribution
        with mean of .5 and standard deviation of .08"""
        density = truncated_normal(loc=.5, scale=.08, low=.3, up=.7)
        super(TinySulfur, self).__init__(avg_srf_temperature=random.randint(80, 140),
                                         density=density, absorption_factor=.77,
                                         core='Icy Core')

class TinyIce(World):
    def __init__(self):
        """density between .3 and .7 using normal distribution
        with mean of .5 and standard deviation of .08"""
        density = truncated_normal(loc=.5, scale=.08, low=.3, up=.7)
        super(TinyIce, self).__init__(avg_srf_temperature=random.randint(80, 140),
                                      size_constraint=SizeConstraint(0.004, 0.024),
                                      density=density, absorption_factor=.86,
                                      core='Icy Core')

class TinyRock(World):
    def __init__(self):
        """density between .6 and 1.0 using normal distribution
        with mean of .8 and standard deviation of .08"""
        density = truncated_normal(loc=.8, scale=.08, low=.6, up=1.0)
        super(TinyRock, self).__init__(avg_srf_temperature=random.randint(140, 500),
                                       size_constraint=SizeConstraint(0.004, 0.024),
                                       density=density, absorption_factor=.97,
                                       core='Small Iron Core')

class SmallHadean(World):
    def __init__(self):
        """density between .3 and .7 using normal distribution
        with mean of .5 and standard deviation of .08"""
        density = truncated_normal(loc=.5, scale=.08, low=.3, up=.7)
        super(SmallHadean, self).__init__(avg_srf_temperature=random.randint(50, 80),
                                          size_constraint=SizeConstraint(0.024, 0.030),
                                          density=density, absorption_factor=.67,
                                          core='Icy Core')

class SmallIce(World):
    def __init__(self):
        """density between .3 and .7 using normal distribution
        with mean of .5 and standard deviation of .08"""
        density = truncated_normal(loc=.5, scale=.08, low=.3, up=.7)
        super(SmallIce, self).__init__(ocean_coverage=random.uniform(.3, .8),
                                       relative_atm_mass=random.uniform(.5, 1.5),
                                       atm_key_elems=['N2', 'CH4'],
                                       avg_srf_temperature=random.randint(80, 140),
                                       size_constraint=SizeConstraint(0.024, 0.030),
                                       absorption_factor=.93,
                                       greenhouse_factor=.1,
                                       pressure_factor=10,
                                       density=density,
                                       core='Icy Core')

class SmallRock(World):
    def __init__(self):
        """density between .6 and 1.0 using normal distribution
        with mean of .8 and standard deviation of .08"""
        density = truncated_normal(loc=.8, scale=.08, low=.6, up=1.0)
        super(SmallRock, self).__init__(avg_srf_temperature=random.randint(140, 500),
                                        size_constraint=SizeConstraint(0.024, 0.030),
                                        density=density, absorption_factor=.96,
                                        core='Small Iron Core')

class StandardChthonian(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        super(StandardChthonian, self).__init__(avg_srf_temperature=random.randint(500, 950),
                                                size_constraint=SizeConstraint(0.030, 0.065),
                                                density=density,
                                                absorption_factor=.97,
                                                core='Large Iron Core')

class StandardGreenhouse(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        """adjusted ocean coverage between 0 and .5 using exponential distribution
        with scale 5. increase scale to make high value rarer."""
        ocean_coverage = exp(-np.random.exponential(scale=5)) * .5
        super(StandardGreenhouse, self).__init__(ocean_coverage=ocean_coverage,
                                                 relative_atm_mass=random.uniform(.5, 1.5),
                                                 atm_key_elems=['CO2'] if ocean_coverage < .1 else ['N2', 'H2O', 'O2'],
                                                 avg_srf_temperature=random.randint(500, 950),
                                                 size_constraint=SizeConstraint(0.030, 0.065),
                                                 absorption_factor=.77,
                                                 greenhouse_factor=2.0,
                                                 pressure_factor=100,
                                                 density=density,
                                                 core='Large Iron Core')

class StandardAmmonia(World):
    def __init__(self):
        """density between .3 and .7 using normal distribution
        with mean of .5 and standard deviation of .08"""
        density = truncated_normal(loc=.5, scale=.08, low=.3, up=.7)
        super(StandardAmmonia, self).__init__(ocean_coverage=random.uniform(.5, 1.0),
                                              relative_atm_mass=random.uniform(.5, 1.5),
                                              atm_key_elems=['N2', 'NH3', 'CH4'],
                                              avg_srf_temperature=random.randint(140, 215),
                                              size_constraint=SizeConstraint(0.030, 0.065),
                                              absorption_factor=.84,
                                              greenhouse_factor=.2,
                                              pressure_factor=1,
                                              density=density,
                                              core='Icy Core')

class StandardHadean(World):
    def __init__(self):
        """density between .3 and .7 using normal distribution
        with mean of .5 and standard deviation of .08"""
        density = truncated_normal(loc=.5, scale=.08, low=.3, up=.7)
        super(StandardHadean, self).__init__(avg_srf_temperature=random.randint(50, 80),
                                             size_constraint=SizeConstraint(0.030, 0.065),
                                             absorption_factor=.67,
                                             density=density,
                                             core='Icy Core')

class StandardIce(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        super(StandardIce, self).__init__(ocean_coverage=random.uniform(.0, .2),
                                          relative_atm_mass=random.uniform(.5, 1.5),
                                          atm_key_elems=['CO2', 'N2'],
                                          avg_srf_temperature=random.randint(80, 230),
                                          size_constraint=SizeConstraint(0.030, 0.065),
                                          absorption_factor=.86,
                                          greenhouse_factor=.2,
                                          pressure_factor=1,
                                          density=density,
                                          core='Large Iron Core')

class StandardOcean(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        """adjusted ocean coverage between .5 and 1.0 using normal distribution
        with mean of .75 and standard deviation of .1"""
        ocean_coverage = truncated_normal(loc=.75, scale=.1, low=.5, up=1.0)
        super(StandardOcean, self).__init__(ocean_coverage=ocean_coverage,
                                            relative_atm_mass=random.uniform(.5, 1.5),
                                            atm_key_elems=['CO2', 'N2'],
                                            avg_srf_temperature=random.randint(250, 340),
                                            size_constraint=SizeConstraint(0.030, 0.065),
                                            absorption_factor=.88,
                                            greenhouse_factor=.16,
                                            pressure_factor=1,
                                            density=density,
                                            core='Large Iron Core')

class StandardGarden(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        """adjusted ocean coverage between .5 and 1.0 using normal distribution
        with mean of .75 and standard deviation of .1"""
        ocean_coverage = truncated_normal(loc=.75, scale=.1, low=.5, up=1.0)
        super(StandardGarden, self).__init__(ocean_coverage=ocean_coverage,
                                             relative_atm_mass=random.uniform(.5, 1.5),
                                             atm_key_elems=['N2', 'O2'],
                                             avg_srf_temperature=random.randint(250, 340),
                                             size_constraint=SizeConstraint(0.030, 0.065),
                                             absorption_factor=.88,
                                             greenhouse_factor=.16,
                                             pressure_factor=1,
                                             density=density,
                                             core='Large Iron Core')

class LargeChthonian(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        super(LargeChthonian, self).__init__(avg_srf_temperature=random.randint(500, 950),
                                             size_constraint=SizeConstraint(0.065, 0.091),
                                             absorption_factor=.97,
                                             density=density,
                                             core='Large Iron Core')

class LargeGreenhouse(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        """adjusted ocean coverage between 0 and .5 using exponential distribution
        with scale 5. increase scale to make high value rarer."""
        ocean_coverage = exp(-np.random.exponential(scale=5)) * .5
        super(LargeGreenhouse, self).__init__(ocean_coverage=ocean_coverage,
                                              relative_atm_mass=random.uniform(.5, 1.5),
                                              atm_key_elems=['CO2'] if ocean_coverage < .1 == 0 else ['N2', 'H2O', 'O2'],
                                              avg_srf_temperature=random.randint(500, 950),
                                              size_constraint=SizeConstraint(0.065, 0.091),
                                              absorption_factor=.77,
                                              greenhouse_factor=2.0,
                                              pressure_factor=500,
                                              density=density,
                                              core='Large Iron Core')

class LargeAmmonia(World):
    def __init__(self):
        """density between .3 and .7 using normal distribution
        with mean of .5 and standard deviation of .08"""
        density = truncated_normal(loc=.5, scale=.08, low=.3, up=.7)
        super(LargeAmmonia, self).__init__(ocean_coverage=random.uniform(0.5, 1.0),
                                           relative_atm_mass=random.uniform(.5, 1.5),
                                           atm_key_elems=['He', 'NH3', 'CH4'],
                                           avg_srf_temperature=random.randint(140, 215),
                                           size_constraint=SizeConstraint(0.065, 0.091),
                                           absorption_factor=.84,
                                           greenhouse_factor=.2,
                                           pressure_factor=5,
                                           density=density,
                                           core='Icy Core')

class LargeIce(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        super(LargeIce, self).__init__(ocean_coverage=random.uniform(.0, .2),
                                       relative_atm_mass=random.uniform(.5, 1.5),
                                       atm_key_elems=['He', 'N2'],
                                       avg_srf_temperature=random.randint(80, 230),
                                       size_constraint=SizeConstraint(0.065, 0.091),
                                       absorption_factor=.86,
                                       greenhouse_factor=.2,
                                       pressure_factor=5,
                                       density=density,
                                       core='Large Iron Core')

class LargeOcean(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        """adjusted ocean coverage between .7 and 1.0 using normal distribution
        with mean of .85 and standard deviation of .075"""
        ocean_coverage = truncated_normal(loc=.85, scale=.075, low=.7, up=1.0)
        super(LargeOcean, self).__init__(ocean_coverage=ocean_coverage,
                                         relative_atm_mass=random.uniform(.5, 1.5),
                                         atm_key_elems=['He', 'N2'],
                                         avg_srf_temperature=random.randint(250, 340),
                                         size_constraint=SizeConstraint(0.065, 0.091),
                                         absorption_factor=.88,
                                         greenhouse_factor=.16,
                                         pressure_factor=5,
                                         density=density,
                                         core='Large Iron Core')

class LargeGarden(World):
    def __init__(self):
        """density between .8 and 1.2 using normal distribution
        with mean of 1.0 and standard deviation of .08"""
        density = truncated_normal(loc=1.0, scale=.08, low=.8, up=1.2)
        """adjusted ocean coverage between .7 and 1.0 using normal distribution
        with mean of .85 and standard deviation of .075"""
        ocean_coverage = truncated_normal(loc=.85, scale=.075, low=.7, up=1.0)
        super(LargeGarden, self).__init__(ocean_coverage=ocean_coverage,
                                          relative_atm_mass=random.uniform(.5, 1.5),
                                          atm_key_elems=['N2', 'O2', 'He', 'Ne', 'Ar',
                                                         'Kr', 'Xe'],
                                          avg_srf_temperature=random.randint(250, 340),
                                          size_constraint=SizeConstraint(0.065, 0.091),
                                          absorption_factor=.88,
                                          greenhouse_factor=.16,
                                          pressure_factor=5,
                                          density=density,
                                          core='Large Iron Core')

class AsteroidBelt(World):
    def __init__(self):
        super(AsteroidBelt, self).__init__(avg_srf_temperature=random.randint(140, 500),
                                           absorption_factor=.97)
