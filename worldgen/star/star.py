# -*- coding: utf-8 -*-

from typing import Tuple

from numpy.random import rand
from .. import Range, RandomizableModel

import sys
import random
from enum import Enum
from math import sqrt
from collections import namedtuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import truncexpon, kstest


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
                                  'M3', 'M4', 'M4', 'M5', 'M6', 'M7']}
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
        upper, lower = 2, .1
        b = upper - lower
        mu = lower
        sigma = .3164
        self.mass = truncexpon(b=b / sigma, scale=sigma, loc=mu).rvs()
        """self.mass = random.choices(list(self.stellar_evolution.mass),
                                   weights=list(self.stellar_evolution.p), k=1)[0]"""

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

    @staticmethod
    def __l_max(mass):
        """l_max fitted through the form a*exp(b*x)+c with threshold on .9"""
        if mass >= .95:
            return 0.320293 * np.exp(2.09055499 * mass) - 0.95302065
        elif mass >= .45:
            return 0.01864272 * np.exp(4.53674559 * mass) - 0.07758067
            return np.nan
        return np.nan

    @staticmethod
    def __l_min(mass):
        """l_min fitted through the form a*exp(b*x)+c"""
        return 4.33687595 * mass ** 3 - 5.79058616 * mass ** 2 + 2.42228237 * mass - 0.24000098

    @staticmethod
    def __m_span(mass):
        """m_span fitted through the form a*exp(b*x)+c"""
        if mass >= .45:
            return 355.25732733 * np.exp(-3.62394465 * mass) - 1.19842708
        return np.nan

    @staticmethod
    def __s_span(mass):
        """s_span fitted through the form a*exp(b*x)"""
        if mass >= .95:
            return 18.445568275396568 * np.exp(-2.471832533773299 * mass)
        return np.nan

    @staticmethod
    def __g_span(mass):
        """g_span fitted through the form a*exp(b*x)"""
        if mass >= .95:
            return 11.045171731219448 * np.exp(-2.4574060414344223 * mass)
        return np.nan
    
    @staticmethod
    def __temp(mass):
        """temp fitted through the form a * x + b)"""
        return 2948.6212815383583 * mass + 2598.6586686607316

    @property
    def mass(self):
        """mass in M☉"""
        # TODO: handle white dwarf luminosity class mass
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
        m_span = type(self).__m_span(self.mass)
        s_span = type(self).__s_span(self.mass)
        g_span = type(self).__g_span(self.mass)
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
        m_span = type(self).__m_span(self.mass)
        if (np.isnan(type(self).__l_max(self.mass))):
            return type(self).__l_min(self.mass)
        # TODO: change to match-case after python 3.10 release
        if (self.luminosity_class == self.Luminosity.IV):
            return type(self).__l_max(self.mass)
        if (self.luminosity_class == self.Luminosity.III):
            return type(self).__l_max(self.mass) * 25
        if (self.luminosity_class == self.Luminosity.D):
            return .001
        return (type(self).__l_min(self.mass) + (self.age / m_span) *
                (type(self).__l_max(self.mass) - type(self).__l_min(self.mass)))

    @property
    def temperature(self):
        """effective temperature in K"""
        if (self.luminosity_class == self.Luminosity.IV):
            temp = type(self).__temp(self.mass)
            return (temp - ((self.age - type(self).__m_span(self.mass)) /
                    type(self).__s_span(self.mass)) * (temp - 4800))
        # TODO: handle giant luminosity class
        # TODO: handle white dwarves luminosity class
        return type(self).__temp(self.mass)

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
