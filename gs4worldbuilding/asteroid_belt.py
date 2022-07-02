from functools import wraps
from typing import Optional

import numpy as np
from astropy import units as u
from astropy.units import Quantity

from gs4worldbuilding.celestial_object import CelestialObject
from gs4worldbuilding.world import World, Resource
from gs4worldbuilding.model.bounds import QuantityBounds, EnumBounds
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.orbit import Orbit


class AsteroidBelt(World, CelestialObject):
    '''The asteroid belt world model'''
    _precedence = ['resource', 'temperature']
    _temperature_bounds = QuantityBounds(140 * u.K, 500 * u.K)
    _absorption = .97
    _resource_bounds = EnumBounds(Resource.WORTHLESS, Resource.MOTHERLODE)

    def random_resource(self) -> Resource:
        '''sum of a 3d roll times over Resource Value Table'''
        table = {4: Resource.WORTHLESS,
                 5: Resource.VERY_SCANT,
                 6: Resource.SCANT,
                 8: Resource.VERY_POOR,
                 10: Resource.POOR,
                 12: Resource.AVERAGE,
                 14: Resource.ABUNDANT,
                 16: Resource.VERY_ABUNDANT,
                 17: Resource.RICH,
                 18: Resource.VERY_RICH}
        roll = RandomGenerator().roll3d6()
        filtered = list(filter(lambda x: roll < x, table.keys()))
        return (table[filtered[0]] if len(filtered) > 0 else
                Resource.MOTHERLODE)

    @property
    def blackbody_correction(self) -> float:
        '''the correction applied on temperature'''
        return self.absorption

    @property
    def habitability(self) -> int:
        '''the habitability score'''
        return 0

    @property
    def mass(self) -> Quantity['u.M_earth']:
        '''the asteroid belt aggregated map'''
        # TODO: implement
        raise NotImplementedError()

    def randomize(self) -> None:
        self.resource = self.random_resource()
        self.temperature = self.random_temperature()

    def __init__(self, orbit: Optional[Orbit] = None):
        self._orbit = orbit
        self.resource = self.random_resource()
        self.temperature = self.random_temperature()


def make_inplace(world_type):
    '''inplace decorator for asteroids'''

    @wraps(world_type, updated=())
    class InplaceAsteroidBelt(world_type):
        '''the orbiting asteroidbelt extended model'''
        _precedence = [p for p in world_type._precedence
                       if p != 'temperature']

        @property
        def blackbody_temperature(self) -> Quantity[u.K]:
            '''blackbody temperature in K from orbit'''
            return (278 * np.power(self.orbit.parent_star.luminosity.value,
                                   (1 / 4)) /
                    np.sqrt(self._orbit.radius.value)) * u.K

        @property
        def temperature(self) -> Quantity[u.K]:
            '''average temperature in K'''
            return (self.blackbody_temperature.value *
                    self.blackbody_correction) * u.K

        @temperature.setter
        def temperature(self, _) -> None:
            raise AttributeError("can't set overriden attribute")

        @property
        def orbit(self) -> Orbit:
            '''the world orbit around its parent body'''
            return self._orbit

    return InplaceAsteroidBelt
