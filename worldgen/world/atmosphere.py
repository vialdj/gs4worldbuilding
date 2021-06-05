from scipy.stats.stats import _parse_kstest_args
from .utils import Range
from enum import Enum

import numpy as np
import random
import copy


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
    def breathable(self):
        """is the atmosphere breathable"""
        return not (self.toxicity is not None or self.suffocating
                    or self.corrosive)

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


class Marginal(Atmosphere):
    pass


def chlorine_or_fluorine(atmosphere):

    class ChlorineOrFluorine(atmosphere, Marginal):
        _toxicity = Range(Atmosphere.Toxicity.HIGH, Atmosphere.Toxicity.LETHAL)
        _corrosive = Range(False, True)

        def __init__(self, atmosphere):
            self = copy.deepcopy(atmosphere)

    return ChlorineOrFluorine


def high_carbon_dioxide(atmosphere):

    class HighCarbonDioxide(atmosphere, Marginal):
        _toxicity = Range(None, Atmosphere.Toxicity.MILD)
        _pressure_category = Atmosphere.Pressure.VERY_DENSE

        def __init__(self, atmosphere):
            self = copy.deepcopy(atmosphere)

    return HighCarbonDioxide


def high_oxygen(atmosphere):

    class HighOxygen(atmosphere, Marginal):

        @property
        def pressure_category(self):
            idx = list(Atmosphere.Pressure).index(super().pressure_category)
            idx = min(idx + 1, len(Atmosphere.Pressure) - 1)
            return list(Atmosphere.Pressure)[idx]

        def __init__(self, world):
            super(HighOxygen, self).__init__(world)

    return HighOxygen


def inert_gases(atmosphere):

    class InertGases(atmosphere, Marginal):

        def __init__(self, atmosphere):
            self = copy.deepcopy(atmosphere)

    return InertGases


def low_oxygen(atmosphere):

    class LowOxygen(atmosphere, Marginal):

        @property
        def pressure_category(self):
            idx = list(Atmosphere.Pressure).index(super().pressure_category)
            pressure_id = max(idx - 1, 0)
            return list(Atmosphere.Pressure)[idx]

        def __init__(self, atmosphere):
            self = copy.deepcopy(atmosphere)

    return LowOxygen


def nitrogen_compounds(atmosphere):

    class NitrogenCompounds(atmosphere, Marginal):
        _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.HIGH)

        def __init__(self, atmosphere):
            self = copy.deepcopy(atmosphere)

    return NitrogenCompounds


def sulfur_compounds(atmosphere):

    class SulfurCompounds(atmosphere, Marginal):
        _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.HIGH)

        def __init__(self, atmosphere):
            self = copy.deepcopy(atmosphere)

    return SulfurCompounds


def organic_toxins(atmosphere):

    class OrganicToxins(atmosphere, Marginal):
        _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.LETHAL)

        def __init__(self, atmosphere):
            self = copy.deepcopy(atmosphere)

    return OrganicToxins


def pollutants(atmosphere):

    class Pollutants(atmosphere, Marginal):
        _toxicity = Atmosphere.Toxicity.MILD

        def __init__(self, atmosphere):
            self = copy.deepcopy(atmosphere)

    return Pollutants


def make_marginal(atmosphere, marginal_type=None):
    marginal_distribution = {
        chlorine_or_fluorine: 0.01852,
        high_carbon_dioxide: 0.07408,
        high_oxygen: 0.06944,
        inert_gases: 0.21296,
        low_oxygen: 0.25,
        nitrogen_compounds: 0.21296,
        sulfur_compounds: 0.06944,
        organic_toxins: 0.07408,
        pollutants: 0.01852
    }

    if marginal_type is None:
        marginal_type = random.choices(list(marginal_distribution.keys()),
                                       weights=list(marginal_distribution
                                                    .values()))[0]
    marginal = atmosphere
    marginal.__class__ = marginal_type(type(atmosphere))
    return marginal
