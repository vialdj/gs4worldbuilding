import enum
from typing import Optional, List, Union

import numpy as np
from astropy import units as u
from astropy.units import cds
from ordered_enum import ValueOrderedEnum

from .. import model
from ..model.bounds import ValueBounds


@enum.unique
class Pressure(u.Quantity, ValueOrderedEnum):
    """class Pressure Enum from Atmospheric Pressure Categories Table"""
    TRACE = .0 * cds.atm
    VERY_THIN = .01 * cds.atm
    THIN = .51 * cds.atm
    STANDARD = .81 * cds.atm
    DENSE = 1.21 * cds.atm
    VERY_DENSE = 1.51 * cds.atm
    SUPER_DENSE = 10 * cds.atm


@enum.unique
class Toxicity(ValueOrderedEnum):
    """class Toxicity Enum from Toxicity Rules categories"""
    NONE = 0
    MILD = 1
    HIGH = 2
    LETHAL = 3


class Atmosphere(model.Model):
    """the Atmosphere Model"""
    _toxicity: Optional[Toxicity] = None
    _corrosive: bool = False
    _suffocating: bool = False
    _composition: Optional[List[str]] = None

    @property
    def composition(self) -> Optional[List[str]]:
        """key properties of the atmosphere"""
        return self._composition

    @property
    def toxicity(self) -> Optional[Union[ValueBounds, Toxicity]]:
        """toxicity of the atmosphere"""
        return self._toxicity

    @property
    def suffocating(self) -> bool:
        """is the atmosphere suffocating"""
        return self._suffocating

    @property
    def corrosive(self) -> bool:
        """is the atmosphere corrosive"""
        return self._corrosive

    @property
    def pressure(self) -> u.Quantity:
        """atmospheric pressure in atm🜨"""
        return (self._world.volatile_mass * self._world.pressure_factor
                * self._world.gravity.value) * cds.atm

    @property
    def pressure_category(self) -> Optional[Pressure]:
        """atmospheric pressure implied by pressure match over
        Atmospheric Pressure Categories Table"""
        categories = sorted(list(Pressure), key=lambda x: x.value)
        return (list(filter(lambda x: self.pressure >= x, categories))[-1]
                if not np.isnan(self.pressure) else None)

    @property
    def breathable(self):
        """is the atmosphere breathable"""
        return not (self.suffocating
                    or self.corrosive)

    def __init__(self, world):
        self._world = world
