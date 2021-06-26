# -*- coding: utf-8 -*-

from typing import Tuple

from numpy.random import rand
from .. import Range, RandomizableModel

import random
from enum import Enum
from math import sqrt
from collections import namedtuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize

class Star(RandomizableModel):
    """the star model"""

    population = namedtuple('Population', ['base', 'step_a', 'step_b'])

    stellar_evolution = {'p': [0.002315, 0.002315, 0.003601121, 0.005080129,
                               0.00520875, 0.004501471, 0.009388529,
                               0.006687757, 0.007202243, 0.007502452,
                               0.009860048, 0.0057875, 0.011146262,
                               0.012003738, 0.011252058, 0.014787942, 0.00868,
                               0.016716986, 0.018003014, 0.015753529,
                               0.020703971, 0.0121525, 0.023404743,
                               0.025205257, 0.030006752, 0.042330748,
                               0.0434025, 0.0324075, 0.0457175, 0.046875,
                               0.125, 0.11574, 0.09722, 0.16204],
                         'mass': [2, 1.9, 1.8, 1.7, 1.6, 1.5, 1.45, 1.4,
                                  1.35, 1.3, 1.25, 1.2, 1.15, 1.10, 1.05,
                                  1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7,
                                  0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35,
                                  0.3, 0.25, 0.2, 0.15, 0.1],
                         'type': ['A5', 'A6', 'A7', 'A9', 'F0', 'F2', 'F3',
                                  'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'G0',
                                  'G1', 'G2', 'G4', 'G6', 'G8', 'K0', 'K2',
                                  'K4', 'K5', 'K6', 'K8', 'M0', 'M1', 'M2',
                                  'M3', 'M4', 'M4', 'M5', 'M6', 'M7'],
                         'temp': [8200, 8000, 7800, 7500, 7300, 7000, 6900,
                                  6700, 6600, 6500, 6400, 6300, 6100, 6000,
                                  5900, 5800, 5700, 5500, 5400, 5200, 4900,
                                  4600, 4400, 4200, 4000, 3800, 3600, 3500,
                                  3400, 3300, 3300, 3200, 3200, 3100],
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
        self.mass = random.choices(list(self.stellar_evolution.mass),
                                   weights=list(self.stellar_evolution.p), k=1)[0]

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
        # TODO: handle white dwarf luminosity class mass
        return self._mass

    @property
    def l_max(self):
        """l_max fitted through the form a*exp(b*x)+c"""
        return 0.320293 * np.exp(2.09055499 * self.mass) - 0.95302065 if self.mass >= .45 else np.nan

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
        """luminosity in L☉"""
        l_min = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].l_min
        m_span = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].m_span
        if (np.isnan(self.l_max)):
            return l_min
        # TODO: change to match-case after python 3.10 release
        if (self.luminosity_class == self.Luminosity.IV):
            return self.l_max
        if (self.luminosity_class == self.Luminosity.III):
            return self.l_max * 25
        if (self.luminosity_class == self.Luminosity.D):
            return .001
        return (l_min + (self.age / m_span) * (self.l_max - l_min))

    @property
    def temperature(self):
        """effective temperature in K"""
        if (self.luminosity_class == self.Luminosity.IV):
            temp = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].temp
            m_span = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].m_span
            s_span = self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].s_span
            return temp - ((self.age - m_span) / s_span) * (temp - 4800)
        # TODO: handle giant luminosity class
        # TODO: handle white dwarves luminosity class
        return self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].temp

    @property
    def radius(self):
        """radius in AU"""
        # TODO: handle white dwarf luminosity class
        return (155000 * sqrt(self.luminosity)) / self.temperature ** 2

    @property
    def inner_limit(self):
        """inner limit in AU"""
        return max(0.1 * self.mass, 0.01 * sqrt(self.luminosity))

    @property
    def outer_limit(self):
        """outer limit in AU"""
        return 40 * self.mass

    @property
    def snow_line(self):
        """snow line in AU"""
        return 4.85 * sqrt(self.luminosity)

    @property
    def spectral_type(self):
        return self.stellar_evolution.iloc[self.stellar_evolution.index[self.mass >= self.stellar_evolution.mass].tolist()[0]].type

    def show(self):
        stellar_evolution = self.stellar_evolution[self.stellar_evolution.mass >= .45]
        #l_max = np.exp(stellar_evolution.mass * 2.62854207) * np.exp(-2.19029826)
        l_max = 0.320293 * np.exp(2.09055499 * stellar_evolution.mass) - 0.95302065
        _, ax = plt.subplots()
        ax.set_title(r'l_max fitted through the form: $\mathcal{a}\/\mathcal{e}^{\mathcal{bx}}+\mathcal{c}$')
        ax.plot(stellar_evolution.mass, stellar_evolution.l_max, 'o', label='l_max')
        ax.plot(stellar_evolution.mass, l_max, '-', label='l_max fit')
        ax.set_xlabel("mass in M☉")
        ax.set_ylabel("l_max in L☉")
        ax.legend()
        ax.annotate(r"""$\mathcal{a} = \mathcal{0.320293}$
$\mathcal{b} = \mathcal{2.09055499}$
$\mathcal{c} = \mathcal{-0.95302065}$""", xy = (1.7, .25))
        plt.show()

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
