# -*- coding: utf-8 -*-

from .. import model
from ..units import d_earth
from ..random import roll2d6, roll3d6, truncnorm_draw
from .marginal_atmosphere import Marginal
from . import Atmosphere

from random import choices
from typing import List
import enum

from scipy.stats import truncnorm
from ordered_enum import ValueOrderedEnum
from astropy import units as u
import numpy as np


class World(model.RandomizableModel):
    """the World Model"""

    _precedence = ['resource', 'hydrosphere', 'volatile_mass',
                   'temperature', 'density', 'diameter']

    @enum.unique
    class Climate(u.Quantity, ValueOrderedEnum):
        """class Climate Enum from world Climate Table with temperature
threshold in K"""
        FROZEN = 0 * u.K
        VERY_COLD = 244 * u.K
        COLD = 255 * u.K
        CHILLY = 266 * u.K
        COOL = 278 * u.K
        NORMAL = 289 * u.K
        WARM = 300 * u.K
        TROPICAL = 311 * u.K
        HOT = 322 * u.K
        VERY_HOT = 333 * u.K
        INFERNAL = 344 * u.K

    class Size(tuple, enum.Enum):
        """class Size Enum from Size Constraints Table"""
        TINY = (.004, .024)
        SMALL = (.024, .030)
        STANDARD = (.030, .065)
        LARGE = (.065, .091)

    class Core(tuple, enum.Enum):
        """class Core Enum from World Density Table"""
        ICY_CORE = (.3 * d_earth, .7 * d_earth)
        SMALL_IRON_CORE = (.6 * d_earth, 1 * d_earth)
        LARGE_IRON_CORE = (.8 * d_earth, 1.2 * d_earth)

    class Resource(int, enum.Enum):
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

    def random_resource(self):
        """sum of a 3d6 roll times over default worlds Ressource Value Table"""
        ressource_dist = [0, 0, 0, .01852, .14352, .67592,
                          .14352, .01852, 0, 0, 0]
        self.resource = choices(list(self.Resource),
                                weights=ressource_dist, k=1)[0]

    def random_temperature(self):
        """sum of a 3d6-3 roll times step value add minimum"""
        tmin = self.temperature_bounds.min.value
        tmax = self.temperature_bounds.max.value
        roll = roll3d6(-3, continuous=True)
        self.temperature = (tmin + roll / 15 * (tmax - tmin)) * u.K

    def random_density(self):
        """sum of a 3d6 roll over World Density Table"""
        if self.core is not None:
            self.density = (self.density_bounds.min + (self.density_bounds.max -
                            self.density_bounds.min) * truncnorm_draw(0, 1, .376, .2))

    def random_diameter(self):
        """roll of 2d6-2 in range [Dmin, Dmax]"""
        if self.size is not None and self.core is not None:
            self.diameter = (self.diameter_bounds.min + (roll2d6(-2, continuous=True) / 10) *
                             (self.diameter_bounds.max - self.diameter_bounds.min))

    def random_volatile_mass(self):
        """sum of a 3d6 roll divided by 10"""
        if self.atmosphere is not None:
            self.volatile_mass = roll3d6(continuous=True) / 10

    @property
    def size(self) -> Size:
        """size class variable"""
        return self._size if hasattr(self, '_size') else None

    @property
    def core(self) -> Core:
        """core class variable"""
        return self._core if hasattr(self, '_core') else None

    @property
    def pressure_factor(self) -> float:
        """pressure factor class variable"""
        return (self._pressure_factor
                if hasattr(self, '_pressure_factor') else np.nan)

    @property
    def greenhouse_factor(self) -> float:
        """greenhouse_factor class variable"""
        return (self._greenhouse_factor
                if hasattr(self, '_greenhouse_factor') else np.nan)

    @property
    def absorption(self) -> float:
        """absorption"""
        return self._absorption

    @property
    def atmosphere(self) -> List[str]:
        """key properties of the atmosphere"""
        return (self._atmosphere
                if hasattr(self, '_atmosphere') else None)

    @property
    def volatile_mass(self) -> float:
        """relative supply of gaseous elements to other worlds of
the same type"""
        return (self._get_bounded_property('volatile_mass')
                if hasattr(self, '_volatile_mass')
                else np.nan)

    @property
    def volatile_mass_bounds(self) -> model.bounds.ValueBounds:
        """computed value range for volatile mass"""
        return model.bounds.ValueBounds(.3, 1.8) if self.atmosphere else None

    @volatile_mass.setter
    def volatile_mass(self, value: float):
        self._set_bounded_property('volatile_mass', value)

    @property
    def resource(self) -> Resource:
        """resource value on Resource Value Table"""
        return self._get_bounded_property('resource')

    @property
    def resource_bounds(self) -> model.bounds.ValueBounds:
        """resource range class variable"""
        return (self._resource_bounds
                if hasattr(self, '_resource_bounds')
                else model.bounds.ValueBounds(self.Resource.VERY_POOR,
                                              self.Resource.VERY_ABUNDANT))

    @resource.setter
    def resource(self, value: Resource):
        if not isinstance(value, self.Resource):
            raise ValueError('resource value type has to be {}'
                             .format(self.Resource))
        self._set_bounded_property('resource', value)

    @property
    def temperature(self) -> u.Quantity:
        """average temperature in K"""
        return self._get_bounded_property('temperature') * u.K

    @property
    def temperature_bounds(self) -> model.bounds.QuantityBounds:
        """temperature range static class variable in K"""
        return self._temperature_bounds

    @temperature.setter
    def temperature(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'temperature' not in value.unit.physical_type:
            raise ValueError('can\'t set temperature to value of %s physical type' %
                             value.unit.physical_type)
        self._set_bounded_property('temperature', value.to(u.K))

    @property
    def density(self) -> u.Quantity:
        """density in d⊕"""
        return (self._get_bounded_property('density')
                if hasattr(self, '_density')
                else np.nan)

    @property
    def density_bounds(self) -> model.bounds.QuantityBounds:
        """value range for density"""
        return model.bounds.QuantityBounds(*self.core.value) if self.core else None

    @density.setter
    def density(self, value: u.Quantity):
        self._set_bounded_property('density', value)

    @property
    def hydrosphere(self) -> float:
        """proportion of surface covered by liquid elements"""
        return (self._get_bounded_property('hydrosphere')
                if hasattr(self, '_hydrosphere')
                else np.nan)

    @property
    def hydrosphere_bounds(self) -> model.bounds.ValueBounds:
        """hydrosphere value range class variable"""
        return (self._hydrosphere_bounds
                if hasattr(self, '_hydrosphere_bounds') else None)

    @hydrosphere.setter
    def hydrosphere(self, value) -> float:
        self._set_bounded_property('hydrosphere', value)

    @property
    def diameter(self) -> u.Quantity:
        """diameter in D⊕"""
        return (self._get_bounded_property('diameter')
                if hasattr(self, '_diameter')
                else np.nan)

    @property
    def diameter_bounds(self) -> model.bounds.QuantityBounds:
        """computed value range for diameter"""
        return (model.bounds.QuantityBounds(np.sqrt(self.blackbody_temperature / self.density) * self.size[0],
                               np.sqrt(self.blackbody_temperature / self.density) * self.size[1])
                if self.density and self.size else None)

    @diameter.setter
    def diameter(self, value: u.Quantity):
        self._set_bounded_property('diameter', value)

    @property
    def blackbody_correction(self) -> float:
        return (self.absorption
                if np.isnan([self.volatile_mass, self.greenhouse_factor]).any()
                else self.absorption * (1 + self.volatile_mass *
                                        self.greenhouse_factor))

    @property
    def blackbody_temperature(self) -> u.Quantity:
        """blackbody temperature in K"""
        return (self.temperature / self.blackbody_correction)

    @property
    def gravity(self) -> u.Quantity:
        """surface gravity in G⊕"""
        return self.density * self.diameter

    @property
    def mass(self) -> u.Quantity:
        """mass in M⊕"""
        return self.density * self.diameter**3 * u.M_earth

    @property
    def climate(self) -> Climate:
        """climate implied by temperature match over World Climate Table"""
        return list(filter(lambda x: self.temperature >= x, self.Climate))[-1]

    @property
    def habitability(self) -> int:
        """the habitability score"""
        filters = [(self.hydrosphere >= .1 and self.hydrosphere < .6, 1),
                   (self.hydrosphere >= .6 and self.hydrosphere < .9, 2),
                   (self.hydrosphere >= .9, 2)]
        atm = self.atmosphere
        if atm and atm.breathable:
            filters.extend([(atm.pressure_category ==
                             Atmosphere.Pressure.VERY_THIN, 1),
                            (atm.pressure_category ==
                             Atmosphere.Pressure.THIN, 2),
                            (atm.pressure_category in
                             [Atmosphere.Pressure.STANDARD,
                              Atmosphere.Pressure.DENSE], 3),
                            (atm.pressure_category in
                             [Atmosphere.Pressure.VERY_DENSE,
                              Atmosphere.Pressure.SUPER_DENSE], 1),
                            (not issubclass(type(atm), Marginal), 1),
                            (self.climate == self.Climate.COLD, 1),
                            (self.climate >= self.Climate.CHILLY and
                             self.climate <= self.Climate.TROPICAL, 2),
                            (self.climate == self.Climate.HOT, 1)])
        if atm and not atm.breathable:
            filters.extend([(atm and not atm.breathable and
                             atm.corrosive, -2),
                            (atm and not atm.breathable and
                             atm.corrosive, -1)])
        return sum(value if truth else 0 for truth, value in filters)

    @property
    def affinity(self) -> int:
        """the affinity score"""
        return self.resource + self.habitability

    def randomize(self):
        if (hasattr(type(self._atmosphere), 'randomize') and
            callable(getattr(type(self._atmosphere), 'randomize'))):
            self._atmosphere.randomize()
        super(World, self).randomize()

    def __init__(self, orbit=None):

        self._orbit = orbit
        self._atmosphere = (self._atmosphere(self)
                            if hasattr(self, '_atmosphere')
                            else None)
        
        if orbit:
            if not orbit._body:
                orbit._body = self
            world = self
            world.__class__ = orbiting_world(type(self))
    
        self.randomize()


def orbiting_world(world):

    class OrbitingWorld(world):
        """the orbiting world extended model"""
        _precedence = [p for p in World._precedence if p != 'temperature']

        @property
        def blackbody_temperature(self) -> u.Quantity:
            """blackbody temperature in K from orbit"""
            return (278 * np.power(self._orbit._parent_body.luminosity.value, (1 / 4))
                    / np.sqrt(self._orbit.radius.value)) * u.K

        @property
        def temperature(self):
            """average temperature in K"""
            return (self.blackbody_temperature.value *
                    self.blackbody_correction) * u.K

        @temperature.setter
        def temperature(self, _):
            raise AttributeError('can\'t set overriden attribute')

        @property
        def orbit(self):
            """the world orbit around its parent body"""
            return self._orbit

    return OrbitingWorld