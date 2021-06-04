# -*- coding: utf-8 -*-

from .utils import Range
from . import Atmosphere

import random

from enum import Enum
from math import sqrt, floor
from inspect import ismethod
from dataclasses import dataclass

from scipy.stats import truncnorm
import numpy as np


class World(object):
    """the World Model"""

    class Climate(int, Enum):
        """class Climate Enum from World Climate Table"""
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

    class Size(Range, Enum):
        """class Size Enum from Size Constraints Table"""
        TINY = (.004, .024)
        SMALL = (.024, .030)
        STANDARD = (.030, .065)
        LARGE = (.065, .091)

    class Core(Range, Enum):
        """class Core Enum from World Density Table"""
        ICY_CORE = (.3, .7)
        SMALL_IRON_CORE = (.6, 1)
        LARGE_IRON_CORE = (.8, 1.2)

    class Ressource(int, Enum):
        """class Ressource Enum from Ressource Value Table"""
        WORTHLESS = -5
        VERY_SCANT = -4
        SCANT = -3
        VERY_POOR = -2
        POOR = -1
        AVERAGE = 0
        ABUNDANT = 1
        VERY_ABUNDANT = 2
        RICH = 3
        VERY_RICH = 4
        MOTHERLODE = 5

    def __set_ranged_property(self, prop, value):
        """centralised setter for ranged value properties"""
        rng = getattr(self, '{}_range'.format(prop))
        if not rng:
            raise AttributeError('can\'t set attribute, no {}_range found'
                                 .format(prop))
        if np.isnan(value):
            raise ValueError('can\'t manually set {} value to nan'.format(prop))
        if value < rng.min or value > rng.max:
            raise ValueError('{} value out of range {}'
                             .format(prop, rng))
        setattr(self, '_{}'.format(prop), value)

    @classmethod
    def random_ressource(cls):
        """sum of a 3d roll times over default worlds Ressource Value Table"""
        ressource_distribution = [0, 0, 0, .01852, .14352, .67592,
                                  .14352, .01852, 0, 0, 0]
        return random.choices(list(cls.Ressource),
                              weights=ressource_distribution, k=1)[0]

    def random_temperature(self):
        """sum of a 3d-3 roll times step value add minimum"""
        tmin = self.temperature_range.min
        tmax = self.temperature_range.max
        roll = truncnorm((0 - 7.5) / 2.958040, (15 - 7.5) / 2.958040,
                         loc=7.5, scale=2.958040).rvs()
        return tmin + roll / 15 * (tmax - tmin)

    def random_density(self):
        """sum of a 3d roll over World Density Table"""
        return (self.density_range.min + (self.density_range.max -
                                          self.density_range.min) *
                truncnorm((0 - 0.376) / 0.2, (1 - 0.376) / 0.2,
                loc=0.376, scale=0.2).rvs())

    def random_diameter(self):
        """roll of 2d-2 in range [Dmin, Dmax]"""
        return (self.diameter_range.min + np.random.triangular(0, .5, 1) *
                (self.diameter_range.max - self.diameter_range.min))

    def random_volatile_mass(self):
        """sum of a 3d roll divided by 10"""
        return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                         loc=10.5, scale=2.958040).rvs() / 10

    @property
    def size(self):
        """size class variable"""
        return type(self)._size if hasattr(type(self), '_size') else None

    @property
    def core(self):
        """core class variable"""
        return type(self)._core if hasattr(type(self), '_core') else None

    @property
    def pressure_factor(self):
        """pressure factor class variable"""
        return (type(self)._pressure_factor
                if hasattr(type(self), '_pressure_factor') else np.nan)

    @property
    def greenhouse_factor(self):
        """greenhouse_factor class variable"""
        return (type(self)._greenhouse_factor
                if hasattr(type(self), '_greenhouse_factor') else np.nan)

    @property
    def absorption(self):
        """absorption"""
        return type(self)._absorption

    @property
    def atmosphere(self):
        """key properties of the atmosphere"""
        return (self._atmosphere
                if hasattr(self, '_atmosphere') else None)

    @property
    def volatile_mass(self):
        """relative supply of gaseous elements to other worlds of the same type"""
        return self._volatile_mass if hasattr(self, '_volatile_mass') else np.nan

    @property
    def volatile_mass_range(self):
        """computed value range for volatile mass"""
        return Range(.3, 1.8) if self.atmosphere else None

    @volatile_mass.setter
    def volatile_mass(self, value):
        self.__set_ranged_property('volatile_mass', value)

    @property
    def ressource(self):
        """resource value on Resource Value Table"""
        return self._ressource

    @property
    def ressource_range(self):
        """ressource range class variable"""
        return type(self)._ressource_range if hasattr(type(self), '_ressource_range') else Range(self.Ressource.VERY_POOR, self.Ressource.VERY_ABUNDANT)

    @ressource.setter
    def ressource(self, value):
        self.__set_ranged_property('ressource', value)

    @property
    def temperature(self):
        """average temperature in K"""
        return self._temperature

    @property
    def temperature_range(self):
        """temperature range class variable"""
        return type(self)._temperature_range

    @temperature.setter
    def temperature(self, value):
        self.__set_ranged_property('temperature', value)

    @property
    def density(self):
        """density in d⊕"""
        return self._density if hasattr(self, '_density') else np.nan

    @property
    def density_range(self):
        """value range for density"""
        return type(self)._core.value if hasattr(type(self), '_core') else None

    @density.setter
    def density(self, value):
        self.__set_ranged_property('density', value)

    @property
    def hydrosphere(self):
        """proportion of surface covered by liquid elements"""
        return self._hydrosphere if hasattr(self, '_hydrosphere') else np.nan

    @property
    def hydrosphere_range(self):
        """hydrosphere value range class variable"""
        return (type(self)._hydrosphere_range
                if hasattr(type(self), '_hydrosphere_range') else None)

    @hydrosphere.setter
    def hydrosphere(self, value):
        self.__set_ranged_property('hydrosphere', value)

    @property
    def diameter(self):
        """diameter in D⊕"""
        return self._diameter if hasattr(self, '_diameter') else np.nan

    @property
    def diameter_range(self):
        """computed value range for diameter"""
        return (Range(sqrt(self.blackbody_temperature / self.density) * self.size.min,
                      sqrt(self.blackbody_temperature / self.density) * self.size.max)
                if self.density and self.size else None)

    @diameter.setter
    def diameter(self, value):
        self.__set_ranged_property('diameter', value)

    @property
    def blackbody_temperature(self):
        """blackbody temperature in K"""
        return (self.temperature / self.absorption
                if np.isnan([self.volatile_mass, self.greenhouse_factor]).any()
                else self.temperature / (self.absorption *
                                         floor(1 + self.volatile_mass
                                               * self.greenhouse_factor)))

    @property
    def gravity(self):
        """surface gravity in G⊕"""
        return self.density * self.diameter

    @property
    def mass(self):
        """mass in M⊕"""
        return self.density * self.diameter**3

    @property
    def climate(self):
        """climate implied by temperature match over World Climate Table"""
        return list(filter(lambda x: self.temperature >= x.value,
                           self.Climate))[-1]

    @property
    def habitability(self):
        """the habitability score"""
        return 0

    def randomize(self):
        """randomizes applicable properties values with precedence constraints"""
        # ranged properties
        rng_props = list(filter(lambda x: hasattr(self, 'random_{}'.format(x)),
                                ['ressource', 'hydrosphere', 'volatile_mass',
                                 'temperature', 'density', 'diameter']))
        for prop in rng_props:
            f = getattr(type(self), 'random_{}'.format(prop))
            if getattr(self, '{}_range'.format(prop)):
                val = f() if ismethod(f) else f(self)
                setattr(self, prop, val)

    def __init__(self):
        self._atmosphere = self._atmosphere(self) if hasattr(type(self), '_atmosphere') else None
        if hasattr(type(self._atmosphere), 'randomize') and callable(getattr(type(self._atmosphere), 'randomize')):
            self._atmosphere.randomize()
        self.randomize()

    def __iter__(self):
        """yield property names and values"""
        for prop in list(filter(lambda x: hasattr(type(self), x)
                         and isinstance(getattr(type(self), x), property),
                         dir(self))):
            yield prop, getattr(self, prop)

    def __str__(self):
        return ('{{class: {}, {}}}'.format(self.__class__.__name__,
                                           ', '.join(['{}: {!s}'.format(prop, value)
                                                     for prop, value in self])))
