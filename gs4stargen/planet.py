# -*- coding: utf-8 -*-
from .model import bounds
from .random import roll3d6, roll2d6, roll1d6
from .units import D_earth, G_earth

from abc import ABC, abstractmethod

import numpy as np
from astropy import units as u


class Planet(ABC):
    """the Planet abstract class"""

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
    def gravity(self) -> u.Quantity:
        """surface gravity in g"""
        return self.density.value * self.diameter.value * G_earth

    @property
    @abstractmethod
    def mass(self) -> u.Quantity:
        """mass in M🜨"""
        pass


class InplacePlanet(Planet, ABC):
    """the Planet given orbital parameters as an abstract class"""

    def random_axial_tilt(self) -> None:
        """Roll 3d over Axial Tilt Tables to define axial tilt"""
        tilt_roll = roll2d6(-2, continuous=True)
        table_roll = roll3d6()
        if table_roll < 17:
            table = {6: 0, 9: 10, 12: 20, 14: 30, 16: 40}
        else:
            table_roll = roll1d6()
            table = {2: 50, 4: 60, 5: 70, 6: 80}
        self.axial_tilt = (table[list(filter(lambda x: table_roll <= x,
                           table.keys()))[0]]
                           + tilt_roll) * u.deg

    def random_retrograde(self) -> None:
        """Roll 3d to define retrograde property"""
        self.retrograde = True if roll3d6() > 13 else False

    def random_rotation(self) -> None:
        """Roll over Rotation Table and Special Rotation Table if applicable"""
        initial_roll = roll3d6(continuous=True)
        if (initial_roll > 16 or initial_roll +
            self._rotation_modifiers[self.size] > 36):
            special_roll = roll2d6()
            rotation = ({7: 48, 8: 120, 9: 240, 10: 480, 11: 1200,
                         12: 2400}[special_roll] * roll1d6(continuous=True)
                         if special_roll > 6 else initial_roll) * u.h
        else:
            rotation = (initial_roll +
                        self._rotation_modifiers[self.size]) * u.h
        self.rotation = min(rotation, self.rotation_bounds.max)

    @property
    def axial_tilt(self) -> u.Quantity:
        """the planet axial tilt in degrees, > 90 if the rotation has the retrograde property"""
        tilt = self._get_bounded_property('axial_tilt')
        return (180 - tilt if self.retrograde else tilt) * u.deg

    @property
    def axial_tilt_bounds(self) -> bounds.QuantityBounds:
        """axial tilt bounds in degrees"""
        return bounds.QuantityBounds(0 * u.deg, 90 * u.deg)

    @axial_tilt.setter
    def axial_tilt(self, value):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError('can\'t set axial_tilt to value of'
                             + ' %s physical type' %
                             value.unit.physical_type)
        self._set_bounded_property('axial_tilt', value.to(u.deg))

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
    def retrograde(self) -> bool:
        """the planetary rotation retrograde property"""
        return self._retrograde

    @retrograde.setter
    def retrograde(self, value):
        if not isinstance(value, bool):
            raise ValueError('expected boolean type value')
        self._retrograde = value

    @property
    def rotation(self) -> u.Quantity:
        """rotation in standard hours"""
        return self._get_bounded_property('rotation') * u.h

    @property
    def rotation_bounds(self) -> bounds.QuantityBounds:
        """rotation bounds in hours"""
        """return bounds.QuantityBounds(min(self._rotation_modifiers[self.size],
                                         16) * u.h,
                                     self._orbit.period.to(u.h))"""
        return bounds.QuantityBounds(0 * u.h, self._orbit.period.to(u.h))

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
    def solar_day(self) -> u.Quantity:
        """solar day in standard hours"""
        rotation = -self.rotation if self.retrograde else self.rotation
        return abs((self._orbit.period.to(u.h).value * rotation.value) /
                   (self._orbit.period.to(u.h).value - rotation.value)
                   if rotation != self._orbit.period else np.inf) * u.h

    @property
    def tidal_effect(self) -> bool:
        """the total tidal effect property"""
        # computing the primary star tidal force
        tidal_force = ((self._orbit._parent_body.mass.value *
                        self.diameter.value * .46) /
                       self._orbit.radius.value ** 3)
        if hasattr(self, '_moons'):
            # adding the sum of the moons tidal effects
            tidal_force += sum([(2.23 * 10 ** 6 * moon.mass.value *
                                 self.diameter.value) /
                                moon._orbit.radius.to(D_earth).value ** 3
                                for moon in self._moons])
        return round(tidal_force *
                     self._orbit._parent_body._star_system.age.value /
                     self.mass.value)

    @property
    def tide_locked(self) -> bool:
        """tide locked readonly property"""
        return self.rotation == self._orbit.period

    @property
    def moons(self):
        """the world moons"""
        return (len(self._moons) if hasattr(self, '_moons') else 0 +
                self._n_moonlets if hasattr(self, 'n_moonlets') else 0)
