import enum
from abc import ABC, abstractmethod

from ordered_enum import ValueOrderedEnum
from astropy import units as u

from .random import RandomGenerator
from .model import bounds


class World(ABC):
    """The gurps world abstract class"""

    @enum.unique
    class Climate(u.Quantity, ValueOrderedEnum):
        """class Climate Enum from world Climate Table with temperature
        threshold in K"""
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

    class Resource(int, ValueOrderedEnum):
        """class Ressource Enum from Ressource Value Table"""
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

    @abstractmethod
    def random_resource(self) -> None:
        pass

    def random_temperature(self) -> None:
        """sum of a 3d6-3 roll in range"""
        tmin = self.temperature_bounds.lower.value
        tmax = self.temperature_bounds.upper.value
        roll = RandomGenerator().roll3d6(-3, continuous=True)
        self.temperature = (tmin + roll / 15 * (tmax - tmin)) * u.K

    @property
    def absorption(self) -> float:
        """absorption"""
        return self._absorption

    @property
    def resource(self) -> Resource:
        """resource value on Resource Value Table"""
        return self._get_bounded_property('resource')

    @property
    def resource_bounds(self) -> bounds.ValueBounds:
        """resource range class variable"""
        return self._resource_bounds

    @resource.setter
    def resource(self, value: Resource):
        if not isinstance(value, self.Resource):
            raise ValueError(f'resource value type has to be {self.Resource}')
        self._set_bounded_property('resource', value)

    @property
    def temperature(self) -> u.Quantity:
        """average temperature in K"""
        return self._get_bounded_property('temperature')

    @property
    def temperature_bounds(self) -> bounds.QuantityBounds:
        """temperature range static class variable in K"""
        return self._temperature_bounds

    @temperature.setter
    def temperature(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'temperature' not in value.unit.physical_type:
            raise ValueError('can\'t set temperature to value of'
                             + f' {value.unit.physical_type} physical type')
        self._set_bounded_property('temperature', value.to(u.K))

    @property
    @abstractmethod
    def blackbody_correction(self) -> float:
        """the correction applied on temperature"""
        raise NotImplementedError('World subclasses should implement ' +
                                  "the 'blackbody_correction' property")

    @property
    def blackbody_temperature(self) -> u.Quantity:
        """blackbody temperature in K"""
        return self.temperature / self.blackbody_correction

    @property
    def climate(self) -> Climate:
        """climate implied by temperature match over World Climate Table"""
        return list(filter(lambda x: self.temperature >= x, self.Climate))[-1]

    @property
    @abstractmethod
    def habitability(self) -> int:
        """the habitability score"""
        raise NotImplementedError('World subclasses should implement ' +
                                  "the 'habitability' property")

    @property
    def affinity(self) -> int:
        """the affinity score"""
        return self.resource + self.habitability
