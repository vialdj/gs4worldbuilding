# -*- coding: utf-8 -*-

import numpy as np
import random
from enum import Enum
from collections import namedtuple
from math import sqrt, floor, exp
from cst_random import truncated_normal

class World(object):
    """The World Model"""

    """Internal Core Enum from World Density Table"""
    class Core(Enum):
        NONE = 0
        ICY_CORE = 1
        SMALL_IRON_CORE = 2
        LARGE_IRON_CORE = 3

    """Internal Size Enum from Size Constraints Table"""
    class Size(Enum):
        NONE = 0
        TINY = 1
        SMALL = 2
        STANDARD = 3
        LARGE = 4

    def __init__(self, avg_srf_temperature, absorption_factor,
                 size=Size.NONE, core=Core.NONE, ocean_coverage=.0,
                 rel_atm_mass=.0, atm_key_elems=[],
                 greenhouse_factor=.0, pressure_factor=.0):
        self.ocean_coverage = ocean_coverage
        # relative supply of gaseous volatiles to other worlds of the same type
        self.rel_atm_mass = rel_atm_mass
        self.atm_key_elems = atm_key_elems
        self.avg_srf_temperature = avg_srf_temperature
        density = self.__density(core)
        self.density = density
        blackbody_temperature = self.__blackbody_temperature(absorption_factor,
                                                             greenhouse_factor,
                                                             rel_atm_mass,
                                                             avg_srf_temperature)
        self.blackbody_temperature = blackbody_temperature
        diameter = self.__diameter(size, blackbody_temperature, density)
        self.diameter = diameter
        surface_gravity = density * diameter
        self.surface_gravity = surface_gravity
        self.mass = density * diameter**3
        self.atm_pressure = rel_atm_mass * pressure_factor * surface_gravity

        # A string describing the core
        self.core = core
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

    """Comparison to World Climate Table"""
    def __climate(self, t):
        d = {244: 'Frozen', 255: 'Very Cold', 266: 'Cold', 278: 'Chilly',
             289: 'Cool', 300: 'Normal', 311: 'Warm', 322: 'Tropical',
             333: 'Hot', 344: 'Very Hot'}
        for k in sorted(d.keys()):
            if t < k: return d[k]
        return 'Infernal'

    """ blackbody temperature B = T / C where C = A * [1 + (M * G)]
    with A the absorption factor, M the relative atmospheric mass and G the
    greenhouse factor (A and G given in the Temperature Factors Table)"""
    def __blackbody_temperature(self,
                                absorption_factor,
                                greenhouse_factor,
                                rel_atm_mass,
                                avg_srf_temperature):
        return avg_srf_temperature / (absorption_factor *
                                      floor(1 + rel_atm_mass *
                                            greenhouse_factor))

    """ roll of 2d-2 in range [Dmin, Dmax]"""
    def __diameter(self, size, blackbody_temperature, density):
        if size != self.Size.NONE:
            SizeConstraint = namedtuple('SizeConstraint', ['min','max'])
            d = {self.Size.TINY: SizeConstraint(0.004, 0.024),
                 self.Size.SMALL: SizeConstraint(0.024, 0.030),
                 self.Size.STANDARD: SizeConstraint(0.030, 0.065),
                 self.Size.LARGE: SizeConstraint(0.065, 0.091)}
            dmin = sqrt(blackbody_temperature / density) * d[size].min
            dmax = sqrt(blackbody_temperature / density) * d[size].max
            return dmin + np.random.triangular(0, .5, 1) * (dmax - dmin)
        return .0

    """sum of a 3d roll over World Density Table"""
    def __density(self, core):
        if core != self.Core.NONE:
            densities = {self.Core.ICY_CORE: [0.3, 0.4, 0.5, 0.6, 0.7],
                         self.Core.SMALL_IRON_CORE: [0.6, 0.7, 0.8, 0.9, 1.0],
                         self.Core.LARGE_IRON_CORE: [0.8, 0.9, 1.0, 1.1, 1.2]}
            return np.random.choice(densities[core],
                                    p=[0.0926, 0.4074, 0.4074, 0.08797, 0.00463])
        return .0

class TinySulfur(World):
    def __init__(self):
        super(TinySulfur, self).__init__(avg_srf_temperature=random.randint(80, 140),
                                         absorption_factor=.77,
                                         core=self.Core.ICY_CORE,
                                         size=self.Size.TINY)

class TinyIce(World):
    def __init__(self):
        super(TinyIce, self).__init__(avg_srf_temperature=random.randint(80, 140),
                                      size=self.Size.TINY,
                                      absorption_factor=.86,
                                      core=self.Core.ICY_CORE)

class TinyRock(World):
    def __init__(self):
        super(TinyRock, self).__init__(avg_srf_temperature=random.randint(140, 500),
                                       size=self.Size.TINY, absorption_factor=.97,
                                       core=self.Core.SMALL_IRON_CORE)

class SmallHadean(World):
    def __init__(self):
        super(SmallHadean, self).__init__(avg_srf_temperature=random.randint(50, 80),
                                          size=self.Size.SMALL, absorption_factor=.67,
                                          core=self.Core.ICY_CORE)

class SmallIce(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        """roll of 1d+2 divided by 10"""
        ocean_coverage = random.uniform(.3, .8)
        super(SmallIce, self).__init__(ocean_coverage=ocean_coverage,
                                       rel_atm_mass=rel_atm_mass,
                                       atm_key_elems=['N2', 'CH4'],
                                       avg_srf_temperature=random.randint(80, 140),
                                       size=self.Size.SMALL,
                                       absorption_factor=.93,
                                       greenhouse_factor=.1,
                                       pressure_factor=10,
                                       core=self.Core.ICY_CORE)

class SmallRock(World):
    def __init__(self):
        super(SmallRock, self).__init__(avg_srf_temperature=random.randint(140, 500),
                                        size=self.Size.SMALL,
                                        absorption_factor=.96,
                                        core=self.Core.SMALL_IRON_CORE)

class StandardChthonian(World):
    def __init__(self):
        super(StandardChthonian, self).__init__(avg_srf_temperature=random.randint(500, 950),
                                                size=self.Size.STANDARD,
                                                absorption_factor=.97,
                                                core=self.Core.LARGE_IRON_CORE)

class StandardGreenhouse(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        """adjusted ocean coverage between 0 and .5 using exponential distribution
        with scale 5. increase scale to make high value rarer."""
        ocean_coverage = exp(-np.random.exponential(scale=5)) * .5
        super(StandardGreenhouse, self).__init__(ocean_coverage=ocean_coverage,
                                                 rel_atm_mass=rel_atm_mass,
                                                 atm_key_elems=['CO2'] if ocean_coverage < .1 else ['N2', 'H2O', 'O2'],
                                                 avg_srf_temperature=random.randint(500, 950),
                                                 size=self.Size.STANDARD,
                                                 absorption_factor=.77,
                                                 greenhouse_factor=2.0,
                                                 pressure_factor=100,
                                                 core=self.Core.LARGE_IRON_CORE)

class StandardAmmonia(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        super(StandardAmmonia, self).__init__(ocean_coverage=random.uniform(.5, 1.0),
                                              rel_atm_mass=rel_atm_mass,
                                              atm_key_elems=['N2', 'NH3', 'CH4'],
                                              avg_srf_temperature=random.randint(140, 215),
                                              size=self.Size.STANDARD,
                                              absorption_factor=.84,
                                              greenhouse_factor=.2,
                                              pressure_factor=1,
                                              core=self.Core.ICY_CORE)

class StandardHadean(World):
    def __init__(self):
        """sum of a 3d roll over World Density Table for Icy Core"""
        super(StandardHadean, self).__init__(avg_srf_temperature=random.randint(50, 80),
                                             size=self.Size.STANDARD,
                                             absorption_factor=.67,
                                             core=self.Core.ICY_CORE)

class StandardIce(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        super(StandardIce, self).__init__(ocean_coverage=random.uniform(.0, .2),
                                          rel_atm_mass=rel_atm_mass,
                                          atm_key_elems=['CO2', 'N2'],
                                          avg_srf_temperature=random.randint(80, 230),
                                          size=self.Size.STANDARD,
                                          absorption_factor=.86,
                                          greenhouse_factor=.2,
                                          pressure_factor=1,
                                          core=self.Core.LARGE_IRON_CORE)

class StandardOcean(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        """adjusted ocean coverage between .5 and 1.0 using normal distribution
        with mean of .75 and standard deviation of .1"""
        ocean_coverage = truncated_normal(loc=.75, scale=.1, low=.5, up=1.0)
        super(StandardOcean, self).__init__(ocean_coverage=ocean_coverage,
                                            rel_atm_mass=rel_atm_mass,
                                            atm_key_elems=['CO2', 'N2'],
                                            avg_srf_temperature=random.randint(250, 340),
                                            size=self.Size.STANDARD,
                                            absorption_factor=.88,
                                            greenhouse_factor=.16,
                                            pressure_factor=1,
                                            core=self.Core.LARGE_IRON_CORE)

class StandardGarden(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        """adjusted ocean coverage between .5 and 1.0 using normal distribution
        with mean of .75 and standard deviation of .1"""
        ocean_coverage = truncated_normal(loc=.75, scale=.1, low=.5, up=1.0)
        super(StandardGarden, self).__init__(ocean_coverage=ocean_coverage,
                                             rel_atm_mass=rel_atm_mass,
                                             atm_key_elems=['N2', 'O2'],
                                             avg_srf_temperature=random.randint(250, 340),
                                             size=self.Size.STANDARD,
                                             absorption_factor=.88,
                                             greenhouse_factor=.16,
                                             pressure_factor=1,
                                             core=self.Core.LARGE_IRON_CORE)

class LargeChthonian(World):
    def __init__(self):
        super(LargeChthonian, self).__init__(avg_srf_temperature=random.randint(500, 950),
                                             size=self.Size.LARGE,
                                             absorption_factor=.97,
                                             core=self.Core.LARGE_IRON_CORE)

class LargeGreenhouse(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        """adjusted ocean coverage between 0 and .5 using exponential distribution
        with scale 5. increase scale to make high value rarer."""
        ocean_coverage = exp(-np.random.exponential(scale=5)) * .5
        super(LargeGreenhouse, self).__init__(ocean_coverage=ocean_coverage,
                                              rel_atm_mass=rel_atm_mass,
                                              atm_key_elems=['CO2'] if ocean_coverage < .1 == 0 else ['N2', 'H2O', 'O2'],
                                              avg_srf_temperature=random.randint(500, 950),
                                              size=self.Size.LARGE,
                                              absorption_factor=.77,
                                              greenhouse_factor=2.0,
                                              pressure_factor=500,
                                              core=self.Core.LARGE_IRON_CORE)

class LargeAmmonia(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        """sum of a 3d roll over World Density Table for Icy Core"""
        super(LargeAmmonia, self).__init__(ocean_coverage=random.uniform(0.5, 1.0),
                                           rel_atm_mass=rel_atm_mass,
                                           atm_key_elems=['He', 'NH3', 'CH4'],
                                           avg_srf_temperature=random.randint(140, 215),
                                           size=self.Size.LARGE,
                                           absorption_factor=.84,
                                           greenhouse_factor=.2,
                                           pressure_factor=5,
                                           core=self.Core.ICY_CORE)

class LargeIce(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        super(LargeIce, self).__init__(ocean_coverage=random.uniform(.0, .2),
                                       rel_atm_mass=rel_atm_mass,
                                       atm_key_elems=['He', 'N2'],
                                       avg_srf_temperature=random.randint(80, 230),
                                       size=self.Size.LARGE,
                                       absorption_factor=.86,
                                       greenhouse_factor=.2,
                                       pressure_factor=5,
                                       core=self.Core.LARGE_IRON_CORE)

class LargeOcean(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        """adjusted ocean coverage between .7 and 1.0 using normal distribution
        with mean of .85 and standard deviation of .075"""
        ocean_coverage = truncated_normal(loc=.85, scale=.075, low=.7, up=1.0)
        super(LargeOcean, self).__init__(ocean_coverage=ocean_coverage,
                                         rel_atm_mass=rel_atm_mass,
                                         atm_key_elems=['He', 'N2'],
                                         avg_srf_temperature=random.randint(250, 340),
                                         size=self.Size.LARGE,
                                         absorption_factor=.88,
                                         greenhouse_factor=.16,
                                         pressure_factor=5,
                                         core=self.Core.LARGE_IRON_CORE)

class LargeGarden(World):
    def __init__(self):
        """sum of a 3d roll divided by 10"""
        rel_atm_mass = truncated_normal(loc=10.5, scale=2.958040, low=3, up=18) / 10
        """adjusted ocean coverage between .7 and 1.0 using normal distribution
        with mean of .85 and standard deviation of .075"""
        ocean_coverage = truncated_normal(loc=.85, scale=.075, low=.7, up=1.0)
        super(LargeGarden, self).__init__(ocean_coverage=ocean_coverage,
                                          rel_atm_mass=rel_atm_mass,
                                          atm_key_elems=['N2', 'O2', 'He', 'Ne', 'Ar',
                                                         'Kr', 'Xe'],
                                          avg_srf_temperature=random.randint(250, 340),
                                          size=self.Size.LARGE,
                                          absorption_factor=.88,
                                          greenhouse_factor=.16,
                                          pressure_factor=5,
                                          core=self.Core.LARGE_IRON_CORE)

class AsteroidBelt(World):
    def __init__(self):
        super(AsteroidBelt, self).__init__(avg_srf_temperature=random.randint(140, 500),
                                           absorption_factor=.97)
