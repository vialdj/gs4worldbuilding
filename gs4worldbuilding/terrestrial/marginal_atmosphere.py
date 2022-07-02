from abc import ABC
import copy
from typing import Callable, Type, Optional
from gs4worldbuilding.model.randomizable_model import RandomizableModel

from gs4worldbuilding.terrestrial import Atmosphere, Toxicity
from gs4worldbuilding.random import RandomGenerator


class MarginalMixin(ABC):
    '''the Marginal class to be inherited by concrete marginal modifiers'''

    @property
    def base(self) -> Atmosphere:
        '''the base atmosphere'''
        return self._base

    @base.setter
    def base(self, base: Atmosphere):
        self._base = base


def chlorine_or_fluorine(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere 'Chlorine of Fluorine' marginal'''
    class ChlorineOrFluorine(atmosphere_type, MarginalMixin):
        '''the 'Chlorine of Fluorine' marginal atmosphere'''
        _toxicity = Toxicity.HIGH

    return ChlorineOrFluorine


def high_carbon_dioxide(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere 'High Carbon Dioxide' marginal'''
    class HighCarbonDioxide(atmosphere_type, MarginalMixin):
        '''the 'High Carbon Dioxide' marginal atmosphere'''
        _toxicity = Toxicity.MILD

    return HighCarbonDioxide


def high_oxygen(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere 'High Oxygen' marginal'''
    class HighOxygen(atmosphere_type, MarginalMixin):
        '''the 'High Oxygen' marginal atmosphere'''
        _toxicity = Toxicity.MILD

    return HighOxygen


def inert_gases(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere 'Inert Gas' marginal'''
    class InertGases(atmosphere_type, MarginalMixin):
        '''the 'Inert Gas' marginal atmosphere'''

    return InertGases


def low_oxygen(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere low oxygen marginal'''
    class LowOxygen(atmosphere_type, MarginalMixin):
        '''the 'Low Oxygen' marginal atmosphere'''

    return LowOxygen


def nitrogen_compounds(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere 'Nitrogen Compounds' marginal'''
    class NitrogenCompounds(atmosphere_type, MarginalMixin):
        '''The 'Nitrogen Coumpounds' marginal atmosphere'''
        _toxicity = Toxicity.MILD

    return NitrogenCompounds


def sulfur_compounds(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere 'Sulfur Compounds' marginal'''
    class SulfurCompounds(atmosphere_type, MarginalMixin):
        '''The 'Sulfur Coumpounds' marginal atmosphere'''
        _toxicity = Toxicity.MILD

    return SulfurCompounds


def organic_toxins(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere 'Organic Toxins' marginal'''
    class OrganicToxins(atmosphere_type, MarginalMixin):
        '''the 'Organic toxins' marginal atmosphere'''
        _toxicity = Toxicity.MILD

    return OrganicToxins


def pollutants(atmosphere_type: Type['MarginalCandidate']):
    '''decorator to make the atmosphere 'Pollutants' marginal'''
    class Pollutants(atmosphere_type, MarginalMixin):
        '''the 'Pollutants' marginal atmosphere'''
        _toxicity = Toxicity.MILD

    return Pollutants


class MarginalCandidate(Atmosphere, RandomizableModel):
    '''the MarginalCandidate class to be inherited by marginalizable
specialized atmospheres'''

    def make_marginal(self,
                      marginal_type: Optional[Callable] = None):
        '''makes a marginal candidate atmosphere instance marginal using the
provided marginal modifier or one at random'''

        if isinstance(self, MarginalMixin):
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

        applied_type = (marginal_type if marginal_type else
                        RandomGenerator().choice(list(marginal_dist.keys()),
                                                 list(marginal_dist.values())))
        base = copy.copy(self)
        marginal = self
        marginal.__class__ = applied_type(type(self))
        marginal.base = base

    def remove_marginal(self) -> None:
        '''remove the marginal modifier on instance if any'''
        if isinstance(self, MarginalMixin):
            base_type = type(self._base)
            atmosphere_type = self
            atmosphere_type.__class__ = base_type
