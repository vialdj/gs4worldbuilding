# -*- coding: utf-8 -*-

from .. import model

from random import choices
import enum

from astropy import units as u
import numpy as np


class GasGiant(model.RandomizableModel):
    """the World Model"""

    _precedence = ['mass']

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
    def diameter(self) -> u.Quantity:
        """diameter in D⊕"""
        return np.power(self.mass.value / self.density.value, (1 / 3))

    def __init__(self, **kw):
        super(GasGiant, self).__init__(**kw)
