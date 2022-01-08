# -*- coding: utf-8 -*-

from .world import World
from .model import bounds, RandomizableModel
from .random import roll3d6

import numpy as np

from astropy import units as u


class AsteroidBelt(RandomizableModel, World):
    """The asteroid belt world model"""
    _designation = 'Asteroid Belt'

    _precedence = ['resource', 'temperature']
    _temperature_bounds = bounds.QuantityBounds(140 * u.K, 500 * u.K)
    _absorption = .97
    _resource_bounds = bounds.ValueBounds(World.Resource.WORTHLESS,
                                          World.Resource.MOTHERLODE)

    def random_resource(self) -> None:
        """sum of a 3d roll times over Resource Value Table"""
        resource_value_table = {4: World.Resource.WORTHLESS,
                                5: World.Resource.VERY_SCANT,
                                6: World.Resource.SCANT,
                                8: World.Resource.VERY_POOR,
                                10: World.Resource.POOR,
                                12: World.Resource.AVERAGE,
                                14: World.Resource.ABUNDANT,
                                16: World.Resource.VERY_ABUNDANT,
                                17: World.Resource.RICH,
                                18: World.Resource.VERY_RICH}
        roll = roll3d6()
        filtered = list(filter(lambda x: roll >= x[0],
                               resource_value_table.items()))
        self.resource = (filtered[-1][1] if len(filtered) > 0
                         else World.Resource.MOTHERLODE)

    @property
    def blackbody_correction(self) -> float:
        """the correction applied on temperature"""
        return self._absorption

    @property
    def habitability(self) -> int:
        """the habitability score"""
        return 0

    def __init__(self, orbit=None):

        self._orbit = orbit

        if orbit:
            if not orbit._body:
                orbit._body = self
            world = self
            world.__class__ = inplace(type(self))

        self.randomize()


def inplace(world):

    class InplaceAsteroidBelt(world):
        """the orbiting asteroidbelt extended model"""
        _precedence = [p for p in world._precedence
                       if p != 'temperature']

        @property
        def blackbody_temperature(self) -> u.Quantity:
            """blackbody temperature in K from orbit"""
            return (278 * np.power(self._orbit._parent_body.luminosity.value,
                                   (1 / 4)) /
                    np.sqrt(self._orbit.radius.value)) * u.K

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

    return InplaceAsteroidBelt
