from .atmosphere import Atmosphere
from .utils import Range

import random
import copy


class Marginal():

    @property
    def base(self):
        """the base atmosphere"""
        return (self._base if hasattr(self, '_base') else None)


def chlorine_or_fluorine(atmosphere):

    class ChlorineOrFluorine(atmosphere, Marginal):
        _toxicity = Range(Atmosphere.Toxicity.HIGH, Atmosphere.Toxicity.LETHAL)
        _corrosive = Range(False, True)

    return ChlorineOrFluorine


def high_carbon_dioxide(atmosphere):

    class HighCarbonDioxide(atmosphere, Marginal):
        _toxicity = Range(None, Atmosphere.Toxicity.MILD)
        _pressure_category = Atmosphere.Pressure.VERY_DENSE

    return HighCarbonDioxide


def high_oxygen(atmosphere):

    class HighOxygen(atmosphere, Marginal):

        @property
        def pressure_category(self):
            idx = list(Atmosphere.Pressure).index(super().pressure_category)
            idx = min(idx + 1, len(Atmosphere.Pressure) - 1)
            return list(Atmosphere.Pressure)[idx]

    return HighOxygen


def inert_gases(atmosphere):

    class InertGases(atmosphere, Marginal):
        pass

    return InertGases


def low_oxygen(atmosphere):

    class LowOxygen(atmosphere, Marginal):

        @property
        def pressure_category(self):
            idx = list(Atmosphere.Pressure).index(super().pressure_category)
            idx = max(idx - 1, 0)
            return list(Atmosphere.Pressure)[idx]

    return LowOxygen


def nitrogen_compounds(atmosphere):

    class NitrogenCompounds(atmosphere, Marginal):
        _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.HIGH)

    return NitrogenCompounds


def sulfur_compounds(atmosphere):

    class SulfurCompounds(atmosphere, Marginal):
        _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.HIGH)

    return SulfurCompounds


def organic_toxins(atmosphere):

    class OrganicToxins(atmosphere, Marginal):
        _toxicity = Range(Atmosphere.Toxicity.MILD, Atmosphere.Toxicity.LETHAL)

    return OrganicToxins


def pollutants(atmosphere):

    class Pollutants(atmosphere, Marginal):
        _toxicity = Atmosphere.Toxicity.MILD

    return Pollutants


class MarginalCandidate:

    def make_marginal(self, marginal_type=None):

        if issubclass(type(self), Marginal):
            self.remove_marginal()

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

        base = copy.copy(self)
        marginal = self
        marginal.__class__ = marginal_type(type(self))
        marginal._base = base

    def remove_marginal(self):

        if issubclass(type(self), Marginal):
            base_type = type(self.base)
            atmosphere = self
            atmosphere.__class__ = base_type
