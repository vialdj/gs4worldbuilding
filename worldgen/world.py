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
                 atm=[], pressure=.0, greenhouse=.0, oceans=.0):
        # the ocean coverage proportion
        self.oceans = oceans
        # key elements in the atmosphere
        self.atm = atm
        # relative supply of gaseous atm to other worlds of the same type
        atm_mass = self.__atm_mass(atm)
        self.atm_mass = atm_mass
        # average surface temperature in K
        temp = self.__temp(temp)
        self.temp = temp
        # climate type
        self.climate = self.__climate(temp)
        # blackbody temperature in K
        bb_temp = self.__blackbody_temperature(absorption, greenhouse,
                                               atm_mass, temp)
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
        atm_pressure = atm_mass * pressure * gravity
        self.atm_pressure = atm_pressure
        # atmosphere category
        self.atm_p_category = self.__atm_category(atm_pressure)


    """match surface temperature to World Climate Table"""
    def __climate(self, temp):
        d = {244: 'Frozen', 255: 'Very Cold', 266: 'Cold', 278: 'Chilly',
             289: 'Cool', 300: 'Normal', 311: 'Warm', 322: 'Tropical',
             333: 'Hot', 344: 'Very Hot'}
        k = list(filter(lambda x: x >= temp, sorted(d.keys())))
        return d[k[0]] if len(k) > 0 else 'Infernal'

    """ blackbody temperature B = T / C where C = A * [1 + (M * G)]
    with A the absorption factor, M the relative atmospheric mass and G the
    greenhouse factor (A and G given in the Temperature Factors Table)"""
    def __blackbody_temperature(self, absorption, greenhouse, atm, temp):
        return temp / (absorption * floor(1 + atm * greenhouse))

    """ roll of 2d-2 in range [Dmin, Dmax]"""
    def __diameter(self, size, bb_temp, density):
        if size != self.Size.NONE:
            d = {self.Size.TINY: (0.004, 0.024),
                 self.Size.SMALL: (0.024, 0.030),
                 self.Size.STANDARD: (0.030, 0.065),
                 self.Size.LARGE: (0.065, 0.091)}
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
            return np.random.choice(densities[core], p=[0.0926, 0.4074, 0.4074,
                                                        0.08797, 0.00463])
        return .0

    """sum of a 3d roll divided by 10"""
    def __atm_mass(self, atm):
        if len(atm) > 0:
            return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                             loc=10.5, scale=2.958040).rvs() / 10
        return .0

    """sum of a 3d-3 roll times step value add minimum"""
    def __temp(self, temp):
        min = temp[0]
        max = temp[1]
        roll = truncnorm((0 - 7.5) / 2.958040, (15 - 7.5) / 2.958040,
                         loc=7.5, scale=2.958040).rvs()
        return min + roll / 15 * (max - min)

    """match atmospheric pressure to Atmospheric Pressure Categories Table"""
    def __atm_category(self, pressure):
        d = {.01: 'Trace', .51: 'Very Thin', .81: 'Thin', 1.21: 'Standard',
             1.51: 'Dense', 10: 'Very Dense'}
        k = list(filter(lambda x: x >= pressure, sorted(d.keys())))
        return d[k[0]] if len(k) > 0 else 'Superdense'

    def __str__(self):
        return '{self.__class__.__name__} (ocean coverage= {self.oceans:.2f}, \
atmosphere composition= {self.atm}, \
atmosphere pressure= {self.atm_pressure:.2f} atm⊕ ({self.atm_p_category}), \
average surface temperature= {self.temp:.2f} K ({self.climate}), \
blackbody temperature= {self.bb_temp:.2f} K, \
density= {self.density:.2f} d⊕, \
core= {self.core}, \
diameter= {self.diameter:.2f} D⊕, \
gravity= {self.gravity:.2f} G⊕, \
mass= {self.mass:.2f} M⊕)'.format(self=self)


class TinySulfur(World):
    def __init__(self):
        super(TinySulfur, self).__init__(temp=(80, 140), absorption=.77,
                                         size=self.Size.TINY,
                                         core=self.Core.ICY_CORE)


class TinyIce(World):
    def __init__(self):
        super(TinyIce, self).__init__(temp=(80, 140), absorption=.86,
                                      size=self.Size.TINY,
                                      core=self.Core.ICY_CORE)


class TinyRock(World):
    def __init__(self):
        super(TinyRock, self).__init__(temp=(140, 500), absorption=.97,
                                       size=self.Size.TINY,
                                       core=self.Core.SMALL_IRON_CORE)


class SmallHadean(World):
    def __init__(self):
        super(SmallHadean, self).__init__(temp=(50, 80), absorption=.67,
                                          size=self.Size.SMALL,
                                          core=self.Core.ICY_CORE)


class SmallIce(World):
    def __init__(self):
        """roll of 1d+2 divided by 10"""
        oceans = random.uniform(.3, .8)
        super(SmallIce, self).__init__(temp=(80, 140), absorption=.93,
                                       size=self.Size.SMALL,
                                       core=self.Core.ICY_CORE,
                                       atm=['N2', 'CH4'],
                                       pressure=10,
                                       greenhouse=.1,
                                       oceans=oceans)


class SmallRock(World):
    def __init__(self):
        super(SmallRock, self).__init__(temp=(140, 500), absorption=.96,
                                        size=self.Size.SMALL,
                                        core=self.Core.SMALL_IRON_CORE)


class StandardChthonian(World):
    def __init__(self):
        super(StandardChthonian, self).__init__(temp=(500, 950),
                                                absorption=.97,
                                                size=self.Size.STANDARD,
                                                core=self.Core.LARGE_IRON_CORE)


class StandardGreenhouse(World):
    def __init__(self):
        super(StandardGreenhouse, self).__init__(temp=(500, 950),
                                                 absorption=.77,
                                                 size=self.Size.STANDARD,
                                                 core=self.Core.LARGE_IRON_CORE,
                                                 atm=['CO2'], pressure=100,
                                                 greenhouse=2.0)


class StandardAmmonia(World):
    def __init__(self):
        """roll of 2d maximum at 10 and divided by 10"""
        oceans = min(np.random.triangular(0.2, .7, 1.2), 1)
        super(StandardAmmonia, self).__init__(temp=(140, 215), absorption=.84,
                                              size=self.Size.STANDARD,
                                              core=self.Core.ICY_CORE,
                                              atm=['N2', 'NH3', 'CH4'],
                                              pressure=1, greenhouse=.2,
                                              oceans=oceans)


class StandardHadean(World):
    def __init__(self):
        super(StandardHadean, self).__init__(temp=(50, 80), absorption=.67,
                                             size=self.Size.STANDARD,
                                             core=self.Core.ICY_CORE)


class StandardIce(World):
    def __init__(self):
        """roll of 2d-10 minimum at 0 and divided by 10"""
        oceans = max(np.random.triangular(-.8, -.3, .2), 0)
        super(StandardIce, self).__init__(temp=(80, 230), absorption=.86,
                                          size=self.Size.STANDARD,
                                          core=self.Core.LARGE_IRON_CORE,
                                          atm=['CO2', 'N2'], pressure=1,
                                          greenhouse=.2, oceans=oceans)


class StandardOcean(World):
    def __init__(self):
        """roll of 1d+4 divided by 10"""
        oceans = random.uniform(.5, 1.0)
        """match ocean coverage to Temperature Factors Table"""
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        absorption = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(StandardOcean, self).__init__(temp=(250, 340),
                                            absorption=absorption,
                                            size=self.Size.STANDARD,
                                            core=self.Core.LARGE_IRON_CORE,
                                            atm=['CO2', 'N2'], pressure=1,
                                            greenhouse=.16, oceans=oceans)


class StandardGarden(World):
    def __init__(self):
        """roll of 1d+4 divided by 10"""
        oceans = random.uniform(.5, 1.0)
        """match ocean coverage to Temperature Factors Table"""
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        absorption = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(StandardGarden, self).__init__(temp=(250, 340),
                                             absorption=absorption,
                                             size=self.Size.STANDARD,
                                             core=self.Core.LARGE_IRON_CORE,
                                             atm=['N2', 'O2'], pressure=1,
                                             greenhouse=.16, oceans=oceans)


class LargeChthonian(World):
    def __init__(self):
        super(LargeChthonian, self).__init__(temp=(500, 950), absorption=.97,
                                             size=self.Size.LARGE,
                                             core=self.Core.LARGE_IRON_CORE)


class LargeGreenhouse(World):
    def __init__(self):
        super(LargeGreenhouse, self).__init__(temp=(500, 950), absorption=.77,
                                              size=self.Size.LARGE,
                                              core=self.Core.LARGE_IRON_CORE,
                                              atm=['CO2'], pressure=500,
                                              greenhouse=2.0)


class LargeAmmonia(World):
    def __init__(self):
        """roll of 2d capped at 10 and divided by 10"""
        oceans = min(np.random.triangular(0.2, .7, 1.2), 1)
        super(LargeAmmonia, self).__init__(temp=(140, 215), absorption=.84,
                                           size=self.Size.LARGE,
                                           core=self.Core.ICY_CORE,
                                           atm=['He', 'NH3', 'CH4'],
                                           pressure=5, greenhouse=.2,
                                           oceans=oceans)


class LargeIce(World):
    def __init__(self):
        """roll of 2d-10 minimum at 0 and divided by 10"""
        oceans = max(np.random.triangular(-.8, -.3, .2), 0)
        super(LargeIce, self).__init__(temp=(80, 230), absorption=.86,
                                       size=self.Size.LARGE,
                                       core=self.Core.LARGE_IRON_CORE,
                                       atm=['He', 'N2'], pressure=5,
                                       greenhouse=.2, oceans=oceans)


class LargeOcean(World):
    def __init__(self):
        """roll of 1d+6 maxed at 10 divided by 10"""
        oceans = min(random.uniform(.7, 1.2), 1)
        """match ocean coverage to Temperature Factors Table"""
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        absorption = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(LargeOcean, self).__init__(temp=(250, 340),
                                         absorption=absorption,
                                         core=self.Core.LARGE_IRON_CORE,
                                         size=self.Size.LARGE,
                                         atm=['He', 'N2'], pressure=5,
                                         greenhouse=.16, oceans=oceans)


class LargeGarden(World):
    def __init__(self):
        """roll of 1d+6 maxed at 10 divided by 10"""
        oceans = min(random.uniform(.7, 1.2), 1)
        """match ocean coverage to Temperature Factors Table"""
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        absorption = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(LargeGarden, self).__init__(temp=(250, 340),
                                          absorption=absorption,
                                          size=self.Size.LARGE,
                                          core=self.Core.LARGE_IRON_CORE,
                                          atm=['N2', 'O2', 'He', 'Ne', 'Ar',
                                               'Kr', 'Xe'], pressure=5,
                                          greenhouse=.16, oceans=oceans)


class AsteroidBelt(World):
    def __init__(self):
        super(AsteroidBelt, self).__init__(temp=(140, 500), absorption=.97)
