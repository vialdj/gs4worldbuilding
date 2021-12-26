# -*- coding: utf-8 -*-

from .. import World, Planet
from ..model import RandomizableModel, bounds
from ..units import d_earth, D_earth, G_earth
from ..random import roll2d6, roll3d6, truncnorm_draw
from .marginal_atmosphere import Marginal
from . import Atmosphere

import enum
from abc import ABC

from ordered_enum import OrderedEnum
from astropy import units as u
import numpy as np


class Terrestrial(RandomizableModel, World, Planet, ABC):
    """the Terrestrial World Model"""

    _precedence = ['resource', 'hydrographic_coverage', 'volatile_mass',
                   'temperature', 'density', 'diameter']
    _resource_bounds = bounds.ValueBounds(World.Resource.SCANT,
                                          World.Resource.RICH)

    class Size(tuple, OrderedEnum):
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

    def random_resource(self):
        """sum of a 3d roll times over Resource Value Table"""
        resource_value_table = {3: World.Resource.SCANT,
                                5: World.Resource.VERY_POOR,
                                8: World.Resource.POOR,
                                14: World.Resource.AVERAGE,
                                17: World.Resource.ABUNDANT,
                                19: World.Resource.VERY_ABUNDANT}
        roll = roll3d6()
        filtered = list(filter(lambda x: roll >= x[0],
                               resource_value_table.items()))
        self.resource = (filtered[-1][1] if len(filtered) > 0
                         else World.Resource.RICH)

    def random_density(self):
        """sum of a 3d6 roll over World Density Table"""
        if self.core is not None:
            self.density = (self.density_bounds.min +
                            (self.density_bounds.max -
                             self.density_bounds.min) *
                            truncnorm_draw(0, 1, .376, .2))

    def random_diameter(self):
        """roll of 2d6-2 in range [Dmin, Dmax]"""
        if self.size is not None and self.core is not None:
            self.diameter = (self.diameter_bounds.min +
                             (roll2d6(-2, continuous=True) / 10) *
                             (self.diameter_bounds.max -
                              self.diameter_bounds.min))

    def random_volatile_mass(self):
        """sum of a 3d6 roll divided by 10"""
        if self.atmosphere is not None:
            self.volatile_mass = roll3d6(continuous=True) / 10

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
    def atmosphere(self):
        return (self._atmosphere if hasattr(self, '_atmosphere') else None)

    @property
    def volatile_mass(self) -> float:
        """relative supply of gaseous elements to other worlds of
the same type"""
        return (self._get_bounded_property('volatile_mass')
                if hasattr(self, '_volatile_mass')
                else np.nan)

    @property
    def volatile_mass_bounds(self) -> bounds.ValueBounds:
        """computed value range for volatile mass"""
        return bounds.ValueBounds(.3, 1.8) if self.atmosphere else None

    @volatile_mass.setter
    def volatile_mass(self, value: float):
        self._set_bounded_property('volatile_mass', value)

    @property
    def density(self) -> u.Quantity:
        return (self._get_bounded_property('density')
                if hasattr(self, '_density')
                else np.nan) * d_earth

    @property
    def density_bounds(self) -> bounds.QuantityBounds:
        """value range for density"""
        return (bounds.QuantityBounds(*self.core.value)
                if self.core else None)

    @density.setter
    def density(self, value: u.Quantity):
        self._set_bounded_property('density', value)

    @property
    def hydrographic_coverage(self) -> float:
        """proportion of surface covered by liquid elements"""
        return (self._get_bounded_property('hydrographic_coverage')
                if hasattr(self, '_hydrographic_coverage')
                else np.nan)

    @property
    def hydrographic_coverage_bounds(self) -> bounds.ValueBounds:
        """hydrographic_coverage value range class variable"""
        return (self._hydrographic_coverage_bounds
                if hasattr(self, '_hydrographic_coverage_bounds') else None)

    @hydrographic_coverage.setter
    def hydrographic_coverage(self, value) -> float:
        self._set_bounded_property('hydrographic_coverage', value)

    @property
    def diameter(self) -> u.Quantity:
        """diameter in D⊕"""
        return (self._get_bounded_property('diameter')
                if hasattr(self, '_diameter')
                else np.nan) * D_earth

    @property
    def diameter_bounds(self) -> bounds.QuantityBounds:
        """computed value range for diameter"""
        return (bounds.QuantityBounds(
                np.sqrt(self.blackbody_temperature.value / self.density.value)
                * self.size[0] * D_earth,
                np.sqrt(self.blackbody_temperature.value / self.density.value)
                * self.size[1] * D_earth)
                if self.density and self.size else None)

    @diameter.setter
    def diameter(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'length' not in value.unit.physical_type:
            raise ValueError('can\'t set diameter to value of %s physical type'
                             % value.unit.physical_type)
        self._set_bounded_property('diameter', value.to(D_earth))

    @property
    def blackbody_correction(self) -> float:
        return ((self.absorption * (1 + self.volatile_mass *
                                   self.greenhouse_factor))
                if self.atmosphere else self.absorption)

    @property
    def blackbody_temperature(self) -> u.Quantity:
        """blackbody temperature in K"""
        return (self.temperature / self.blackbody_correction)

    @property
    def gravity(self) -> u.Quantity:
        """surface gravity in g"""
        return self.density.value * self.diameter.value * G_earth

    @property
    def mass(self) -> u.Quantity:
        """mass in M⊕"""
        return self.density.value * self.diameter.value ** 3 * u.M_earth

    @property
    def habitability(self) -> int:
        """the habitability score"""
        filters = [(self.hydrographic_coverage >= .1 and
                    self.hydrographic_coverage < .6, 1),
                   (self.hydrographic_coverage >= .6 and
                    self.hydrographic_coverage < .9, 2),
                   (self.hydrographic_coverage >= .9, 2)]
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
        super(Terrestrial, self).randomize()

    def __init__(self, orbit=None):

        self._orbit = orbit
        self._atmosphere = (self._atmosphere(self)
                            if hasattr(self, '_atmosphere')
                            else None)

        if orbit:
            if not orbit._body:
                orbit._body = self
            world = self
            world.__class__ = (satellite(type(self))
                               if issubclass(type(orbit._parent_body),
                                             type(self))
                               else inplace(type(self)))

        self.randomize()


def inplace(world):

    class InplaceTerrestrial(world):
        """the orbiting world extended model"""
        _precedence = [p for p in world._precedence
                       if p != 'temperature']

        @property
        def blackbody_temperature(self) -> u.Quantity:
            """blackbody temperature in K from orbit"""
            return (278 * np.power(self._orbit._parent_body.luminosity.value,
                                   (1 / 4)) /
                    np.sqrt(self._orbit.radius.value)) * u.K

        @property
        def temperature(self) -> u.Quantity:
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

        @property
        def moons(self):
            """the world moons"""
            return 0
            # return self._n_moons + self._n_moonlets

    return InplaceTerrestrial


def satellite(world):

    class TerrestrialSatellite(world):

        @property
        def blackbody_temperature(self) -> u.Quantity:
            """blackbody temperature in K from parent body"""
            return self._orbit._parent_body.blackbody_temperature

    return TerrestrialSatellite
