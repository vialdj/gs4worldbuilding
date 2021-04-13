# -*- coding: utf-8 -*-

from enum import Enum
from collections import namedtuple
from math import sqrt, floor

from scipy.stats import truncnorm
import numpy as np


class World(object):
    # the World Model

    # value range named tuple
    Range = namedtuple('Range', ['min', 'max'])

    class RangeError(Exception):
        # raised to signal an error on Range attributes access or mutations
        pass

    def __set_ranged_property(self, property, value):
        range = getattr(self, '{}_range'.format(property))
        if not range:
            raise RangeError('no value range available for {} on {}'
                             .format(property, self.__class__.__name__))
        if value < range.min or value > range.max:
            raise RangeError('value out of range for {} on {}'
                             .format(property, self.__class__.__name__))
        setattr(self, '_{}'.format(property), value)

    class Size(Range, Enum):
        # class Size Enum from Size Constraints Table
        TINY = (.004, .024)
        SMALL = (.024, .030)
        STANDARD = (.030, .065)
        LARGE = (.065, .091)

    class Core(Range, Enum):
        # class Core Enum from World Density Table
        ICY_CORE = (.3, .7)
        SMALL_IRON_CORE = (.6, 1)
        LARGE_IRON_CORE = (.8, 1.2)

    class Climate(int, Enum):
        # class Climate Enum from World Climate Table
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

    class Atmosphere(float, Enum):
        # class Atmosphere Enum from Atmospheric Pressure Categories Table
        NA = np.nan
        TRACE = .0
        VERY_THIN = .01
        THIN = .51
        STANDARD = .81
        DENSE = 1.21
        VERY_DENSE = 1.51
        SUPER_DENSE = 10

    # class vars
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
        if hasattr(cls, '_core'):
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
    def size(self):
        # size class variable
        return type(self)._size if hasattr(type(self), '_size') else None

    @property
    def core(self):
        # core class variable
        return type(self)._core if hasattr(type(self), '_core') else None

    @property
    def pressure_factor(self):
        # pressure factor class var
        return type(self)._pressure_factor

    @property
    def greenhouse_factor(self):
        # greenhouse_factor class var
        return type(self)._greenhouse_factor

    @property
    def absorption(self):
        # absorption
        return type(self)._absorption

    @property
    def atmosphere(self):
        # key elements in the atmosphere
        return type(self)._atmosphere

    @property
    def volatile_mass(self):
        # relative supply of gaseous elements to other worlds of the same type
        return self._volatile_mass

    @property
    def volatile_mass_range(self):
        # computed value range for volatile mass
        if (self.atmosphere):
            return self.Range(.3, 1.8)
        return None

    @volatile_mass.setter
    def volatile_mass(self, value):
        self.__set_ranged_property('volatile_mass', value)

    @property
    def temperature(self):
        # average temperature in K
        return self._temperature

    @property
    def temperature_range(self):
        # temperature range class variable
        return type(self)._temperature_range

    @temperature.setter
    def temperature(self, value):
        self.__set_ranged_property('temperature', value)

    @property
    def density(self):
        # density in d⊕
        return self._density

    @property
    def density_range(self):
        # computed value range for density
        return type(self)._core.value if hasattr(type(self), '_core') else None

    @density.setter
    def density(self, value):
        self.__set_ranged_property('density', value)

    @property
    def hydrosphere(self):
        # proportion of surface covered by liquid elements
        return self._hydrosphere

    @property
    def hydrosphere_range(self):
        # hydrosphere range class variable
        return (type(self)._hydrosphere_range
                if hasattr(type(self), '_hydrosphere_range') else None)

    @hydrosphere.setter
    def hydrosphere(self, value):
        self.__set_ranged_property('hydrosphere', value)

    @property
    def diameter(self):
        # diameter in D⊕
        return self._diameter

    @property
    def diameter_range(self):
        # computed value range for diameter
        if (not np.isnan(self.density) and self.size):
            return self.Range(sqrt(self.blackbody_temperature / self.density) *
                              self.size.min,
                              sqrt(self.blackbody_temperature / self.density) *
                              self.size.max)
        return None

    @diameter.setter
    def diameter(self, value):
        self.__set_ranged_property('diameter', value)

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

    def __iter__(self):
        attributes = dir(self)
        for attr in attributes:
            if (hasattr(type(self), attr) and isinstance(getattr(type(self),
                                                                 attr),
                                                         property)):
                yield attr, getattr(self, attr)

    def __str__(self):
        return ('{}'.format(', '.join(['{} = {!s}'.format(attr, value)
                                       for attr, value in self])))
