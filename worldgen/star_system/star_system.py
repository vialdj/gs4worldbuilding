from .. import RandomizableModel
from . import Star
from . import CompanionStar

from collections import namedtuple
from enum import Enum
import random

import numpy as np

class StarSystem(RandomizableModel):
    """the StarSystem model"""

    _precedence = ['population', 'age', 'stars']

    population = namedtuple('Population', ['base', 'step_a', 'step_b'])

    class Population(population, Enum):
        """class population Enum from Stellar Age Table with base and steps in Ga"""
        EXTREME_POPULATION_1 = (0, 0, 0)
        YOUNG_POPULATION_1 = (.1, .3, .05)
        INTERMEDIATE_POPULATION_1 = (2, .6, .1)
        OLD_POPULATION_1 = (5.6, .6, .1)
        INTERMEDIATE_POPULATION_2 = (8, .6, .1)
        EXTREME_POPULATION_2 = (10, .6, .1)

    def random_population(self):
        """sum of a 3d roll over Stellar Age Table populations categories"""
        self.population = random.choices(list(self.Population),
                                         weights=[.00463, .08797, .4074,
                                                  .4074, .08797, .00463],
                                         k=1)[0]

    def random_age(self):
        if (self.age_range.max - self.age_range.min) > 0:
            self._age = self.population.base + (random.uniform(0, 5) * self.population.step_a +
                                                random.uniform(0, 5) * self.population.step_b)
        else:
            self._age = np.nan

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

    def __random_unary(self):
        pass

    def __random_binary(self):
        self.secondary_star = CompanionStar(self, self.primary_star)

    def __random_tertiary(self):
        self.secondary_star = CompanionStar(self, self.primary_star)
        self.tertiary_star = CompanionStar(self, self.primary_star)

    def random_stars(self):
        self.primary_star = Star(self)
        randomize = random.choices([self.__random_unary, self.__random_binary, self.__random_tertiary],
                                   weights=[.5, .4537, .0463],
                                   k=1)[0]
        randomize()

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
    def primary_star(self):
        return self._primary_star

    @primary_star.setter
    def primary_star(self, value):
        self._primary_star = value

    @property
    def secondary_star(self):
        return self._secondary_star if hasattr(self, '_secondary_star') else None

    @secondary_star.setter
    def secondary_star(self, value):
        self._secondary_star = value

    @property
    def tertiary_star(self):
        return self._tertiary_star if hasattr(self, '_tertiary_star') else None

    @tertiary_star.setter
    def tertiary_star(self, value):
        self._tertiary_star = value

    def __init__(self):
        self.randomize()
