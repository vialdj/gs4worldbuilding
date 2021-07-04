from .. import Model
from enum import Enum

import numpy as np


class Atmosphere(Model):
    """the Atmosphere Model"""

    class Pressure(float, Enum):
        """class Pressure Enum from Atmospheric Pressure Categories Table"""
        TRACE = .0
        VERY_THIN = .01
        THIN = .51
        STANDARD = .81
        DENSE = 1.21
        VERY_DENSE = 1.51
        SUPER_DENSE = 10

    class Toxicity(Enum):
        """class Toxicity Enum from Toxicity Rules categories"""
        MILD = 0
        HIGH = 1
        LETHAL = 2

    @property
    def composition(self):
        """key properties of the atmosphere"""
        return (type(self)._composition
                if hasattr(type(self), '_composition') else None)

    @property
    def toxicity(self):
        """toxicity of the atmosphere"""
        return (self._toxicity
                if hasattr(self, '_toxicity') else None)

    @property
    def suffocating(self):
        """is the atmosphere suffocating"""
        return (type(self)._suffocating
                if hasattr(type(self), '_suffocating') else False)

    @property
    def corrosive(self):
        """is the atmosphere corrosive"""
        return (type(self)._corrosive
                if hasattr(type(self), '_corrosive') else False)

    @property
    def pressure(self):
        """atmospheric pressure in atm⊕"""
        return (self._world.volatile_mass * self._world.pressure_factor
                * self._world.gravity)

    @property
    def pressure_category(self):
        """atmospheric pressure implied by pressure match over
        Atmospheric Pressure Categories Table"""
        return (list(filter(lambda x: self.pressure >= x.value,
                            self.Pressure))[-1]
                if not np.isnan(self.pressure) else None)

    @property
    def breathable(self):
        """is the atmosphere breathable"""
        return not (self.toxicity is not None or self.suffocating
                    or self.corrosive)

    def __init__(self, world):
        self._world = world
