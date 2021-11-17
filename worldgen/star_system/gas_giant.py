# -*- coding: utf-8 -*-

from . import Orbit, Star
from .. import model, random

from random import choices
import enum

from astropy import units as u
import numpy as np


class GasGiant(model.RandomizableModel):
    """the World Model"""

    _precedence = ['mass']

    class GasGiantOrbit(Orbit):
        """The gas giant orbit model"""

        # TODO: watchout for epistellar modifier
        def random_eccentricity(self):
            if (self._parent_body.gas_giant_arrangement == Star.GasGiantArrangement.ECCENTRIC and
                self.radius <= self._parent_body.snow_line):
                self.eccentricity = random.truncnorm_draw(.1, .8, .45435, .23165400385057022)
            else:
                self.eccentricity = random.truncnorm_draw(.0, .2, .04625, .042877004326328585)

        @property
        # TODO: watchout for epistellar modifier
        def eccentricity_bounds(self) -> model.bounds.ValueBounds:
            """value range for eccentricity dependent separation"""
            if (self._parent_body.gas_giant_arrangement == Star.GasGiantArrangement.ECCENTRIC and
                self.radius <= self._parent_body.snow_line):
                return model.bounds.ValueBounds(.1, .8)
            else:
                return model.bounds.ValueBounds(.0, .2)

    class Size(enum.Enum):
        """class Size Enum from Size Constraints Table"""
        SMALL = enum.auto()
        MEDIUM = enum.auto()
        LARGE = enum.auto()

    @property
    def size(self) -> Size:
        """size class variable"""
        return type(self)._size if hasattr(type(self), '_size') else None

    @property
    def mass(self) -> u.Quantity:
        """mass in M⊕"""
        return self._get_bounded_property('mass') * u.M_earth

    @property
    def mass_bounds(self) -> model.bounds.QuantityBounds:
        """Mass range static class variable in M⊕"""
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
    def orbit(self) -> GasGiantOrbit:
        """the GasGiant orbit around its parent body"""
        return self._orbit

    @property
    def diameter(self) -> u.Quantity:
        """diameter in D⊕"""
        return np.power(self.mass.value / self.density.value, (1 / 3))

    def __init__(self, parent_body, radius):
        self._orbit = type(self).GasGiantOrbit(parent_body, self, radius)

        self.randomize()