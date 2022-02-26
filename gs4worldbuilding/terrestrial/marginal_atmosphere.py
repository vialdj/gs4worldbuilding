# -*- coding: utf-8 -*-

from .atmosphere import Atmosphere
from .. import model
from ..random import RandomGenerator

import copy


class Marginal():
    """the Marginal class to be inherited by concrete marginal modifiers"""

    @property
    def base(self):
        """the base atmosphere"""
        return (self._base if hasattr(self, '_base') else None)


def chlorine_or_fluorine(atmosphere):

    class ChlorineOrFluorine(atmosphere, Marginal):
        _toxicity = model.bounds.ValueBounds(
                        Atmosphere.Toxicity.HIGH,
                        Atmosphere.Toxicity.LETHAL
                    )
        _corrosive = model.bounds.ValueBounds(False, True)

    return ChlorineOrFluorine


def high_carbon_dioxide(atmosphere):

    class HighCarbonDioxide(atmosphere, Marginal):
        _toxicity = model.bounds.ValueBounds(
                        Atmosphere.Toxicity.NONE,
                        Atmosphere.Toxicity.MILD
                    )

        @property
        def pressure_category(self):
            return Atmosphere.Pressure.VERY_DENSE

    return HighCarbonDioxide


def high_oxygen(atmosphere):

    class HighOxygen(atmosphere, Marginal):
        _toxicity = model.bounds.ValueBounds(
                        Atmosphere.Toxicity.NONE,
                        Atmosphere.Toxicity.MILD
                    )

        @property
        def pressure_category(self):
            categories = sorted(list(Atmosphere.Pressure),
                                key=lambda x: x.value)
            idx = categories.index(super().pressure_category)
            idx = min(idx + 1, len(categories) - 1)
            return categories[idx]

    return HighOxygen


def inert_gases(atmosphere):

    class InertGases(atmosphere, Marginal):
        _toxicity = Atmosphere.Toxicity.NONE

    return InertGases


def low_oxygen(atmosphere):

    class LowOxygen(atmosphere, Marginal):

        @property
        def pressure_category(self):
            categories = sorted(list(Atmosphere.Pressure),
                                key=lambda x: x.value)
            idx = categories.index(super().pressure_category)
            idx = max(idx - 1, 0)
            return categories[idx]

    return LowOxygen


def nitrogen_compounds(atmosphere):

    class NitrogenCompounds(atmosphere, Marginal):
        _toxicity = model.bounds.ValueBounds(
                        Atmosphere.Toxicity.MILD,
                        Atmosphere.Toxicity.HIGH
                    )

    return NitrogenCompounds


def sulfur_compounds(atmosphere):

    class SulfurCompounds(atmosphere, Marginal):
        _toxicity = model.bounds.ValueBounds(
                        Atmosphere.Toxicity.MILD,
                        Atmosphere.Toxicity.HIGH
                    )

    return SulfurCompounds


def organic_toxins(atmosphere):

    class OrganicToxins(atmosphere, Marginal):
        _toxicity = model.bounds.ValueBounds(
                        Atmosphere.Toxicity.MILD,
                        Atmosphere.Toxicity.LETHAL
                    )

    return OrganicToxins


def pollutants(atmosphere):

    class Pollutants(atmosphere, Marginal):
        _toxicity = Atmosphere.Toxicity.MILD

    return Pollutants


class MarginalCandidate(object):
    """the MarginalCandidate class to be inherited by marginalizable
specialized atmospheres"""

    def make_marginal(self, marginal_type=None):
        """makes a marginal candidate atmosphere marginal using the
provided marginal modifier or one at random"""

        if issubclass(type(self), Marginal):
            self.remove_marginal()

        marginal_dist = {
            chlorine_or_fluorine: .01852,
            high_carbon_dioxide: .07408,
            high_oxygen: .06944,
            inert_gases: .21296,
            low_oxygen: .25,
            nitrogen_compounds: .21296,
            sulfur_compounds: .06944,
            organic_toxins: .07408,
            pollutants: .01852
        }

        if marginal_type is None:
            marginal_type = RandomGenerator().choice(list(marginal_dist.keys()),
                                                     list(marginal_dist.values()))[0]

        base = copy.copy(self)
        base.locked = True
        marginal = self
        marginal.__class__ = marginal_type(type(self))
        marginal._base = base

    def remove_marginal(self):

        if issubclass(type(self), Marginal):
            base_type = type(self.base)
            atmosphere = self
            atmosphere.__class__ = base_type
            atmosphere.locked = False
