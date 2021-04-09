# -*- coding: utf-8 -*-

from enum import Enum
from collections import namedtuple
from math import sqrt, floor
from scipy.stats import truncnorm
import numpy as np


class World(object):
    # the World Model

    Range = namedtuple('Range', ['min', 'max'])

    # class Size Enum from Size Constraints Table
    class Size(Range, Enum):
        NA = (np.nan, np.nan)
        TINY = (.004, .024)
        SMALL = (.024, .030)
        STANDARD = (.030, .065)
        LARGE = (.065, .091)

    # class Core Enum from World Density Table
    class Core(Range, Enum):
        NA = (np.nan, np.nan)
        ICY_CORE = (.3, .7)
        SMALL_IRON_CORE = (.6, 1)
        LARGE_IRON_CORE = (.8, 1.2)

    # class Climate Enum from World Climate Table
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

    # class Atmosphere Enum from Atmospheric Pressure Categories Table
    class Atmosphere(float, Enum):
        NA = np.nan
        TRACE = .0
        VERY_THIN = .01
        THIN = .51
        STANDARD = .81
        DENSE = 1.21
        VERY_DENSE = 1.51
        SUPER_DENSE = 10

    # class vars
    _size = Size.NA
    _core = Core.NA
    _pressure_factor = 0
    _greenhouse_factor = np.nan
    _atmosphere = []

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
        if cls._core != cls.Core.NA:
            return (cls._core.min + (cls._core.max - cls._core.min) *
                    truncnorm((0 - 0.376) / 0.2, (1 - 0.376) / 0.2,
                    loc=0.376, scale=0.2).rvs())
        return np.nan

    def random_diameter(self):
        # roll of 2d-2 in range [Dmin, Dmax]
        if self.diameter_range:
            return (self.diameter_range.min + np.random.triangular(0, .5, 1) *
                    (self.diameter_range.max - self.diameter_range.min))
        return np.nan

    def random_volatile_mass(self):
        # sum of a 3d roll divided by 10
        if self.atmosphere:
            return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                             loc=10.5, scale=2.958040).rvs() / 10
        return np.nan

    @classmethod
    def random_hydrosphere(cls):
        return np.nan

    @property
    def temperature_range(self):
        # temperature range class var
        return type(self)._temperature_range

    @property
    def size(self):
        # size class var
        return type(self)._size

    @property
    def core(self):
        # core class var
        return type(self)._core

    @property
    def pressure_factor(self):
        # pressure factor class var
        return type(self)._pressure_factor

    @property
    def greenhouse_factor(self):
        # greenhouse_factor class var
        return type(self)._greenhouse_factor

    @property
    def hydrosphere_range(self):
        # hydrosphere range class var
        return type(self)._hydrosphere_range

    @property
    def absorption(self):
        # absorption
        return type(self)._absorption

    @property
    def atmosphere(self):
        # key elements in the atmosphere
        return type(self)._atmosphere

    @property
    def volatile_mass_range(self):
        if (self.atmosphere):
            return self.Range(.3, 1.8)
        return None

    @property
    def volatile_mass(self):
        # relative supply of gaseous elements to other worlds of the same type
        return self._volatile_mass

    @volatile_mass.setter
    def volatile_mass(self, value):
        assert(self.volatile_mass_range), "attribute is not applicable"
        assert (value >= self.volatile_mass_range.min and
                value <= self.volatile_mass_range.max), "value out of bounds"
        self._temperature = value

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
        assert self.core != Core.NA, "attribute is not applicable"
        assert (value >= type(self)._core.min and
                value <= type(self)._core.max), "value out of bounds"
        self._density = value

    @property
    def hydrosphere(self):
        # proportion of surface covered by liquid elements
        return self._hydrosphere

    @hydrosphere.setter
    def hydrosphere(self, value):
        assert(self.hydrosphere_range), "attribute is not applicable"
        assert (value >= self.hydrosphere_range.min and
                value <= self.hydrosphere_range.max), "value out of bounds"
        self._hydrosphere = value

    @property
    def diameter_range(self):
        if (~np.isnan(self.density) and self.size != self.Size.NA):
            return self.Range(sqrt(self.blackbody_temperature / self.density) *
                              self.size.value.min,
                              sqrt(self.blackbody_temperature / self.density) *
                              self.size.value.max)
        return None

    @property
    def diameter(self):
        # diameter in D⊕
        return self._diameter

    @diameter.setter
    def diameter(self, value):
        assert(self.diameter_range), "attribute is not applicable"
        assert (value >= self.diameter_range.min and
                value <= self.diameter_range.max), "value out of bounds"
        self._diameter = value

    @property
    def blackbody_temperature(self):
        # blackbody temperature in K
        return (self.temperature / self.absorption
                if np.isnan([self.volatile_mass, self.greenhouse_factor]).any()
                else self.temperature / (self.absorption *
                                         floor(1 + self.volatile_mass
                                               * self.greenhouse_factor)))

    @property
    def gravity(self):
        # surface gravity in G⊕
        return self.density * self.diameter

    @property
    def mass(self):
        # mass in M⊕
        return self.density * self.diameter**3

    @property
    def climate(self):
        # climate implied by temperature match over World Climate Table
        return list(filter(lambda x: self.temperature >= x.value,
                           self.Climate))[-1]

    @property
    def pressure(self):
        # atmospheric pressure in atm⊕
        return self.volatile_mass * self.pressure_factor * self.gravity

    @property
    def pressure_category(self):
        # atmospheric pressure implied by pressure match over
        # Atmospheric Pressure Categories Table
        return list(filter(lambda x: self.pressure >= x.value or
                           np.isnan([self.pressure, x.value]).all(),
                           self.Atmosphere))[-1]

    def __init__(self):
        # randomize applicable values
        self.temperature = type(self).random_temperature()
        self._density = type(self).random_density()
        self._hydrosphere = self.random_hydrosphere()
        self._volatile_mass = self.random_volatile_mass()
        self._diameter = self.random_diameter()

    def __str__(self):
        return '{self.__class__.__name__} (hydrosphere={self.hydrosphere:.2f}, \
atmosphere={self.atmosphere}, \
pressure={self.pressure:.2f}({self.pressure_category.name}) atm⊕, \
average surface temperature={self.temperature:.2f}({self.climate.name}) K, \
size={self.size.name}, \
blackbody temperature={self.blackbody_temperature:.2f} K, \
density={self.density:.2f} d⊕, \
core={self.core.name}, \
diameter={self.diameter:.2f} D⊕, \
gravity={self.gravity:.2f} G⊕, \
mass={self.mass:.2f} M⊕)'.format(self=self)