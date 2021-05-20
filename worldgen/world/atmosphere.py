from enum import Enum

import numpy as np


# marginal atmpsheres decorators
def chlorine_or_fluorine(cls):
    cls._marginal = 'chlorine_or_fluorine'


def high_carbon_dioxide(cls):
    pass


def high_oxygen(cls):
    pass


def inert_gases(cls):
    pass


def low_oxygen(cls):
    pass


def nitrogen_compounds(cls):
    pass


def sulfur_compounds(cls):
    pass


def organic_toxins(cls):
    pass


def pollutants(cls):
    pass


class Atmosphere(object):
    """the Atmosphere Model"""

    marginal_distribution = {chlorine_or_fluorine: 0.01852,
                             high_carbon_dioxide: 0.07408,
                             high_oxygen: 0.06944,
                             inert_gases: 0.21296,
                             low_oxygen: 0.25,
                             nitrogen_compounds: 0.21296,
                             sulfur_compounds: 0.06944,
                             organic_toxins: 0.07408,
                             pollutants: 0.01852
                            }

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
    def marginal(self):
        """the marginal modifier"""
        return (type(self)._marginal
                if hasattr(type(self), '_marginal') else None)

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
