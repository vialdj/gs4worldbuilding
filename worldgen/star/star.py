# -*- coding: utf-8 -*-

from .. import RandomizableModel

import random
from enum import Enum
from math import sqrt
from collections import namedtuple

import numpy as np
from scipy.stats import truncexpon


class Star(RandomizableModel):
    """the Star model on its main sequence"""

    _precedence = ['mass', 'population', 'age']
    #_luminosity_class = Star.Luminosity.V

    population = namedtuple('Population', ['base', 'step_a', 'step_b'])

    class Population(population, Enum):
        """class Population Enum from Stellar Age Table"""
        EXTREME_POPULATION_1 = (0, 0, 0)
        YOUNG_POPULATION_1 = (.1, .3, .05)
        INTERMEDIATE_POPULATION_1 = (2, .6, .1)
        OLD_POPULATION_1 = (5.6, .6, .1)
        INTERMEDIATE_POPULATION_2 = (8, .6, .1)
        EXTREME_POPULATION_2 = (10, .6, .1)

    class Luminosity(Enum):
        V = 'Main sequence'
        IV = 'Subgiant'
        III = 'Giant'
        D = 'White dwarf'

    def random_mass(self):
        """consecutive sum of a 3d roll times over Stellar Mass Table"""
        upper, lower = 2, .1
        b = upper - lower
        mu = lower
        sigma = .3164
        self._mass = truncexpon(b=b / sigma, scale=sigma, loc=mu).rvs()

    def random_population(self):
        """sum of a 3d roll over Stellar Age Table populations categories"""
        self.population = random.choices(list(self.Population),
                                         weights=[0.00463, 0.08797, 0.4074,
                                                  0.4074, 0.08797, 0.00463],
                                         k=1)[0]

    def random_age(self):
        if (self.age_range.max - self.age_range.min) > 0:
            self._age = self.population.base + (random.uniform(0, 5) * self.population.step_a +
                                                random.uniform(0, 5) * self.population.step_b)
        else:
            self._age = np.nan

    @staticmethod
    def _l_max(mass):
        """l_max fitted through the form a*x**b"""
        if mass >= .45:
            return 1.417549268949681 * mass ** 3.786542028176919
        return np.nan

    @staticmethod
    def __l_min(mass):
        """l_min fitted through the form a*x**b"""
        return 0.8994825154104518 * mass ** 4.182711149771404

    @staticmethod
    def _m_span(mass):
        """m_span fitted through the form a*exp(b*x)+c"""
        if mass >= .45:
            return 355.25732733 * np.exp(-3.62394465 * mass) - 1.19842708
        return np.nan

    @staticmethod
    def _s_span(mass):
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
    def _temp(mass):
        """temp in interval [3100, 8200] linearly through the form a * x + b)"""
        return 2684.21052632 * mass + 2831.57894737

    @property
    def mass(self):
        """mass in M☉"""
        # TODO: handle white dwarf luminosity class mass
        return self._mass

    @property
    def mass_range(self):
        """value range for mass"""
        return type(self).Range(.1, 2)

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
        return self._age

    @property
    def age_range(self):
        """computed value range for age"""
        return type(self).Range(self.population.base, self.population.base +
                                5 * self.population.step_a + 5 * self.population.step_b)

    @age.setter
    def age(self, value):
        self._set_ranged_property('age', value)

    @property
    def luminosity_class(self):
        """the star luminosity class"""
        return self._luminosity_class if hasattr(self, '_luminosity_class') else type(self).Luminosity.V
        m_span = type(self).__m_span(self._mass)
        s_span = type(self).__s_span(self._mass) + m_span
        g_span = type(self).__g_span(self._mass) + s_span
        if (not np.isnan(g_span) and self.age > g_span):
            return self.Luminosity.D
        if (not np.isnan(s_span) and self.age > s_span):
            return self.Luminosity.III
        if (not np.isnan(m_span) and self.age > m_span):
            return self.Luminosity.IV
        return self.Luminosity.V

    @property
    def luminosity(self):
        """luminosity in L☉"""
        if (np.isnan(type(self)._l_max(self.mass))):
            return type(self).__l_min(self.mass)
        return (type(self).__l_min(self.mass) + (self.age / type(self)._m_span(self.mass)) *
                (type(self)._l_max(self.mass) - type(self).__l_min(self.mass)))

    @property
    def temperature(self):
        """effective temperature in K"""
        return type(self)._temp(self.mass)

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
        """spectral type from mass"""
        d = {2: 'A5', 1.9: 'A6', 1.8: 'A7', 1.7: 'A9', 1.6: 'F0', 1.5: 'F2',
             1.45: 'F3', 1.4: 'F4', 1.35: 'F5', 1.3: 'F6', 1.25: 'F7',
             1.2: 'F8', 1.15: 'F9', 1.10: 'G0', 1.05: 'G1', 1: 'G2',
             .95: 'G4', .9: 'G6', .85: 'G8', .8: 'K0', .75: 'K2', .7: 'K4',
             .65: 'K5', .6: 'K6', .55: 'K8', .5: 'M0', .45: 'M1', .4: 'M2',
             .35: 'M3', .3: 'M4', .25: 'M4', .2: 'M5', .15: 'M6', .1: 'M7'}
        return d[list(filter(lambda x: x >= self.mass, sorted(d.keys())))[0]]

    def __init__(self):
        self.randomize()
