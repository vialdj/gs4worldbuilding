# -*- coding: utf-8 -*-

from typing import Tuple

from numpy.random import rand
from .. import Range, RandomizableModel

import random
from enum import Enum
from collections import namedtuple

import numpy as np
import pandas as pd


class Star(RandomizableModel):
    """the star model"""

    population = namedtuple('Population', ['base', 'step_a', 'step_b'])

    stellar_evolution = {'mass': [2, 1.9, 1.8, 1.7, 1.6, 1.5, 1.45, 1.4,
                                  1.35, 1.3, 1.25, 1.2, 1.15, 1.10, 1.05,
                                  1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7,
                                  0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35,
                                  0.3, 0.25, 0.2, 0.15, 0.1],
                         'type': ['A5', 'A6', 'A7', 'A9', 'F0', 'F2', 'F3',
                                  'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'G0',
                                  'G1', 'G2', 'G4', 'G6', 'G8', 'K0', 'K2',
                                  'K4', 'K5', 'K6', 'K8', 'M0', 'M1', 'M2',
                                  'M3', 'M4', 'M4', 'M5', 'M6', 'M7'],
                         'l_min': [16, 13, 11, 8.6, 6.7, 5.1, 4.3, 3.7, 3.1,
                                   2.5, 2.1, 1.7, 1.4, 1.1, 0.87, 0.68, 0.56,
                                   0.45, 0.36, 0.28, 0.23, 0.19, 0.15, 0.13,
                                   0.11, 0.09, 0.07, 0.054, 0.037, 0.024,
                                   0.015, 0.0079, 0.0036, 0.0012],
                         'l_max': [20, 16, 13, 10, 8.2, 6.5, 5.7, 5.1, 4.5,
                                   3.9, 3.5, 3.0, 2.6, 2.2, 1.9, 1.6, 1.3,
                                   1.0, 0.84, 0.65, 0.48, 0.35, 0.25, 0.20,
                                   0.15, 0.11, 0.08],
                         'm_span': [1.3, 1.5, 1.8, 2.1, 2.5, 3.0, 3.3, 3.7,
                                    4.1, 4.6, 5.2, 5.9, 6.7, 7.7, 8.8, 10,
                                    12, 14, 17, 20, 24, 30, 37, 42, 50, 59,
                                    70],
                         's_span': [0.2, 0.2, 0.3, 0.3, 0.4, 0.5, 0.5, 0.6,
                                    0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6,
                                    1.8],
                         'g_span': [0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3, 0.4,
                                    0.4, 0.4, 0.5, 0.6, 0.6, 0.7, 0.8, 1.0,
                                    1.1]}
    stellar_evolution = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in stellar_evolution.items()]))

    class Population(population, Enum):
        """class Population Enum from Stellar Age Table"""
        EXTREME_POPULATION_1 = (0, 0, 0)
        YOUNG_POPULATION_1 = (.1, .3, .05)
        INTERMEDIATE_POPULATION_1 = (2, .6, .1)
        OLD_POPULATION_1 = (5.6, .6, .1)
        INTERMEDIATE_POPULATION_2 = (8, .6, .1)
        EXTREME_POPULATION_2 = (10, .6, .1)

    class Luminosity(Enum):
        V = 'Main sequence',
        IV = 'Subgiant',
        III = 'Giant',
        D = 'White dwarf'

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
        if (self.age_range.max - self.age_range.min) > 0:
            self._age = ((random.uniform(0, 5) * self.population.step_a +
                         random.uniform(0, 5) * self.population.step_b) /
                         (self.age_range.max - self.age_range.min))
        else:
            self._age = np.nan

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

    @property
    def luminosity_class(self):
        """the star luminosity class"""
        m_span = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].m_span
        s_span = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].s_span + m_span
        g_span = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].g_span + s_span
        if (not np.isnan(g_span) and self.age > g_span):
            return self.Luminosity.D
        elif (not np.isnan(s_span) and self.age > s_span):
            return self.Luminosity.III
        elif (not np.isnan(m_span) and self.age > m_span):
            return self.Luminosity.IV
        return self.Luminosity.V

    @property
    def luminosity(self):
        """star luminosity in L☉"""
        l_min = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].l_min
        l_max = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].l_max
        m_span = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].m_span
        if (np.isnan(l_max)):
            return l_min
        if (self.luminosity_class == self.Luminosity.IV):
            return l_max
        if (self.luminosity_class == self.Luminosity.III):
            return l_max * 25
        if (self.luminosity_class == self.Luminosity.D):
            return .001
        return (l_min + (self.age / m_span) * (l_max - l_min))

    @property
    def spectral_type(self):
        return self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].type

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
