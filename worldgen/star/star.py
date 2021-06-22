# -*- coding: utf-8 -*-

from typing import Tuple

from numpy.random import rand
from .. import Range, RandomizableModel

import random
from enum import Enum
from collections import namedtuple

import numpy as np


class Star(RandomizableModel):
    """the star model"""

    population = namedtuple('Population', ['base', 'step_a', 'step_b'])

    class Population(population, Enum):
        """class Population Enum from Stellar Age Table"""
        EXTREME_POPULATION_1 = (0, 0, 0)
        YOUNG_POPULATION_1 = (.1, .3, .05)
        INTERMEDIATE_POPULATION_1 = (2, .6, .1)
        OLD_POPULATION_1 = (5.6, .6, .1)
        INTERMEDIATE_POPULATION_2 = (8, .6, .1)
        EXTREME_POPULATION_2 = (10, .6, .1)

    def random_mass(self):
        """consecutive sum of a 3d roll times over Stellar Mass Table"""
        mass_distribution = {2: 0.002315, 1.9: 0.002315, 1.8: 0.003601121,
                             1.7: 0.005080129, 1.6: 0.00520875,
                             1.5: 0.004501471, 1.45: 0.009388529,
                             1.4: 0.006687757, 1.35: 0.007202243,
                             1.3: 0.007502452, 1.25: 0.009860048,
                             1.2: 0.0057875, 1.15: 0.011146262,
                             1.10: 0.012003738, 1.05: 0.011252058,
                             1: 0.014787942, 0.95: 0.00868,
                             0.9: 0.016716986, 0.85: 0.018003014,
                             0.8: 0.015753529, 0.75: 0.020703971,
                             0.7: 0.0121525, 0.65: 0.023404743,
                             0.6: 0.025205257, 0.55: 0.030006752,
                             0.5: 0.042330748, 0.45: 0.0434025,
                             0.4: 0.0324075, 0.35: 0.0457175,
                             0.3: 0.046875, 0.25: 0.125,
                             0.2: 0.11574, 0.15: 0.09722,
                             0.1: 0.16204}
        self.mass = random.choices(list(mass_distribution.keys()),
                                   weights=list(mass_distribution.values()), k=1)[0]

    def random_population(self):
        """sum of a 3d roll over Stellar Age Table populations categories"""
        self.population = random.choices(list(self.Population),
                                         weights=[0.00463, 0.08797, 0.4074,
                                                  0.4074, 0.08797, 0.00463],
                                         k=1)[0]

    def random_age(self):
        self._age = ((random.uniform(0, 5) * self.population.step_a +
                     random.uniform(0, 5) * self.population.step_b) /
                     (self.age_range.max - self.age_range.min))

    @property
    def mass(self):
        """mass in M☉"""
        return self._mass

    @property
    def mass_range(self):
        """value range for mass"""
        return Range(.1, 2)

    @mass.setter
    def mass(self, value):
        self._set_ranged_property('mass', value)

    @property
    def population(self):
        """population category over Stellar Age Table"""
        return self._population

    @population.setter
    def population(self, value):
        if not isinstance(value, self.Population):
            raise ValueError('{} value type has to be {}'.format('population', self.Population))
        self._population = value

    @property
    def age(self):
        """age in Ga"""
        return self.population.base + (self.age_range.max -
                                       self.age_range.min) * self._age

    @property
    def age_range(self):
        """computed value range for age"""
        return Range(self.population.base, self.population.base +
                     5 * self.population.step_a + 5 * self.population.step_b)

    @age.setter
    def age(self, value):
        self._set_ranged_property('age', value)

    def __init__(self):
        self.randomize(['mass', 'population', 'age'])

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
