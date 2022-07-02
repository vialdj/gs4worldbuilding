from enum import IntEnum, unique
from typing import List

from ordered_enum import ValueOrderedEnum
from astropy.units import Quantity, cds

from gs4worldbuilding.model import Model


@unique
class Pressure(Quantity[cds.atm], ValueOrderedEnum):
    '''class Pressure Enum from Atmospheric Pressure Categories Table'''
    TRACE = .0 * cds.atm
    VERY_THIN = .01 * cds.atm
    THIN = .51 * cds.atm
    STANDARD = .81 * cds.atm
    DENSE = 1.21 * cds.atm
    VERY_DENSE = 1.51 * cds.atm
    SUPER_DENSE = 10 * cds.atm


@unique
class Toxicity(IntEnum, ValueOrderedEnum):
    '''class Toxicity Enum from Toxicity Rules categories'''
    NONE = 0
    MILD = 1
    HIGH = 2
    LETHAL = 3


class Atmosphere(Model):
    '''the Atmosphere Model'''
    _toxicity = Toxicity.NONE
    _corrosive = False
    _suffocating = False
    _composition: List[str]

    @property
    def composition(self) -> List[str]:
        '''key properties of the atmosphere'''
        return self._composition

    @property
    def toxicity(self) -> Toxicity:
        '''toxicity of the atmosphere'''
        return self._toxicity

    @property
    def suffocating(self) -> bool:
        '''is the atmosphere suffocating'''
        return self._suffocating

    @property
    def corrosive(self) -> bool:
        '''is the atmosphere corrosive'''
        return self._corrosive

    @property
    def pressure(self) -> Quantity[cds.atm]:
        '''atmospheric pressure in atm🜨'''
        return (self._world.volatile_mass * self._world.pressure_factor
                * self._world.gravity.value) * cds.atm

    @property
    def pressure_category(self) -> Pressure:
        '''atmospheric pressure implied by pressure match over
        Atmospheric Pressure Categories Table'''
        categories = sorted(list(Pressure), key=lambda x: x.value)
        return list(filter(lambda x: self.pressure >= x, categories))[-1]

    @property
    def breathable(self) -> bool:
        '''is the atmosphere breathable'''
        return not (self.suffocating or self.corrosive)

    def __init__(self, world):
        self._world = world
