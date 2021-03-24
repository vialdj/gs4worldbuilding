# -*- coding: utf-8 -*-

import numpy as np
import random
from enum import Enum
from math import sqrt, floor
from scipy.stats import truncnorm

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

    def __init__(self, temp, absorption, size=Size.NONE, core=Core.NONE,
                 oceans=.0, atm=[], greenhouse=.0, pressure=.0):
        # the ocean coverage proportion
        self.oceans = oceans
        # key elements in the atmosphere
        self.atm = atm
        # relative supply of gaseous atm to other worlds of the same type
        atm_mass = self.__atm_mass(atm)
        self.atm_mass = atm_mass
        # average surface temperature in K
        self.temp = temp
        # climate type
        self.climate = self.__climate(temp)
        # blackbody temperature in K
        bb_temp = self.__blackbody_temperature(absorption, greenhouse, atm_mass,
                                               temp)
        self.bb_temp = bb_temp
        # core type
        self.core = core
        # density in d⊕
        density = self.__density(core)
        self.density = density
        # diameter in D⊕
        diameter = self.__diameter(size, bb_temp, density)
        self.diameter = diameter
        # surface gravity in G⊕
        gravity = density * diameter
        self.gravity = gravity
        # mass in M⊕
        self.mass = density * diameter**3
        # atmospheric pressure in atm⊕
        self.atm_pressure = atm_mass * pressure * gravity

    """Match surface temperature to World Climate Table"""
    def __climate(self, temp):
        d = {244: 'Frozen', 255: 'Very Cold', 266: 'Cold', 278: 'Chilly',
             289: 'Cool', 300: 'Normal', 311: 'Warm', 322: 'Tropical',
             333: 'Hot', 344: 'Very Hot'}
        for k in sorted(d.keys()):
            if temp < k: return d[k]
        return 'Infernal'

    """ blackbody temperature B = T / C where C = A * [1 + (M * G)]
    with A the absorption factor, M the relative atmospheric mass and G the
    greenhouse factor (A and G given in the Temperature Factors Table)"""
    def __blackbody_temperature(self, absorption, greenhouse, atm, temp):
        return temp / (absorption * floor(1 + atm * greenhouse))

    """ roll of 2d-2 in range [Dmin, Dmax]"""
    def __diameter(self, size, bb_temp, density):
        if size != self.Size.NONE:
            d = {self.Size.TINY: (0.004, 0.024), self.Size.SMALL: (0.024, 0.030),
                 self.Size.STANDARD: (0.030, 0.065), self.Size.LARGE: (0.065, 0.091)}
            dmin = sqrt(bb_temp / density) * d[size][0]
            dmax = sqrt(bb_temp / density) * d[size][1]
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

    """sum of a 3d roll divided by 10"""
    def __atm_mass(self, atm):
        if len(atm) > 0:
            return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                             loc=10.5, scale=2.958040).rvs() / 10
        return .0

    def __str__(self):
        return '{self.__class__.__name__} (ocean coverage= {self.oceans:.2f}, \
atmosphere composition= {self.atm}, \
atmosphere pressure= {self.atm_pressure:.2f} atm⊕, \
average surface temperature= {self.temp} K, \
climate= {self.climate}, \
blackbody temperature= {self.bb_temp:.2f} K, \
density= {self.density:.2f} d⊕, \
core= {self.core}, \
diameter= {self.diameter:.2f} D⊕, \
gravity= {self.gravity:.2f} G⊕, \
mass= {self.mass:.2f} M⊕)'.format(self=self)



class TinySulfur(World):
    def __init__(self):
        super(TinySulfur, self).__init__(temp=random.randint(80, 140),
                                         absorption=.77, core=self.Core.ICY_CORE,
                                         size=self.Size.TINY)

class TinyIce(World):
    def __init__(self):
        super(TinyIce, self).__init__(temp=random.randint(80, 140),
                                      size=self.Size.TINY, absorption=.86,
                                      core=self.Core.ICY_CORE)

class TinyRock(World):
    def __init__(self):
        super(TinyRock, self).__init__(temp=random.randint(140, 500),
                                       size=self.Size.TINY, absorption=.97,
                                       core=self.Core.SMALL_IRON_CORE)

class SmallHadean(World):
    def __init__(self):
        super(SmallHadean, self).__init__(temp=random.randint(50, 80),
                                          size=self.Size.SMALL, absorption=.67,
                                          core=self.Core.ICY_CORE)

class SmallIce(World):
    def __init__(self):
        """roll of 1d+2 divided by 10"""
        oceans = random.uniform(.3, .8)
        super(SmallIce, self).__init__(oceans=oceans, atm=['N2', 'CH4'],
                                       temp=random.randint(80, 140),
                                       size=self.Size.SMALL, pressure=10,
                                       absorption=.93, greenhouse=.1,
                                       core=self.Core.ICY_CORE)

class SmallRock(World):
    def __init__(self):
        super(SmallRock, self).__init__(temp=random.randint(140, 500),
                                        size=self.Size.SMALL, absorption=.96,
                                        core=self.Core.SMALL_IRON_CORE)

class StandardChthonian(World):
    def __init__(self):
        super(StandardChthonian, self).__init__(temp=random.randint(500, 950),
                                                size=self.Size.STANDARD,
                                                absorption=.97,
                                                core=self.Core.LARGE_IRON_CORE)

class StandardGreenhouse(World):
    def __init__(self):
        super(StandardGreenhouse, self).__init__(atm=['CO2'], pressure=100,
                                                 temp=random.randint(500, 950),
                                                 size=self.Size.STANDARD,
                                                 absorption=.77, greenhouse=2.0,
                                                 core=self.Core.LARGE_IRON_CORE)

class StandardAmmonia(World):
    def __init__(self):
        """roll of 2d maximum at 10 and divided by 10"""
        oceans = min(np.random.triangular(0.2, .7, 1.2), 1)
        super(StandardAmmonia, self).__init__(oceans=oceans, pressure=1,
                                              atm=['N2', 'NH3', 'CH4'],
                                              temp=random.randint(140, 215),
                                              size=self.Size.STANDARD,
                                              absorption=.84, greenhouse=.2,
                                              core=self.Core.ICY_CORE)

class StandardHadean(World):
    def __init__(self):
        super(StandardHadean, self).__init__(temp=random.randint(50, 80),
                                             size=self.Size.STANDARD,
                                             absorption=.67,
                                             core=self.Core.ICY_CORE)

class StandardIce(World):
    def __init__(self):
        """roll of 2d-10 minimum at 0 and divided by 10"""
        oceans = max(np.random.triangular(-.8, -.3, .2), 0)
        super(StandardIce, self).__init__(oceans=oceans, atm=['CO2', 'N2'],
                                          temp=random.randint(80, 230),
                                          absorption=.86, greenhouse=.2,
                                          pressure=1, size=self.Size.STANDARD,
                                          core=self.Core.LARGE_IRON_CORE)

class StandardOcean(World):
    def __init__(self):
        """roll of 1d+4 divided by 10"""
        oceans = random.uniform(.5, 1.0)
        super(StandardOcean, self).__init__(oceans=oceans, atm=['CO2', 'N2'],
                                            temp=random.randint(250, 340),
                                            size=self.Size.STANDARD, pressure=1,
                                            absorption=.88, greenhouse=.16,
                                            core=self.Core.LARGE_IRON_CORE)

class StandardGarden(World):
    def __init__(self):
        """roll of 1d+4 divided by 10"""
        oceans = random.uniform(.5, 1.0)
        super(StandardGarden, self).__init__(oceans=oceans, atm=['N2', 'O2'],
                                             temp=random.randint(250, 340),
                                             size=self.Size.STANDARD, pressure=1,
                                             absorption=.88, greenhouse=.16,
                                             core=self.Core.LARGE_IRON_CORE)

class LargeChthonian(World):
    def __init__(self):
        super(LargeChthonian, self).__init__(temp=random.randint(500, 950),
                                             size=self.Size.LARGE,
                                             absorption=.97,
                                             core=self.Core.LARGE_IRON_CORE)

class LargeGreenhouse(World):
    def __init__(self):
        super(LargeGreenhouse, self).__init__(atm=['CO2'], size=self.Size.LARGE,
                                              temp=random.randint(500, 950),
                                              absorption=.77, greenhouse=2.0,
                                              pressure=500,
                                              core=self.Core.LARGE_IRON_CORE)

class LargeAmmonia(World):
    def __init__(self):
        """roll of 2d capped at 10 and divided by 10"""
        oceans = min(np.random.triangular(0.2, .7, 1.2), 1)
        super(LargeAmmonia, self).__init__(oceans=oceans, size=self.Size.LARGE,
                                           atm=['He', 'NH3', 'CH4'],
                                           temp=random.randint(140, 215),
                                           absorption=.84, greenhouse=.2,
                                           pressure=5, core=self.Core.ICY_CORE)

class LargeIce(World):
    def __init__(self):
        """roll of 2d-10 minimum at 0 and divided by 10"""
        oceans = max(np.random.triangular(-.8, -.3, .2), 0)
        super(LargeIce, self).__init__(oceans=oceans, atm=['He', 'N2'],
                                       temp=random.randint(80, 230),
                                       size=self.Size.LARGE, absorption=.86,
                                       greenhouse=.2, pressure=5,
                                       core=self.Core.LARGE_IRON_CORE)

class LargeOcean(World):
    def __init__(self):
        """roll of 1d+6 maxed at 10 divided by 10"""
        oceans = min(random.uniform(.7, 1.2), 1)
        super(LargeOcean, self).__init__(oceans=oceans, atm=['He', 'N2'],
                                         temp=random.randint(250, 340),
                                         size=self.Size.LARGE, pressure=5,
                                         absorption=.88, greenhouse=.16,
                                         core=self.Core.LARGE_IRON_CORE)

class LargeGarden(World):
    def __init__(self):
        """roll of 1d+6 maxed at 10 divided by 10"""
        oceans = min(random.uniform(.7, 1.2), 1)
        super(LargeGarden, self).__init__(oceans=oceans, size=self.Size.LARGE,
                                          atm=['N2', 'O2', 'He', 'Ne', 'Ar',
                                               'Kr', 'Xe'], pressure=5,
                                          temp=random.randint(250, 340),
                                          absorption=.88, greenhouse=.16,
                                          core=self.Core.LARGE_IRON_CORE)

class AsteroidBelt(World):
    def __init__(self):
        super(AsteroidBelt, self).__init__(temp=random.randint(140, 500),
                                           absorption=.97)
