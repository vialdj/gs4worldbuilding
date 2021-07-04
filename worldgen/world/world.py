# -*- coding: utf-8 -*-

from .. import Range, RandomizableModel
from .marginal_atmosphere import Marginal
from . import Atmosphere

from random import choices
from enum import Enum
from math import sqrt, floor

from scipy.stats import truncnorm
import numpy as np


class World(RandomizableModel):
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

    def random_ressource(self):
        """sum of a 3d roll times over default worlds Ressource Value Table"""
        ressource_distribution = [0, 0, 0, .01852, .14352, .67592,
                                  .14352, .01852, 0, 0, 0]
        self.ressource = choices(list(self.Ressource),
                                 weights=ressource_distribution, k=1)[0]

    def random_temperature(self):
        """sum of a 3d-3 roll times step value add minimum"""
        tmin = self.temperature_range.min
        tmax = self.temperature_range.max
        roll = truncnorm((0 - 7.5) / 2.958040, (15 - 7.5) / 2.958040,
                         loc=7.5, scale=2.958040).rvs()
        self.temperature = tmin + roll / 15 * (tmax - tmin)

    def random_density(self):
        """sum of a 3d roll over World Density Table"""
        if self.core is not None:
            self.density = (self.density_range.min + (self.density_range.max -
                            self.density_range.min) *
                            truncnorm((0 - 0.376) / 0.2, (1 - 0.376) / 0.2,
                            loc=0.376, scale=0.2).rvs())

    def random_diameter(self):
        """roll of 2d-2 in range [Dmin, Dmax]"""
        if self.size is not None and self.core is not None:
            self.diameter = (self.diameter_range.min + np.random.triangular(0, .5, 1) *
                             (self.diameter_range.max - self.diameter_range.min))

    def random_volatile_mass(self):
        """sum of a 3d roll divided by 10"""
        if self.atmosphere is not None:
            self.volatile_mass = truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
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
        self._set_ranged_property('volatile_mass', value)

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
        self._set_ranged_property('ressource', value)

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
        self._set_ranged_property('temperature', value)

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
        self._set_ranged_property('density', value)

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
        self._set_ranged_property('hydrosphere', value)

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
        self._set_ranged_property('diameter', value)

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
        filters = [(self.hydrosphere >= .1 and self.hydrosphere < .6, 1),
                   (self.hydrosphere >= .6 and self.hydrosphere < .9, 2),
                   (self.hydrosphere >= .9, 2)]
        atm = self.atmosphere
        if atm and atm.breathable:
            filters.extend([(atm.pressure_category == Atmosphere.Pressure.VERY_THIN, 1),
                            (atm.pressure_category == Atmosphere.Pressure.THIN, 2),
                            (atm.pressure_category in [Atmosphere.Pressure.STANDARD, Atmosphere.Pressure.DENSE], 3),
                            (atm.pressure_category in [Atmosphere.Pressure.VERY_DENSE, Atmosphere.Pressure.SUPER_DENSE], 1),
                            (not issubclass(type(atm), Marginal), 1),
                            (self.climate == self.Climate.COLD, 1),
                            (self.climate >= self.Climate.CHILLY and self.climate <= self.Climate.TROPICAL, 2),
                            (self.climate == self.Climate.HOT, 1)])
        if atm and not atm.breathable:
            filters.extend([(atm and not atm.breathable and atm.corrosive, -2),
                            (atm and not atm.breathable and atm.corrosive, -1)])
        return sum(value if truth else 0 for truth, value in filters)

    @property
    def affinity(self):
        """the affinity score"""
        return self.ressource + self.habitability

    def __init__(self):
        self._atmosphere = self._atmosphere(self) if hasattr(type(self), '_atmosphere') else None
        if hasattr(type(self._atmosphere), 'randomize') and callable(getattr(type(self._atmosphere), 'randomize')):
            self._atmosphere.randomize()
        self.randomize(['ressource', 'hydrosphere', 'volatile_mass',
                        'temperature', 'density', 'diameter'])