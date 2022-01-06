# -*- coding: utf-8 -*-

from .planet import InplacePlanet
from . import model, random, units
from .orbit import Orbit

import enum
from abc import ABC

from astropy import units as u
import numpy as np
from ordered_enum import OrderedEnum


class GasGiant(model.RandomizableModel, InplacePlanet, ABC):
    """the World Model"""

    _precedence = ['mass', 'rotation']

    class GasGiantOrbit(Orbit):
        """The gas giant orbit model"""

        # TODO: watchout for epistellar modifier
        def random_eccentricity(self):
            if (self._parent_body.gas_giant_arrangement == type(self._parent_body).GasGiantArrangement.ECCENTRIC and
                self.radius <= self._parent_body.snow_line):
                self.eccentricity = random.truncnorm_draw(.1, .8, .45435, .23165400385057022)
            else:
                self.eccentricity = random.truncnorm_draw(.0, .2, .04625, .042877004326328585)

        @property
        # TODO: watchout for epistellar modifier
        def eccentricity_bounds(self) -> model.bounds.ValueBounds:
            """value range for eccentricity dependent separation"""
            if (self._parent_body.gas_giant_arrangement == type(self._parent_body).GasGiantArrangement.ECCENTRIC and
                self.radius <= self._parent_body.snow_line):
                return model.bounds.ValueBounds(.1, .8)
            else:
                return model.bounds.ValueBounds(.0, .2)

    class Size(OrderedEnum):
        """class Size Enum from Size Constraints Table"""
        SMALL = enum.auto()
        MEDIUM = enum.auto()
        LARGE = enum.auto()

    _rotation_modifiers = {Size.SMALL: 6,
                           Size.MEDIUM: 0,
                           Size.LARGE: 0}

    @property
    def size(self) -> Size:
        """size class variable"""
        return type(self)._size if hasattr(type(self), '_size') else None

    @property
    def mass(self) -> u.Quantity:
        """mass in M🜨"""
        return self._get_bounded_property('mass') * u.M_earth

    @property
    def mass_bounds(self) -> model.bounds.QuantityBounds:
        """Mass range static class variable in M🜨"""
        return type(self)._mass_bounds

    @mass.setter
    def mass(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'mass' not in value.unit.physical_type:
            raise ValueError('can\'t set mass to value of %s physical type' %
                             value.unit.physical_type)
        self._set_bounded_property('mass', value.to(u.M_earth))

    @property
    def diameter(self) -> u.Quantity:
        """diameter in D🜨"""
        return (np.power(self.mass.value / self.density.value, (1 / 3))
                * units.D_earth)

    def __init__(self, parent_body, radius):
        self._orbit = type(self).GasGiantOrbit(parent_body, radius, self)
        self.randomize()


class SmallGasGiant(GasGiant):
    """The small gas giant model"""

    _mass_bounds = model.bounds.QuantityBounds(10 * u.M_earth, 80 * u.M_earth)
    _size = GasGiant.Size.SMALL

    def random_mass(self):
        """small mass pdf fit as a truncated exponential"""
        self.mass = (random.truncexpon_draw(10, 80, 17.69518578597015) *
                     u.M_earth)

    @property
    def density(self) -> u.Quantity:
        """small density in d🜨 from Gas Giant Size Table fitted as ax**b+c"""
        return (74.43464003356911 * self.mass.value ** -2.473690314600168
                + .17) * units.d_earth


class MediumGasGiant(GasGiant):
    """The medium gas giant model"""

    _mass_bounds = model.bounds.QuantityBounds(100 * u.M_earth,
                                               500 * u.M_earth)
    _size = GasGiant.Size.MEDIUM

    def random_mass(self):
        """medium mass pdf fit as a truncated normal"""
        self.mass = (random.truncexpon_draw(100, 500, 102.41483046902924) *
                     u.M_earth)

    @property
    def density(self) -> u.Quantity:
        """medium density in d🜨 from Gas Giant Size Table fitted as ax+b"""
        return ((.0002766666669434452 * self.mass.value + .15033333325029977)
                * units.d_earth)


class LargeGasGiant(GasGiant):
    """The large gas giant model"""

    _mass_bounds = model.bounds.QuantityBounds(600 * u.M_earth,
                                               4000 * u.M_earth)
    _size = GasGiant.Size.LARGE

    def random_mass(self):
        """large mass pdf fit as a truncated exponential"""
        self.mass = (random.truncexpon_draw(600, 4000, 872.1918137657565) *
                     u.M_earth)

    @property
    def density(self) -> u.Quantity:
        """large density in d🜨 from Gas Giant Size Table fitted as ax+b"""
        return ((.0003880597018732323 * self.mass.value + .036185736947409355)
                * units.d_earth)
