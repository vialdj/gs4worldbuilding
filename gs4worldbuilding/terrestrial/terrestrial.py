# -*- coding: utf-8 -*-

from .. import World, Planet, InplacePlanet, gas_giant
from ..model import RandomizableModel, bounds
from ..units import d_earth, D_earth, G_earth
from ..random import RandomGenerator
from .marginal_atmosphere import Marginal
from . import Atmosphere, Pressure

import enum
from abc import ABC

from ordered_enum import OrderedEnum
from astropy import units as u
import numpy as np


class Terrestrial(RandomizableModel, World, Planet, ABC):
    """the Terrestrial World Model"""

    _precedence = ['hydrographic_coverage', 'volatile_mass',
                   'temperature', 'density', 'diameter', 'resource']
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
        table = {3: World.Resource.SCANT,
                 5: World.Resource.VERY_POOR,
                 8: World.Resource.POOR,
                 14: World.Resource.AVERAGE,
                 17: World.Resource.ABUNDANT,
                 19: World.Resource.VERY_ABUNDANT}
        roll = RandomGenerator().roll3d6()
        filtered = list(filter(lambda x: roll < x, table.keys()))
        self.resource = (table[filtered[0]] if len(filtered) > 0 else
                         World.Resource.RICH)

    def random_density(self):
        """sum of a 3d6 roll over World Density Table"""
        if self.core is not None:
            self.density = (self.density_bounds.lower +
                            (self.density_bounds.upper -
                             self.density_bounds.lower) *
                            RandomGenerator().truncnorm_draw(0, 1, .376, .2))

    def random_diameter(self):
        """roll of 2d6-2 in range [Dmin, Dmax]"""
        if self.size is not None and self.core is not None:
            self.diameter = (self.diameter_bounds.lower +
                             (RandomGenerator().roll2d6(-2, continuous=True) / 10) *
                             (self.diameter_bounds.upper -
                              self.diameter_bounds.lower))

    def random_volatile_mass(self):
        """sum of a 3d6 roll divided by 10"""
        if self.atmosphere is not None:
            self.volatile_mass = RandomGenerator().roll3d6(continuous=True) / 10

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
                else np.nan)

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
        """diameter in D🜨"""
        return (self._get_bounded_property('diameter')
                if hasattr(self, '_diameter')
                else np.nan)

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
    def mass(self) -> u.Quantity:
        """mass in M🜨"""
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
                             Pressure.VERY_THIN, 1),
                            (atm.pressure_category ==
                             Pressure.THIN, 2),
                            (atm.pressure_category in
                             [Pressure.STANDARD,
                              Pressure.DENSE], 3),
                            (atm.pressure_category in
                             [Pressure.VERY_DENSE,
                              Pressure.SUPER_DENSE], 1),
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
        super().randomize()

    def __init__(self, orbit=None):

        self._orbit = orbit
        self._atmosphere = (self._atmosphere(self)
                            if hasattr(self, '_atmosphere')
                            else None)
        if orbit:
            if not orbit._body:
                orbit._body = self
            world = self
            world.__class__ = (place_satellite(type(self))
                               if issubclass(type(orbit._parent_body),
                                             Planet)
                               else place_terrestrial(type(self)))

        self.randomize()


class InplaceTerrestrial(Terrestrial, InplacePlanet):
    """the orbiting world extended model"""
    _precedence = [*[p for p in Terrestrial._precedence if
                     (p != 'temperature' and p != 'resource')],
                   'rotation', 'resonant', 'retrograde', 'axial_tilt',
                   'volcanic_activity', 'tectonic_activity', 'resource']
    _rotation_modifiers = {Terrestrial.Size.TINY: 18,
                           Terrestrial.Size.SMALL: 14,
                           Terrestrial.Size.STANDARD: 10,
                           Terrestrial.Size.LARGE: 6}

    class TectonicActivity(OrderedEnum):
        """class tectonic activity category Enum from corresponding table"""
        NONE = 'No tectonic activity'
        LIGHT = 'Light tectonic activity'
        MODERATE = 'Moderate tectonic activity'
        HEAVY = 'Heavy tectonic activity'
        EXTREME = 'Extreme tectonic activity'

    class VolcanicActivity(OrderedEnum):
        """class volcanic activity category Enum from corresponding table"""
        NONE = 'No volcanic activity'
        LIGHT = 'Light volcanic activity'
        MODERATE = 'Moderate volcanic activity'
        HEAVY = 'Heavy volcanic activity'
        EXTREME = 'Extreme volcanic activity'

    def random_resource(self):
        """sum of a 3d roll times over Resource Value Table with volcanism modifier"""
        table = {3: World.Resource.SCANT,
                 5: World.Resource.VERY_POOR,
                 8: World.Resource.POOR,
                 14: World.Resource.AVERAGE,
                 17: World.Resource.ABUNDANT,
                 19: World.Resource.VERY_ABUNDANT}
        modifiers = {self.VolcanicActivity.NONE: -2,
                     self.VolcanicActivity.LIGHT: -1,
                     self.VolcanicActivity.MODERATE: 0,
                     self.VolcanicActivity.HEAVY: 1,
                     self.VolcanicActivity.EXTREME: 2}
        roll = RandomGenerator().roll3d6(modifiers[self.volcanic_activity])
        filtered = list(filter(lambda x: roll < x, table.keys()))
        self.resource = (table[filtered[0]] if len(filtered) > 0 else
                         World.Resource.RICH)

    def random_tectonic_activity(self) -> None:
        table = {7: self.TectonicActivity.NONE,
                 11: self.TectonicActivity.LIGHT,
                 15: self.TectonicActivity.MODERATE,
                 19: self.TectonicActivity.HEAVY}
        filters = [(self.volcanic_activity ==
                    self.VolcanicActivity.NONE, -8),
                   (self.volcanic_activity ==
                    self.VolcanicActivity.LIGHT, -4),
                   (self.volcanic_activity ==
                    self.VolcanicActivity.HEAVY, 4),
                   (self.volcanic_activity ==
                    self.VolcanicActivity.EXTREME, 8),
                   (self.hydrographic_coverage == 0, -4),
                   (self.hydrographic_coverage > 0 and
                    self.hydrographic_coverage < .5, -2),
                   (hasattr(self, '_moons') and len(self._moons) == 1, 2),
                   (hasattr(self, '_moons') and len(self._moons) > 1, 4)]
        roll = RandomGenerator().roll3d6(sum(value if truth else 0 for
                                         truth, value in filters))
        filtered = list(filter(lambda x: roll < x, table.keys()))
        self.tectonic_activity = ((table[filtered[0]] if
                                   len(filtered) > 0 else
                                   type(self).TectonicActivity.EXTREME) if
                                  self.size > type(self).Size.SMALL else
                                  type(self).TectonicActivity.NONE)

    def random_volcanic_activity(self) -> None:
        table = {17: self.VolcanicActivity.NONE,
                 21: self.VolcanicActivity.LIGHT,
                 27: self.VolcanicActivity.MODERATE,
                 71: self.VolcanicActivity.HEAVY}
        age = (self._orbit._parent_body._star_system.age
               if not issubclass(type(self._orbit._parent_body), Planet)
               else self._orbit._parent_body._orbit._parent_body._star_system.age)
        modifier = round((self.gravity.value / age.value) * 40)
        modifiers = [(hasattr(self, '_moons') and len(self._moons) == 1, 5),
                     (hasattr(self, '_moons') and len(self._moons) > 1, 10),
                     (self._designation == 'Tiny (Sulfur)', 60),
                     (issubclass(type(self._orbit._parent_body),
                                 gas_giant.GasGiant), 5)]
        roll = RandomGenerator().roll3d6(modifier + sum(value if truth else 0
                                         for truth, value in modifiers))
        filtered = list(filter(lambda x: roll < x, table.keys()))
        self.volcanic_activity = (table[filtered[0]] if len(filtered) > 0
                                  else type(self).VolcanicActivity.EXTREME)

    @property
    def blackbody_temperature(self) -> u.Quantity:
        return InplacePlanet.blackbody_temperature.fget(self)

    @property
    def habitability(self) -> int:
        modifiers = [(self.volcanic_activity == self.VolcanicActivity.HEAVY,
                      -1),
                     (self.tectonic_activity == self.TectonicActivity.HEAVY,
                      -1),
                     (self.volcanic_activity == self.VolcanicActivity.EXTREME,
                      -2),
                     (self.tectonic_activity == self.TectonicActivity.EXTREME,
                      -2)]
        return (Terrestrial.habitability.fget(self) +
                max(sum(value if truth else 0 for truth, value in modifiers),
                    -2))

    @property
    def resource_bounds(self) -> bounds.ValueBounds:
        modifiers = {self.VolcanicActivity.NONE: -2,
                     self.VolcanicActivity.LIGHT: -1,
                     self.VolcanicActivity.MODERATE: 0,
                     self.VolcanicActivity.HEAVY: 1,
                     self.VolcanicActivity.EXTREME: 2}
        modifier = modifiers[self.volcanic_activity]

        value_bounds = Terrestrial.resource_bounds.fget(self)
        return bounds.ValueBounds(value_bounds.lower + modifier,
                                  value_bounds.upper + modifier)

    @property
    def temperature(self) -> u.Quantity:
        """average temperature in K"""
        return (self.blackbody_temperature.value *
                self.blackbody_correction) * u.K

    @temperature.setter
    def temperature(self, _):
        raise AttributeError('can\'t set overriden attribute')

    @property
    def tectonic_activity(self):
        """tectonic activity value on corresponding Table"""
        return self._get_bounded_property('tectonic_activity')

    @property
    def tectonic_activity_bounds(self) -> bounds.ValueBounds:
        """tectonic activity range"""
        table = {7: self.TectonicActivity.NONE,
                 11: self.TectonicActivity.LIGHT,
                 15: self.TectonicActivity.MODERATE,
                 19: self.TectonicActivity.HEAVY}
        modifiers = [(self.volcanic_activity ==
                      self.VolcanicActivity.NONE, -8),
                     (self.volcanic_activity ==
                      self.VolcanicActivity.LIGHT, -4),
                     (self.volcanic_activity ==
                      self.VolcanicActivity.HEAVY, 4),
                     (self.volcanic_activity ==
                      self.VolcanicActivity.EXTREME, 8),
                     (self.hydrographic_coverage == 0, -4),
                     (self.hydrographic_coverage > 0 and
                      self.hydrographic_coverage < .5, -2),
                     (hasattr(self, '_moons') and
                      len(self._moons) == 1, 2),
                     (hasattr(self, '_moons') and len(self._moons) > 1, 4)]
        min_roll = sum(value if truth else 0 for
                       truth, value in modifiers) + 3
        filtered = list(filter(lambda x: min_roll < x, table.keys()))
        min = (table[filtered[0]] if len(filtered) > 0
               else type(self).TectonicActivity.EXTREME)
        max_roll = min_roll + 15
        filtered = list(filter(lambda x: max_roll < x, table.keys()))
        max = (table[filtered[0]] if len(filtered) > 0
               else type(self).TectonicActivity.EXTREME)
        return (bounds.ValueBounds(min, max) if
                self.size > type(self).Size.SMALL else
                bounds.ValueBounds(self.TectonicActivity.NONE,
                                   self.TectonicActivity.NONE))

    @tectonic_activity.setter
    def tectonic_activity(self, value):
        if not isinstance(value, self.TectonicActivity):
            raise ValueError('tectonic activity value type has to be' +
                             f'{self.TectonicActivity}')
        self._set_bounded_property('tectonic_activity', value)

    @property
    def volcanic_activity(self):
        """volcanic activity value on corresponding Table"""
        return self._get_bounded_property('volcanic_activity')

    @property
    def volcanic_activity_bounds(self) -> bounds.ValueBounds:
        """volcanic activity range"""
        table = {17: self.VolcanicActivity.NONE,
                 21: self.VolcanicActivity.LIGHT,
                 27: self.VolcanicActivity.MODERATE,
                 71: self.VolcanicActivity.HEAVY}
        age = (self._orbit._parent_body._star_system.age if
               not issubclass(type(self._orbit._parent_body), Planet) else
               self._orbit._parent_body._orbit._parent_body._star_system.age)
        min_roll = round((self.gravity.value / age.value) * 40) + 3
        modifiers = [(hasattr(self, '_moons') and
                      len(self._moons) == 1, 5),
                     (hasattr(self, '_moons') and
                      len(self._moons) > 1, 10),
                     (self._designation == 'Tiny (Sulfur)', 60),
                     (issubclass(type(self._orbit._parent_body),
                                 gas_giant.GasGiant), 5)]
        min_roll += sum(value if truth else 0 for truth, value in modifiers)
        filtered = list(filter(lambda x: min_roll < x, table.keys()))
        min = (table[filtered[0]] if len(filtered) > 0
               else type(self).VolcanicActivity.EXTREME)
        max_roll = min_roll + 15
        filtered = list(filter(lambda x: max_roll < x, table.keys()))
        max = (table[filtered[0]] if len(filtered) > 0
               else type(self).VolcanicActivity.EXTREME)
        return bounds.ValueBounds(min, max)

    @volcanic_activity.setter
    def volcanic_activity(self, value):
        if not isinstance(value, self.VolcanicActivity):
            raise ValueError('volcanic activity value type has to be ' +
                             f'{self.VolcanicActivity}')
        self._set_bounded_property('volcanic_activity', value)


def place_terrestrial(world):

    class ConcreteInplaceTerrestrial(world, InplaceTerrestrial):
        pass

    return ConcreteInplaceTerrestrial


def place_satellite(world):

    class Satellite(world, InplaceTerrestrial):

        _precedence = InplaceTerrestrial._precedence
        _rotation_modifiers = {world.Size.TINY: 18,
                               world.Size.SMALL: 14,
                               world.Size.STANDARD: 10,
                               world.Size.LARGE: 6}

        @property
        def blackbody_temperature(self) -> u.Quantity:
            """blackbody temperature in K from parent body"""
            return self._orbit._parent_body.blackbody_temperature

        @property
        def solar_day(self) -> u.Quantity:
            """solar day in standard hours"""
            rotation = -self.rotation if self.retrograde else self.rotation
            return abs((self._orbit._parent_body._orbit.period.to(u.h).value *
                        rotation.to(u.h).value) /
                       (self._orbit._parent_body._orbit.period.to(u.h).value -
                        rotation.to(u.h).value)
                       if rotation != self._orbit.period else np.inf) * u.h

        @property
        def tidal_effect(self) -> bool:
            """the total tidal effect property"""
            # computing the planet tidal force
            tidal_force = ((2230000 * self._orbit._parent_body.mass.value *
                            self.diameter.value) /
                           self._orbit.radius.to(D_earth).value ** 3)
            return round(tidal_force *
                         self._orbit._parent_body._orbit._parent_body._star_system.age.value /
                         self.mass.value)

    return Satellite
