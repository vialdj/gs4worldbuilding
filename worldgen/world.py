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
    class Size(Range, Enum):
        TINY = (.004, .024)
        SMALL = (.024, .030)
        STANDARD = (.030, .065)
        LARGE = (.065, .091)

    # Core Enum from World Density Table
    class Core(Range, Enum):
        ICY_CORE = (.3, .7)
        SMALL_IRON_CORE = (.6, 1.0)
        LARGE_IRON_CORE = (.8, 1.2)

    # Climate Enum from World Climate Table
    class Climate(int, Enum):
        FROZEN = 0
        VERY_COLD = 244
        COLD = 255
        CHILLY = 266
        COOL = 278
        NORMAL = 289
        WARM = 300
        TROPICAL = 311
        HOT = 322
        VERY_HOT = 333
        INFERNAL = 344

    # internal Atmosphere Enum from Atmospheric Pressure Categories Table
    class Atmosphere(float, Enum):
        TRACE = .0
        VERY_THIN = .01
        THIN = .51
        STANDARD = .81
        DENSE = 1.21
        VERY_DENSE = 1.51
        SUPER_DENSE = 10

    _temperature_range = None
    _size = None
    _core = None
    _pressure_factor = 0
    _greenhouse = .0

    @classmethod
    def random_temperature(cls):
        # sum of a 3d-3 roll times step value add minimum
        tmin = cls._temperature_range.min
        tmax = cls._temperature_range.max
        roll = truncnorm((0 - 7.5) / 2.958040, (15 - 7.5) / 2.958040,
                         loc=7.5, scale=2.958040).rvs()
        return tmin + roll / 15 * (tmax - tmin)

    @classmethod
    def random_density(cls):
        # sum of a 3d roll over World Density Table
        return (cls._core.min + (cls._core.max - cls._core.min) *
                truncnorm((0 - 0.376) / 0.2, (1 - 0.376) / 0.2,
                loc=0.376, scale=0.2).rvs())

    def random_diameter(self):
        # roll of 2d-2 in range [Dmin, Dmax]
        return (self.diameter_range.min + np.random.triangular(0, .5, 1) *
                (self.diameter_range.max - self.diameter_range.min))

    def __init__(self, absorption, atm=[], oceans=.0):
        # the ocean coverage proportion
        self.oceans = oceans
        # key elements in the atmosphere
        self.atm = atm
        # relative supply of gaseous elements to other worlds of the same type
        atm_mass = self.__atm_mass(atm)
        self.atm_mass = atm_mass
        self.temperature = type(self).random_temperature()
        # blackbody temperature in K
        bb_temp = self.__blackbody_temperature(absorption, self.greenhouse,
                                               atm_mass, self.temperature)
        self.bb_temp = bb_temp
        self.density = type(self).random_density()
        self.diameter = self.random_diameter()
        # surface gravity in G⊕
        gravity = self.density * self.diameter
        self.gravity = gravity
        # mass in M⊕
        self.mass = self.density * self.diameter**3
        # atmospheric pressure in atm⊕
        pressure = atm_mass * self.pressure_factor * gravity
        self.pressure = pressure

    @property
    def temperature_range(self):
        # world type temperature range class value
        return type(self)._temperature_range

    @property
    def size(self):
        # world type size class value
        return type(self)._size

    @property
    def core(self):
        # world type core class value
        return type(self)._core

    @property
    def pressure_factor(self):
        # world type pressure factor class value
        return type(self)._pressure_factor

    @property
    def greenhouse(self):
        # world type greenhouse class value
        return type(self)._greenhouse

    @property
    def temperature(self):
        # average temperature in K
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        assert (value >= self.temperature_range.min and
                value <= self.temperature_range.max), "value out of bounds"
        self._temperature = value

    @property
    def density(self):
        # density in d⊕
        return self._density

    @density.setter
    def density(self, value):
        assert self.core, "parent attribute is not available"
        assert (value >= type(self)._core.min and
                value <= type(self)._core.max), "value out of bounds"
        self._density = value

    @property
    def diameter_range(self):
        # diameter range in D⊕
        assert self.density and self.bb_temp and self.size, "parent attribute is not available"
        return self.Range(sqrt(self.bb_temp / self.density) * self.size.value.min,
                          sqrt(self.bb_temp / self.density) * self.size.value.max)

    @property
    def diameter(self):
        # diameter in D⊕
        return self._diameter
    
    @diameter.setter
    def diameter(self, value):
        assert (value >= self.diameter_range.min and
                value <= self.diameter_range.max), "value out of bounds"
        self._diameter = value

    @property
    def climate(self):
        # climate implied by temperature match over World Climate Table
        return list(filter(lambda x: self.temperature >= x.value, self.Climate))[-1]

    @property
    def pressure_category(self):
        # atmospheric pressure implied by pressure match over Atmospheric Pressure Categories Table
        return list(filter(lambda x: self.pressure >= x.value, self.Atmosphere))[-1]

    # blackbody temperature B = T / C where C = A * [1 + (M * G)]
    # with A the absorption factor, M the relative atmospheric mass and G the
    # greenhouse factor (A and G given in the Temperature Factors Table)
    def __blackbody_temperature(self, absorption, greenhouse, atm, temperature):
        return temperature / (absorption * floor(1 + atm * greenhouse))

    # sum of a 3d roll divided by 10
    def __atm_mass(self, atm):
        if len(atm) > 0:
            return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                             loc=10.5, scale=2.958040).rvs() / 10
        return .0

    def __str__(self):
        return '{self.__class__.__name__} (ocean coverage= {self.oceans:.2f}, \
atmosphere composition= {self.atm}, \
atmosphere pressure= {self.pressure:.2f} atm⊕ ({self.pressure_category.name}), \
average surface temperature= {self.temperature:.2f} K, \
climate = {self.climate.name}, \
size= {self.size.name}, \
blackbody temperature= {self.bb_temp:.2f} K, \
density= {self.density:.2f} d⊕, \
core= {self.core.name}, \
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
    _pressure_factor = 10
    _greenhouse = .1

    def __init__(self):
        # roll of 1d+2 divided by 10
        oceans = random.uniform(.3, .8)
        super(SmallIce, self).__init__(absorption=.93, atm=['N2', 'CH4'],
                                       oceans=oceans)


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
    _pressure_factor = 100
    _greenhouse = 2.0

    def __init__(self):
        super(StandardGreenhouse, self).__init__(absorption=.77, atm=['CO2'])


class StandardAmmonia(World):
    _temperature_range = World.Range(140, 215)
    _size = World.Size.STANDARD
    _core = World.Core.ICY_CORE
    _pressure_factor = 1
    _greenhouse = .2

    def __init__(self):
        # roll of 2d maximum at 10 and divided by 10
        oceans = min(np.random.triangular(0.2, .7, 1.2), 1)
        super(StandardAmmonia, self).__init__(absorption=.84,
                                              atm=['N2', 'NH3', 'CH4'],
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
    _pressure_factor = 1
    _greenhouse = .2

    def __init__(self):
        # roll of 2d-10 minimum at 0 and divided by 10
        oceans = max(np.random.triangular(-.8, -.3, .2), 0)
        super(StandardIce, self).__init__(absorption=.86,
                                          atm=['CO2', 'N2'],
                                          oceans=oceans)


class StandardOcean(World):
    _temperature_range = World.Range(250, 340)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse = .16

    def __init__(self):
        # roll of 1d+4 divided by 10
        oceans = random.uniform(.5, 1.0)
        # match ocean coverage to Temperature Factors Table
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        a = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(StandardOcean, self).__init__(absorption=a, atm=['CO2', 'N2'],
                                            oceans=oceans)


class StandardGarden(World):
    _temperature_range = World.Range(250, 340)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse = .16

    def __init__(self):
        # roll of 1d+4 divided by 10
        oceans = random.uniform(.5, 1.0)
        # match ocean coverage to Temperature Factors Table
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        a = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(StandardGarden, self).__init__(absorption=a, atm=['N2', 'O2'],
                                             oceans=oceans)


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
    _pressure_factor = 500
    _greenhouse = 2.0

    def __init__(self):
        super(LargeGreenhouse, self).__init__(absorption=.77, atm=['CO2'])


class LargeAmmonia(World):
    _temperature_range = World.Range(140, 215)
    _size = World.Size.LARGE
    _core = World.Core.ICY_CORE
    _pressure_factor = 5
    _greenhouse = .2

    def __init__(self):
        # roll of 2d capped at 10 and divided by 10
        oceans = min(np.random.triangular(0.2, .7, 1.2), 1)
        super(LargeAmmonia, self).__init__(absorption=.84,
                                           atm=['He', 'NH3', 'CH4'], oceans=oceans)


class LargeIce(World):
    _temperature_range = World.Range(80, 230)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse = .2

    def __init__(self):
        # roll of 2d-10 minimum at 0 and divided by 10
        oceans = max(np.random.triangular(-.8, -.3, .2), 0)
        super(LargeIce, self).__init__(absorption=.86,
                                       atm=['He', 'N2'], oceans=oceans)


class LargeOcean(World):
    _temperature_range = World.Range(250, 340)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse = .16

    def __init__(self):
        # roll of 1d+6 maxed at 10 divided by 10
        oceans = min(random.uniform(.7, 1.2), 1)
        # match ocean coverage to Temperature Factors Table
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        a = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(LargeOcean, self).__init__(absorption=a,
                                         atm=['He', 'N2'], oceans=oceans)


class LargeGarden(World):
    _temperature_range = World.Range(250, 340)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse = .16

    def __init__(self):
        # roll of 1d+6 maxed at 10 divided by 10
        oceans = min(random.uniform(.7, 1.2), 1)
        # match ocean coverage to Temperature Factors Table
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        a = d[list(filter(lambda x: x >= oceans, sorted(d.keys())))[0]]
        super(LargeGarden, self).__init__(absorption=a,
                                          atm=['N2', 'O2', 'He', 'Ne', 'Ar',
                                               'Kr', 'Xe'], oceans=oceans)


class AsteroidBelt(World):
    _temperature_range = World.Range(140, 500)

    def __init__(self):
        super(AsteroidBelt, self).__init__(absorption=.97)
