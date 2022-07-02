from abc import ABC

import numpy as np
from astropy import units as u
from astropy.units import Quantity

from gs4worldbuilding.celestial_object import CelestialObject
from gs4worldbuilding.model.bounds import QuantityBounds
from gs4worldbuilding.model import RandomizableModel
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.units import D_earth
from gs4worldbuilding.orbit import Orbit


class PlanetaryOrbit(Orbit):
    '''the specialization for planetary orbits'''
    @property
    def period(self) -> u.Quantity:
        '''the orbital period in earth years'''
        return np.sqrt(self.radius.value ** 3 /
                       (self._parent_body.mass.value +
                        self._body.mass.to(u.M_sun).value)) * u.a


class Planet(RandomizableModel, CelestialObject, ABC):
    '''the Planet given orbital parameters as an abstract class'''
    _rotation: float

    def random_axial_tilt(self) -> Quantity[u.deg]:
        '''Roll 3d over Axial Tilt Tables to define axial tilt'''
        tilt_roll = RandomGenerator().roll2d6(-2, continuous=True)
        table_roll = RandomGenerator().roll3d6()
        if table_roll < 17:
            table = {6: 0, 9: 10, 12: 20, 14: 30, 16: 40}
        else:
            table_roll = RandomGenerator().roll1d6()
            table = {2: 50, 4: 60, 5: 70, 6: 80}
        return (table[list(filter(lambda x: table_roll <= x,
                table.keys()))[0]] + tilt_roll) * u.deg

    def random_resonant(self) -> bool:
        '''Roll 3d to define resonant property'''
        resonant = False
        rotation = self.rotation_bounds.scale(self._rotation)
        if ((rotation * u.h == self._orbit.period or
             self.tidal_effect >= 50) and self._orbit.eccentricity >= .1):
            resonant = True if RandomGenerator().roll3d6() >= 12 else False
        return resonant

    def random_retrograde(self) -> bool:
        '''Roll 3d to define retrograde property'''
        return True if RandomGenerator().roll3d6() > 13 else False

    def random_rotation(self) -> None:
        '''Roll over Rotation Table and Special Rotation Table if applicable'''
        initial_roll = RandomGenerator().roll3d6(continuous=True)
        if (initial_roll > 16 or initial_roll +
                self._rotation_modifiers[self.size] > 36):
            special_roll = int(RandomGenerator().roll2d6())
            rotation = ({7: 48, 8: 120, 9: 240, 10: 480, 11: 1200,
                         12: 2400}[special_roll] * RandomGenerator().roll1d6(continuous=True)
                        if special_roll > 6 else initial_roll) * u.h
        else:
            rotation = (initial_roll + self.tidal_effect +
                        self._rotation_modifiers[self.size]) * u.h
        return min(rotation, self.rotation_bounds.upper)

    @property
    def axial_tilt(self) -> Quantity[u.deg]:
        '''the planet axial tilt in degrees, > 90 if the rotation has the
retrograde property'''
        tilt = self._get_bounded_property('axial_tilt')
        return (180 - tilt if self.retrograde else tilt) * u.deg

    @property
    def axial_tilt_bounds(self) -> QuantityBounds:
        '''axial tilt bounds in degrees'''
        return QuantityBounds(0 * u.deg, 90 * u.deg)

    @axial_tilt.setter
    def axial_tilt(self, value: Quantity['angle']) -> None:
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError("can't set axial_tilt to value of" +
                             f' {value.unit.physical_type} physical type')
        self._set_bounded_property('axial_tilt', value.to(u.deg))

    @property
    def blackbody_temperature(self) -> Quantity[u.K]:
        '''blackbody temperature in K from orbit'''
        return (278 * np.power(self._orbit.parent_star.luminosity.value,
                               (1 / 4)) /
                np.sqrt(self._orbit.radius.value)) * u.K

    @property
    def moons(self) -> int:
        '''the world major moons'''
        return self._n_moons

    @property
    def moonlets(self) -> int:
        '''the world moonlets'''
        return self._n_moonlets

    @property
    def resonant(self) -> bool:
        '''either the planet display a resonant rotation'''
        return self._get_bounded_property('resonant')

    @property
    def resonant_set(self) -> set:
        '''the boolean set for the resonant property'''
        rotation = self.rotation_bounds.scale(self._rotation)
        return set([False, (rotation * u.h == self._orbit.period or
                    self.tidal_effect >= 50) and
                    self._orbit.eccentricity >= .1])

    @resonant.setter
    def resonant(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError('expected boolean type value')
        self._set_bounded_property('resonant', value)

    @property
    def retrograde(self) -> bool:
        '''the planetary rotation retrograde property'''
        return self._retrograde

    @retrograde.setter
    def retrograde(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError('expected boolean type value')
        self._retrograde = value

    @property
    def rotation(self) -> Quantity[u.h]:
        '''rotation in standard hours'''
        if self.resonant:
            return (2 * self._orbit.period.to(u.h)) / 3
        return (self._orbit.period.to(u.h) if self.tide_locked
                else self._get_bounded_property('rotation'))

    @property
    def rotation_bounds(self) -> QuantityBounds:
        '''rotation bounds in hours'''
        '''return QuantityBounds(min(self._rotation_modifiers[self.size],
                                         16) * u.h,
                                     self._orbit.period.to(u.h))'''
        return QuantityBounds(0 * u.h, self._orbit.period.to(u.h))

    @rotation.setter
    def rotation(self, value: Quantity['time']):
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'time' not in value.unit.physical_type:
            raise ValueError('can\'t set rotation to value of'
                             + ' %s physical type' %
                             value.unit.physical_type)
        self._set_bounded_property('rotation', value.to(u.h))

    @property
    def solar_day(self) -> Quantity[u.h]:
        '''solar day in standard hours'''
        rotation = -self.rotation if self.retrograde else self.rotation
        return abs((self._orbit.period.to(u.h).value * rotation.value) /
                   (self._orbit.period.to(u.h).value - rotation.value)
                   if rotation != self._orbit.period else np.inf) * u.h

    @property
    def tidal_effect(self) -> int:
        '''the total tidal effect property'''
        # computing the primary star tidal force
        tidal_force = ((self._orbit.parent_body.mass.value *
                        self.diameter.value * .46) /
                       self._orbit.radius.value ** 3)
        if hasattr(self, '_moons'):
            # adding the sum of the moons tidal effects
            tidal_force += sum([(2230000 * moon.mass.value *
                                 self.diameter.value) /
                                moon._orbit.radius.to(D_earth).value ** 3
                                for moon in self._moons])
        return round(tidal_force *
                     self._orbit.parent_star.age.value /
                     self.mass.value)

    @property
    def tide_locked(self) -> bool:
        '''tide locked readonly property'''
        rotation = self.rotation_bounds.scale(self._rotation)
        return ((rotation * u.h == self._orbit.period or
                self.tidal_effect >= 50) and not self.resonant)

    def __init__(self, orbit: PlanetaryOrbit):
        self._orbit = orbit
