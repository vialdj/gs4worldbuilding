# -*- coding: utf-8 -*-

import random
from enum import Enum
from collections import namedtuple
from math import sqrt, floor
from scipy.stats import truncnorm
import numpy as np


class World(object):
    # the World Model

    Range = namedtuple('Range', ['min', 'max'])

    # Size Enum from Size Constraints Table
    class Size(str, Enum):
        TINY = 'Tiny'
        SMALL = 'Small'
        STANDARD = 'Standard'
        LARGE = 'Large'

    # Core Enum from World Density Table
    class Core(str, Enum):
        ICY_CORE = 'Icy core'
        SMALL_IRON_CORE = 'Small iron core'
        LARGE_IRON_CORE = 'Large iron core'

    # internal Climate Enum from World Climate Table
    class Climate(str, Enum):
        FROZEN = 'Frozen'
        VERY_COLD = 'Very cold'
        COLD = 'Cold'
        CHILLY = 'Chilly'
        COOL = 'Cool'
        NORMAL = 'Normal'
        WARM = 'Warm'
        TROPICAL = 'Tropical'
        HOT = 'Hot'
        VERY_HOT = 'Very hot'
        INFERNAL = 'Infernal'

    # internal Atmosphere Enum from Atmospheric Pressure Categories Table
    class Atmosphere(str, Enum):
        TRACE = 'Trace'
        VERY_THIN = 'Very thin'
        THIN = 'Thin'
        STANDARD = 'Standard'
        DENSE = 'Dense'
        VERY_DENSE = 'Very dense'
        SUPER_DENSE = 'Super dense'

    # temperature range static member
    _temperature_range = None
    # size static member
    _size = None
    # core static member
    _core = None

    @classmethod
    def random_temperature(cls):
        # sum of a 3d-3 roll times step value add minimum
        tmin = cls._temperature_range.min
        tmax = cls._temperature_range.max
        roll = truncnorm((0 - 7.5) / 2.958040, (15 - 7.5) / 2.958040,
                         loc=7.5, scale=2.958040).rvs()
        return tmin + roll / 15 * (tmax - tmin)

    # internal Atmosphere class
    # class Atmosphere(NamedTuple):
    #     composition: list = None
    #     pressure_factor: float = .0
    #     relative_mass: float = .0
    #     pressure: float = .0
    #     category: str = ''

    def __init__(self, absorption, core=None, atm=[], pressure=.0,
                 greenhouse=.0, oceans=.0):
        # the ocean coverage proportion
        self.oceans = oceans
        # key elements in the atmosphere
        self.atm = atm
        # relative supply of gaseous elements to other worlds of the same type
        atm_mass = self.__atm_mass(atm)
        self.atm_mass = atm_mass
        self.temperature = type(self).random_temperature()
        # blackbody temperature in K
        bb_temp = self.__blackbody_temperature(absorption, greenhouse,
                                               atm_mass, self.temperature)
        self.bb_temp = bb_temp
        # density in d⊕
        density = self.__density(self.core)
        self.density = density
        # diameter in D⊕
        diameter = self.__diameter(self.size, bb_temp, density)
        self.diameter = diameter
        # surface gravity in G⊕
        gravity = density * diameter
        self.gravity = gravity
        # mass in M⊕
        self.mass = density * diameter**3
        # atmospheric pressure in atm⊕
        atm_pressure = atm_mass * pressure * gravity
        self.atm_pressure = atm_pressure
        # atmosphere category
        self.atm_p_category = self.__atm_category(atm_pressure)

    @property
    def temperature_range(self):
        # world type temperature range static member
        return type(self)._temperature_range

    @property
    def size(self):
        # world type size static value
        return type(self)._size

    @property
    def core(self):
        # world type core static value
        return type(self)._core

    @property
    def temperature(self):
        # average temperature in K
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        assert (value >= self.temperature_range.min and
                value <= self.temperature_range.max), "value out of bounds"
        self._temperature = value
        self.__climate_f()

    @property
    def climate(self):
        # climate implied by temperature match over World Climate Table
        return self._climate

    def __climate_f(self):
        d = {244: self.Climate.FROZEN,
             255: self.Climate.VERY_COLD,
             266: self.Climate.COLD,
             278: self.Climate.CHILLY,
             289: self.Climate.COOL,
             300: self.Climate.NORMAL,
             311: self.Climate.WARM,
             322: self.Climate.TROPICAL,
             333: self.Climate.HOT,
             344: self.Climate.VERY_HOT}
        k = list(filter(lambda x: x >= self.temperature, sorted(d.keys())))
        self._climate = d[k[0]] if len(k) > 0 else self.Climate.INFERNAL

    # blackbody temperature B = T / C where C = A * [1 + (M * G)]
    # with A the absorption factor, M the relative atmospheric mass and G the
    # greenhouse factor (A and G given in the Temperature Factors Table)
    def __blackbody_temperature(self, absorption, greenhouse, atm, temperature):
        return temperature / (absorption * floor(1 + atm * greenhouse))

    # roll of 2d-2 in range [Dmin, Dmax]
    def __diameter(self, size, bb_temp, density):
        if size is not None:
            d = {self.Size.TINY: (0.004, 0.024),
                 self.Size.SMALL: (0.024, 0.030),
                 self.Size.STANDARD: (0.030, 0.065),
                 self.Size.LARGE: (0.065, 0.091)}
            dmin = sqrt(bb_temp / density) * d[size][0]
            dmax = sqrt(bb_temp / density) * d[size][1]
            return dmin + np.random.triangular(0, .5, 1) * (dmax - dmin)
        return .0

    # sum of a 3d roll over World Density Table
    def __density(self, core):
        if core is not None:
            densities = {self.Core.ICY_CORE: [0.3, 0.4, 0.5, 0.6, 0.7],
                         self.Core.SMALL_IRON_CORE: [0.6, 0.7, 0.8, 0.9, 1.0],
                         self.Core.LARGE_IRON_CORE: [0.8, 0.9, 1.0, 1.1, 1.2]}
            return np.random.choice(densities[core], p=[0.0926, 0.4074, 0.4074,
                                                        0.08797, 0.00463])
        return .0

    # sum of a 3d roll divided by 10
    def __atm_mass(self, atm):
        if len(atm) > 0:
            return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                             loc=10.5, scale=2.958040).rvs() / 10
        return .0



    # match atmospheric pressure to Atmospheric Pressure Categories Table
    def __atm_category(self, pressure):
        d = {.01: self.Atmosphere.TRACE,
             .51: self.Atmosphere.VERY_THIN,
             .81: self.Atmosphere.THIN,
             1.21: self.Atmosphere.STANDARD,
             1.51: self.Atmosphere.DENSE,
             10: self.Atmosphere.VERY_DENSE}
        k = list(filter(lambda x: x >= pressure, sorted(d.keys())))
        return d[k[0]] if len(k) > 0 else self.Atmosphere.SUPER_DENSE

    def __str__(self):
        return '{self.__class__.__name__} (ocean coverage= {self.oceans:.2f}, \
atmosphere composition= {self.atm}, \
atmosphere pressure= {self.atm_pressure:.2f} atm⊕ ({self.atm_p_category}), \
average surface temperature= {self.temperature:.2f} K, \
climate = {self.climate}, \
size= {self.size}, \
blackbody temperature= {self.bb_temp:.2f} K, \
density= {self.density:.2f} d⊕, \
core= {self.core}, \
diameter= {self.diameter:.2f} D⊕, \
gravity= {self.gravity:.2f} G⊕, \
mass= {self.mass:.2f} M⊕)'.format(self=self)


class TinySulfur(World):
    _temperature_range = World.Range(80, 140)
    _size = World.Size.TINY
    _core = World.Core.ICY_CORE

    def __init__(self):
        super(TinySulfur, self).__init__(absorption=.77)


class TinyIce(World):
    _temperature_range = World.Range(80, 140)
    _size = World.Size.TINY
    _core = World.Core.ICY_CORE

    def __init__(self):
        super(TinyIce, self).__init__(absorption=.86)


class TinyRock(World):
    _temperature_range = World.Range(140, 500)
    _size = World.Size.TINY
    _core = World.Core.SMALL_IRON_CORE

    def __init__(self):
        super(TinyRock, self).__init__(absorption=.97)


class SmallHadean(World):
    _temperature_range = World.Range(50, 80)
    _size = World.Size.SMALL
    _core = World.Core.ICY_CORE

    def __init__(self):
        super(SmallHadean, self).__init__(absorption=.67)


class SmallIce(World):
    _temperature_range = World.Range(80, 140)
    _size = World.Size.SMALL
    _core = World.Core.ICY_CORE

    def __init__(self):
        # roll of 1d+2 divided by 10
        oceans = random.uniform(.3, .8)
        super(SmallIce, self).__init__(absorption=.93, atm=['N2', 'CH4'],
                                       pressure=10, greenhouse=.1, oceans=oceans)


class SmallRock(World):
    _temperature_range = World.Range(140, 500)
    _size = World.Size.SMALL
    _core = World.Core.SMALL_IRON_CORE

    def __init__(self):
        super(SmallRock, self).__init__(absorption=.96)


class StandardChthonian(World):
    _temperature_range = World.Range(500, 950)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        super(StandardChthonian, self).__init__(absorption=.97)


class StandardGreenhouse(World):
    _temperature_range = World.Range(500, 950)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        super(StandardGreenhouse, self).__init__(absorption=.77, atm=['CO2'],
                                                 pressure=100,
                                                 greenhouse=2.0)


class StandardAmmonia(World):
    _temperature_range = World.Range(140, 215)
    _size = World.Size.STANDARD
    _core = World.Core.ICY_CORE

    def __init__(self):
        # roll of 2d maximum at 10 and divided by 10
        oceans = min(np.random.triangular(0.2, .7, 1.2), 1)
        super(StandardAmmonia, self).__init__(absorption=.84,
                                              atm=['N2', 'NH3', 'CH4'],
                                              pressure=1, greenhouse=.2,
                                              oceans=oceans)


class StandardHadean(World):
    _temperature_range = World.Range(50, 80)
    _size = World.Size.STANDARD
    _core = World.Core.ICY_CORE

    def __init__(self):
        super(StandardHadean, self).__init__(absorption=.67)


class StandardIce(World):
    _temperature_range = World.Range(80, 230)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        # roll of 2d-10 minimum at 0 and divided by 10
        oceans = max(np.random.triangular(-.8, -.3, .2), 0)
        super(StandardIce, self).__init__(absorption=.86,
                                          atm=['CO2', 'N2'], pressure=1,
                                          greenhouse=.2, oceans=oceans)


class StandardOcean(World):
    _temperature_range = World.Range(250, 340)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        # roll of 1d+4 divided by 10
        oceans = random.uniform(.5, 1.0)
        # match ocean coverage to Temperature Factors Table
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        a = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(StandardOcean, self).__init__(absorption=a, atm=['CO2', 'N2'], pressure=1,
                                            greenhouse=.16, oceans=oceans)


class StandardGarden(World):
    _temperature_range = World.Range(250, 340)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        # roll of 1d+4 divided by 10
        oceans = random.uniform(.5, 1.0)
        # match ocean coverage to Temperature Factors Table
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        a = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(StandardGarden, self).__init__(absorption=a, atm=['N2', 'O2'],
                                             pressure=1, greenhouse=.16, oceans=oceans)


class LargeChthonian(World):
    _temperature_range = World.Range(500, 950)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        super(LargeChthonian, self).__init__(absorption=.97)


class LargeGreenhouse(World):
    _temperature_range = World.Range(500, 950)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        super(LargeGreenhouse, self).__init__(absorption=.77,
                                              atm=['CO2'], pressure=500,
                                              greenhouse=2.0)


class LargeAmmonia(World):
    _temperature_range = World.Range(140, 215)
    _size = World.Size.LARGE
    _core = World.Core.ICY_CORE

    def __init__(self):
        # roll of 2d capped at 10 and divided by 10
        oceans = min(np.random.triangular(0.2, .7, 1.2), 1)
        super(LargeAmmonia, self).__init__(absorption=.84,
                                           atm=['He', 'NH3', 'CH4'],
                                           pressure=5, greenhouse=.2,
                                           oceans=oceans)


class LargeIce(World):
    _temperature_range = World.Range(80, 230)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        # roll of 2d-10 minimum at 0 and divided by 10
        oceans = max(np.random.triangular(-.8, -.3, .2), 0)
        super(LargeIce, self).__init__(absorption=.86,
                                       atm=['He', 'N2'], pressure=5,
                                       greenhouse=.2, oceans=oceans)


class LargeOcean(World):
    _temperature_range = World.Range(250, 340)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        # roll of 1d+6 maxed at 10 divided by 10
        oceans = min(random.uniform(.7, 1.2), 1)
        # match ocean coverage to Temperature Factors Table
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        a = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(LargeOcean, self).__init__(absorption=a,
                                         atm=['He', 'N2'], pressure=5,
                                         greenhouse=.16, oceans=oceans)


class LargeGarden(World):
    _temperature_range: World.Range(250, 340)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE

    def __init__(self):
        # roll of 1d+6 maxed at 10 divided by 10
        oceans = min(random.uniform(.7, 1.2), 1)
        # match ocean coverage to Temperature Factors Table
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        a = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(LargeGarden, self).__init__(absorption=a,
                                          atm=['N2', 'O2', 'He', 'Ne', 'Ar',
                                               'Kr', 'Xe'], pressure=5,
                                          greenhouse=.16, oceans=oceans)


class AsteroidBelt(World):
    _temperature_range: World.Range(140, 500)

    def __init__(self):
        super(AsteroidBelt, self).__init__(absorption=.97)
