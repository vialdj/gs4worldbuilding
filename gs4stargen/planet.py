# -*- coding: utf-8 -*-
from .model import bounds
from .random import roll3d6, roll2d6, roll1d6

from abc import ABC, abstractmethod

import numpy as np
from astropy import units as u


class Planet(ABC):
    """the Planet interface"""

    @property
    def size(self):
        """size class variable"""
        return self._size

    @property
    @abstractmethod
    def density(self) -> u.Quantity:
        """density in d🜨"""
        pass

    @property
    @abstractmethod
    def diameter(self) -> u.Quantity:
        """diameter in D🜨"""
        pass

    @property
    @abstractmethod
    def mass(self) -> u.Quantity:
        """mass in M🜨"""
        pass


class InplacePlanet(Planet, ABC):
    """the Planet given orbital parameters as an abstract class"""

    def random_rotation(self) -> None:
        """Roll over Rotation Table and Special Rotation Table if applicable"""
        initial_roll = roll3d6(continuous=True)
        if (initial_roll > 16 or initial_roll +
            self._rotation_modifiers[self.size] > 36):
            special_roll = roll2d6()
            self.rotation = ({7: 48, 8: 120, 9: 240, 10: 480, 11: 1200,
                              12: 2400}[special_roll] *
                             roll1d6(continuous=True)
                             if special_roll > 6 else initial_roll) * u.h
        else:
            self.rotation = (initial_roll +
                             self._rotation_modifiers[self.size]) * u.h

    @property
    def blackbody_temperature(self) -> u.Quantity:
        """blackbody temperature in K from orbit"""
        return (278 * np.power(self._orbit._parent_body.luminosity.value,
                               (1 / 4)) /
                np.sqrt(self._orbit.radius.value)) * u.K

    @property
    def orbit(self):
        """the planets orbit around its parent body"""
        return self._orbit

    @property
    def rotation(self) -> u.Quantity:
        """rotation in standard hours"""
        return self._get_bounded_property('rotation') * u.h

    @property
    def rotation_bounds(self) -> bounds.QuantityBounds:
        """rotation bounds in hours"""
        return bounds.QuantityBounds(self._rotation_modifiers[self.size] * u.h,
                                     self._orbit.period.to(u.h))

    @rotation.setter
    def rotation(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'time' not in value.unit.physical_type:
            raise ValueError('can\'t set rotation to value of'
                             + ' %s physical type' %
                             value.unit.physical_type)
        self._set_bounded_property('rotation', value.to(u.h))

    @property
    def moons(self):
        """the world moons"""
        return 0
