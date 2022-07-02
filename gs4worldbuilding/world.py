from enum import IntEnum, unique
from abc import ABC, abstractmethod

from ordered_enum import ValueOrderedEnum
from astropy import units as u
from astropy.units import Quantity

from .random import RandomGenerator
from .model import RandomizableModel
from .model.bounds import QuantityBounds, EnumBounds


@unique
class Climate(Quantity[u.K], ValueOrderedEnum):
    '''Climate Enum from world Climate Table with temperature threshold in K'''
    FROZEN = 0 * u.K
    VERY_COLD = 244 * u.K
    COLD = 255 * u.K
    CHILLY = 266 * u.K
    COOL = 278 * u.K
    NORMAL = 289 * u.K
    WARM = 300 * u.K
    TROPICAL = 311 * u.K
    HOT = 322 * u.K
    VERY_HOT = 333 * u.K
    INFERNAL = 344 * u.K


class Resource(IntEnum, ValueOrderedEnum):
    '''Ressource Enum from Ressource Value Table'''
    WORTHLESS = -5
    VERY_SCANT = -4
    SCANT = -3
    VERY_POOR = -2
    POOR = -1
    AVERAGE = 0
    ABUNDANT = 1
    VERY_ABUNDANT = 2
    RICH = 3
    VERY_RICH = 4
    MOTHERLODE = 5


class World(RandomizableModel, ABC):
    '''The gurps world abstract class'''
    _absorption: float
    _resource_bounds: EnumBounds
    _temperature_bounds: QuantityBounds

    @abstractmethod
    def random_resource(self) -> Resource:
        '''random resource value'''

    def random_temperature(self) -> Quantity[u.K]:
        '''sum of a 3d6-3 roll in range'''
        tmin = self.temperature_bounds.lower.value
        tmax = self.temperature_bounds.upper.value
        roll = RandomGenerator().roll3d6(-3, continuous=True)
        return (tmin + roll / 15 * (tmax - tmin)) * u.K

    @property
    def absorption(self) -> float:
        '''absorption'''
        return self._absorption

    @property
    def resource(self) -> Resource:
        '''resource value on Resource Value Table'''
        return self._get_bounded_property('resource')

    @property
    def resource_bounds(self) -> EnumBounds:
        '''resource range class variable'''
        return self._resource_bounds

    @resource.setter
    def resource(self, value: Resource):
        if not isinstance(value, Resource):
            raise ValueError(f'resource value type has to be {Resource}')
        self._set_bounded_property('resource', value)

    @property
    def temperature(self) -> Quantity[u.K]:
        '''average temperature in K'''
        return self._get_bounded_property('temperature')

    @property
    def temperature_bounds(self) -> QuantityBounds:
        '''temperature range static class variable in K'''
        return self._temperature_bounds

    @temperature.setter
    def temperature(self, value: Quantity['temperature']):
        if not isinstance(value, Quantity):
            raise ValueError('expected quantity type value')
        if 'temperature' not in value.unit.physical_type:
            raise ValueError('can\'t set temperature to value of'
                             + f' {value.unit.physical_type} physical type')
        self._set_bounded_property('temperature', value.to(u.K))

    @property
    @abstractmethod
    def blackbody_correction(self) -> float:
        '''the correction applied on temperature'''
        raise NotImplementedError('World subclasses should implement ' +
                                  "the 'blackbody_correction' property")

    @property
    def blackbody_temperature(self) -> Quantity[u.K]:
        '''blackbody temperature in K'''
        return self.temperature / self.blackbody_correction

    @property
    def climate(self) -> Climate:
        '''climate implied by temperature match over World Climate Table'''
        return list(filter(lambda x: self.temperature >= x, Climate))[-1]

    @property
    @abstractmethod
    def habitability(self) -> int:
        '''the habitability score'''
        raise NotImplementedError('World subclasses should implement ' +
                                  "the 'habitability' property")

    @property
    def affinity(self) -> int:
        '''the affinity score'''
        return self.resource + self.habitability

    def randomize(self) -> None:
        self.resource = self.random_resource()
        self.temperature = self.random_temperature()

    def __eq__(self, other: 'World') -> bool:
        return (isinstance(other, type(self)) and
                self.absorption == other.absorption and
                self.affinity == other.affinity and
                self.blackbody_correction == other.blackbody_correction and
                self.blackbody_temperature == other.blackbody_temperature and
                self.climate == other.climate and
                self.habitability == other.habitability and
                self.resource == other.resource and
                self.resource_bounds == other.resource_bounds and
                self.temperature == other.temperature and
                self.temperature_bounds == other.temperature_bounds)
