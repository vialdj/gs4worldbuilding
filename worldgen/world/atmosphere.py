from .utils import Range
from enum import Enum

import numpy as np


class Atmosphere(object):
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
    def marginal(self):
        """the marginal modifiers"""
        return (self._marginal if hasattr(self, '_marginal') else None)

    def __init__(self, world):
        self._world = world

    def __iter__(self):
        """yield property names and values"""
        for prop in list(filter(lambda x: hasattr(type(self), x)
                         and isinstance(getattr(type(self), x), property),
                         dir(self))):
            yield prop, getattr(self, prop)

    def __str__(self):
        return ('{{class: {}, {}}}'.format(self.__class__.__name__,
                                           ', '.join(['{}: {!s}'.format(prop, value)
                                                     for prop, value in self])))


class MarginalAtmosphere(Atmosphere):
    def __init__(self, atmosphere):
        self = atmosphere


class ChlorineOrFluorine(MarginalAtmosphere):
    _toxicity = Range(Atmosphere.Toxicity.HIGH, Atmosphere.Toxicity.LETHAL)
    _corrosive = Range(False, True)


class HighCarbonDioxide(MarginalAtmosphere):
    _toxicity = Range(None, Atmosphere.Toxicity.MILD)
    _pressure_category = Atmosphere.Pressure.VERY_DENSE


class HighOxygen(MarginalAtmosphere):
    _toxicity = Range(None, Atmosphere.Toxicity.MILD)

    @property
    def pressure_category(self):
        idx = list(Atmosphere.Pressure).index(super().pressure_category())
        idx = min(idx + 1, len(Atmosphere.Pressure) - 1)
        return list(Atmosphere.Pressure)[idx]


class InertGases(MarginalAtmosphere):
    pass


class LowOxygen(MarginalAtmosphere):

    @property
    def pressure_category(self):
        idx = list(Atmosphere.Pressure).index(super().pressure_category())
        pressure_id = max(idx - 1, 0)
        return list(Atmosphere.Pressure)[idx]


class NitrogenCompounds(MarginalAtmosphere):
    _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.HIGH)


class SulfurCompounds(MarginalAtmosphere):
    _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.HIGH)


class OrganicToxins(MarginalAtmosphere):
    _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.LETHAL)


class Pollutants(MarginalAtmosphere):
    _toxicity = Atmosphere.Toxicity.MILD


marginal_distribution = {
    ChlorineOrFluorine: 0.01852,
    HighCarbonDioxide: 0.07408,
    HighOxygen: 0.06944,
    InertGases: 0.21296,
    LowOxygen: 0.25,
    NitrogenCompounds: 0.21296,
    SulfurCompounds: 0.06944,
    OrganicToxins: 0.07408,
    Pollutants: 0.01852
}