from worldgen.star_system import companion_star
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
        """class population Enum from Stellar Age Table with base and
steps in Ga"""
        EXTREME_POPULATION_1 = (0, 0, 0)
        YOUNG_POPULATION_1 = (.1, .3, .05)
        INTERMEDIATE_POPULATION_1 = (2, .6, .1)
        OLD_POPULATION_1 = (5.6, .6, .1)
        INTERMEDIATE_POPULATION_2 = (8, .6, .1)
        EXTREME_POPULATION_2 = (10, .6, .1)

    def random_population(self):
        """sum of a 3d roll over Stellar Age Table populations categories"""
        self.population = random.choices(list(self.Population),
                                         weights=self._population_dist,
                                         k=1)[0]

    def random_age(self):
        """2 distinct rolls of 1d-1 times step-a and step-b added to base age
from Stellar Age Table"""
        self.age = (self.population.base +
                    random.uniform(0, 5) * self.population.step_a +
                    random.uniform(0, 5) * self.population.step_b)

    @property
    def age(self):
        """age in Ga"""
        return self._get_ranged_property('age')

    @property
    def age_range(self):
        """computed value range for age"""
        return type(self).Range(self.population.base, self.population.base +
                                5 * self.population.step_a +
                                5 * self.population.step_b)

    @age.setter
    def age(self, value):
        self._set_ranged_property('age', value)

    def random_stars(self):
        """the system stars generation an arrangement procedure"""
        primary_star = Star(self)
        self.stars = [primary_star]
        # multiple star roll
        r = random.uniform(0, 1)
        if (r >= self._stars_dist[0]):
            companion = CompanionStar(self, self.primary_star)
            primary_star._companions = [companion]
            self.stars.append(companion)
        if r >= self._stars_dist[0] + self._stars_dist[1]:
            companion = CompanionStar(self, self.primary_star, True)
            primary_star._companions.append(companion)
            self.stars.append(companion)
        # sub-companion star rolls if any
        for star in filter(lambda s: s.separation >=
                           CompanionStar.Separation.DISTANT, self.stars[1:]):
            if (random.uniform(0, 1) > .5):
                companion = CompanionStar(self, star, sub_companion=True)
                star._companions = [companion]
                self.stars.append(companion)

    @property
    def population(self):
        """population category over Stellar Age Table"""
        return self._population

    @property
    def population_range(self):
        """population range class variable"""
        return (type(self)._population_range
                if hasattr(type(self), '_population_range')
                else type(self).Range(self.Population.EXTREME_POPULATION_1,
                                      self.Population.EXTREME_POPULATION_2))

    @population.setter
    def population(self, value):
        if not isinstance(value, self.Population):
            raise ValueError('population value type has to be {}'
                             .format(self.Population))
        self._set_ranged_property('population', value)

    @property
    def primary_star(self):
        return self.stars[0]

    @primary_star.setter
    def primary_star(self, value):
        self.stars[0] = value

    @property
    def secondary_star(self):
        return self.stars[1] if len(self.stars) > 1 else None

    @secondary_star.setter
    def secondary_star(self, value):
        if len(self.stars) > 1:
            self.stars[1] = value
        else:
            self.stars.append(value)

    @property
    def tertiary_star(self):
        return self.stars[2] if len(self.stars) > 2 else None

    @tertiary_star.setter
    def tertiary_star(self, value):
        if len(self.stars) > 2:
            self.stars[2] = value
        else:
            self.stars.append(value)

    def __init__(self, open_cluster=False, garden_host=False):
        self.garden_host = garden_host
        if open_cluster:
            self._stars_dist = [.162037037, .578703704, .259259259]
        else:
            self._stars_dist = [.5, .453703703, .046296297]
        if garden_host:
            self._population_dist = [0, .166666667, 0.555555556, .277777778, 0,
                                     0]
            self._population_range = type(self).Range(self.Population.YOUNG_POPULATION_1,
                                                      self.Population.OLD_POPULATION_1)
        else:
            self._population_dist = [.00462963, .087962963, .407407407,
                                     .407407407, .087962963, .00462963]
        self.randomize()
