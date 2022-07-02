import numpy as np
from astropy import units as u
from astropy.units import Quantity

from gs4worldbuilding.model import RandomizableModel
from gs4worldbuilding.model.bounds import ScalarBounds
from gs4worldbuilding.celestial_object import CelestialObject
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.star import Star


class Orbit(RandomizableModel):
    '''the orbit model'''

    _eccentricity_bounds = ScalarBounds(0, .8)

    def random_ascending_lon(self) -> Quantity['angle']:
        '''draw from a uniform distribution between -180 and 180'''
        return RandomGenerator().rng.uniform(-180, 180) * u.deg

    def random_eccentricity(self) -> float:
        '''sum of a 3d6 roll over Planetary Orbital Eccentricity Table with
        modifiers if any'''
        return (RandomGenerator()
                .truncnorm_draw(0, .8, .20295, 15273767544387992))

    def random_inclination(self) -> Quantity['angle']:
        '''draw from a Rayleigh distribution with a mode of 2'''
        return RandomGenerator().rng.rayleigh(2) * u.deg

    def random_epoch_mean_anomaly(self) -> Quantity['angle']:
        '''draw from a uniform distribution between 0 and 360'''
        return RandomGenerator().rng.uniform(0, 360) * u.deg

    def random_periapsis_arg(self) -> Quantity['angle']:
        '''draw from a uniform distribution between 0 and 360'''
        return RandomGenerator().rng.uniform(0, 360) * u.deg

    @property
    def body(self) -> CelestialObject:
        '''the orbiting body'''
        return self._body

    @property
    def parent_body(self) -> CelestialObject:
        '''the attracting body'''
        return self._parent_body

    @property
    def parent_star(self) -> Star:
        '''the parent star to the object'''
        node = None
        while not isinstance(node, Star):
            node = self.parent_body
        return node

    @property
    def radius(self) -> u.Quantity:
        '''The average orbital radius to the parent body in AU'''
        return self._radius

    @radius.setter
    def radius(self, value: Quantity['length']) -> None:
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'length' not in value.unit.physical_type:
            raise ValueError("can't set radius to value of" +
                             f'{value.unit.physical_type} physical type')
        self._radius = value.to(u.au)

    @property
    def eccentricity(self) -> float:
        '''the orbital orbit eccentricity'''
        return self._get_bounded_property('eccentricity')

    @property
    def eccentricity_bounds(self) -> ScalarBounds:
        '''value range for eccentricity'''
        return self._eccentricity_bounds

    @eccentricity.setter
    def eccentricity(self, value: float) -> None:
        self._set_bounded_property('eccentricity', value)

    @property
    def epoch_mean_anomaly(self) -> Quantity['u.deg']:
        '''the mean anomaly at epoch M0 in degrees'''
        return self._epoch_mean_anomaly

    @epoch_mean_anomaly.setter
    def epoch_mean_anomaly(self, value: Quantity['angle']) -> None:
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError("can't set mean anomaly at epoch to value of " +
                             f' {value.unit.physical_type} physical type')
        self._epoch_mean_anomaly = value.to(u.deg)

    @property
    def inclination(self) -> Quantity[u.deg]:
        '''the orbital inclination in degrees'''
        return self._inclination

    @inclination.setter
    def inclination(self, value: Quantity['angle']) -> None:
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError("can't set inclination to value of " +
                             f' {value.unit.physical_type} physical type')
        self._inclination = value.to(u.deg)

    @property
    def ascending_lon(self) -> Quantity[u.deg]:
        '''the longitude of the ascending node Ω in degrees'''
        return self._ascending_lon

    @ascending_lon.setter
    def ascending_lon(self, value: Quantity) -> None:
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError("can't set longitude of ascending node to value" +
                             f' of {value.unit.physical_type} physical type')
        self._ascending_lon = value.to(u.deg)

    @property
    def min_separation(self) -> Quantity[u.au]:
        '''the minimum separation in AU'''
        return ((1 - self.eccentricity) * self.radius.value) * u.au

    @property
    def max_separation(self) -> Quantity[u.au]:
        '''the maximum separation in AU'''
        return ((1 + self.eccentricity) * self.radius.value) * u.au

    @property
    def periapsis_arg(self) -> Quantity[u.deg]:
        '''the argument of periapsis ω in degrees'''
        return self._periapsis_arg

    @periapsis_arg.setter
    def periapsis_arg(self, value: Quantity['angle']) -> None:
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError("can't set argument of periapsis to value of" +
                             f' {value.unit.physical_type} physical type')
        self._periapsis_arg = value.to(u.deg)

    @property
    def period(self) -> Quantity[u.a]:
        '''the orbital period in earth years'''
        return np.sqrt(self.radius.value ** 3 /
                       self._parent_body.mass.value) * u.a

    def randomize(self):
        self.eccentricity = self.random_eccentricity()
        self.inclination = self.random_inclination()
        self.ascending_lon = self.random_ascending_lon()
        self.periapsis_arg = self.random_periapsis_arg()
        self.epoch_mean_anomaly = self.random_epoch_mean_anomaly()

    def __init__(self, parent_body: CelestialObject,
                 radius: u.Quantity, body: CelestialObject):
        self._body = body
        self._parent_body = parent_body
        self.radius = radius
        self.eccentricity = self.random_eccentricity()
        self.inclination = self.random_inclination()
        self.ascending_lon = self.random_ascending_lon()
        self.periapsis_arg = self.random_periapsis_arg()
        self.epoch_mean_anomaly = self.random_epoch_mean_anomaly()
