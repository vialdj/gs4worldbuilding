# -*- coding: utf-8 -*-

from . import model
from .random import roll1d6, roll3d6
from .star import Star
from .companion_star import CompanionStar

from collections import namedtuple
import random
import enum

from ordered_enum import ValueOrderedEnum
from astropy import units as u


class StarSystem(model.RandomizableModel):
    """the StarSystem model"""

    _precedence = ['population', 'age', 'stars']

    @enum.unique
    class MultipleStars(int, ValueOrderedEnum):
        """class MultipleStars Enum"""
        UNARY = 1
        BINARY = 2
        TERNARY = 3
        QUATERARY = 4

    population = namedtuple('Population', ['base', 'step_a', 'step_b'])

    class Population(population, enum.Enum):
        """class population Enum from Stellar Age Table with base and
steps in Ga"""
        EXTREME_POPULATION_1 = (0 * u.Ga, 0 * u.Ga, 0 * u.Ga)
        YOUNG_POPULATION_1 = (.1 * u.Ga, .3 * u.Ga, .05 * u.Ga)
        INTERMEDIATE_POPULATION_1 = (2 * u.Ga, .6 * u.Ga, .1 * u.Ga)
        OLD_POPULATION_1 = (5.6 * u.Ga, .6 * u.Ga, .1 * u.Ga)
        INTERMEDIATE_POPULATION_2 = (8 * u.Ga, .6 * u.Ga, .1 * u.Ga)
        EXTREME_POPULATION_2 = (10 * u.Ga, .6 * u.Ga, .1 * u.Ga)

    def random_population(self):
        """sum of a 3d roll over Stellar Age Table populations categories"""
        self.population = random.choices(list(self.Population),
                                         weights=self._population_dist,
                                         k=1)[0]

    def random_age(self):
        """2 distinct rolls of 1d-1 times step-a and step-b added to base age
from Stellar Age Table"""
        self.age = (self.population.base +
                    roll1d6(-1, continuous=True) * self.population.step_a +
                    roll1d6(-1, continuous=True) * self.population.step_b)

    @property
    def age(self) -> u.Quantity:
        """age in Ga"""
        return self._get_bounded_property('age') * u.Ga

    @property
    def age_bounds(self):
        """computed value range for age"""
        return model.bounds.QuantityBounds(
            self.population.base,
            self.population.base + 5 * self.population.step_a +
            5 * self.population.step_b
        )

    @property
    def multiplicity(self):
        return list(self.MultipleStars)[len(self._stars) - 1]

    @age.setter
    def age(self, value):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'time' not in value.unit.physical_type:
            raise ValueError('can\'t set age to value of %s physical type' %
                             value.unit.physical_type)
        self._set_bounded_property('age', value.to(u.Ga))

    def make_stars(self, n):
        """the system stars generation and arrangement procedure"""
        primary_star = Star(self)

        if hasattr(self, '_stars'):
            for i in range(len(self._stars)):
                delattr(type(self), chr(ord('A') + i))

        self._stars = [primary_star]
        if n > 1:
            secondary_star = CompanionStar(self, primary_star)
            primary_star._companions = [secondary_star]
            secondary_star._companions = [primary_star]
            self._stars.append(secondary_star)
        if n > 2:
            teriary_star = CompanionStar(self, primary_star, True)
            primary_star._companions.append(teriary_star)
            # for the third component in a trinary star system
            # the closest companion is the primary star of the system
            teriary_star._companions = [primary_star, secondary_star]
            secondary_star._companions.append(teriary_star)
            self._stars.append(teriary_star)

        # sub-companion star rolls if allowed
        for star in filter(lambda s: s.separation >=
                           CompanionStar.Separation.DISTANT, self._stars[1:]):
            if roll3d6() >= 11:
                companion = CompanionStar(self, star, sub_companion=True)
                # the two stars are closest companions
                star._companions.insert(0, companion)
                companion._companions = [star]
                self._stars.append(companion)

        for i in range(len(self._stars)):
            self._stars[i].name = chr(ord('A') + i)
            setattr(type(self), chr(ord('A') + i),
                    property(lambda self, i=i: self._stars[i]))

        # populate stars orbits
        self._worlds = []
        for star in self._stars:
            star.populate()
            self._worlds.extend(star._worlds)

    def random_stars(self):
        """the system randomization of stars"""
        # multiple star roll
        self.make_stars(random.choices([1, 2, 3], weights=self._stars_dist,
                                       k=1)[0])

    @property
    def population(self) -> Population:
        """population category over Stellar Age Table"""
        return self._population

    @property
    def population_bounds(self):
        """population range class variable"""
        return (type(self)._population_bounds
                if hasattr(type(self), '_population_bounds')
                else model.bounds.ValueBounds(
                                    self.Population.EXTREME_POPULATION_1,
                                    self.Population.EXTREME_POPULATION_2
                                  )
                )

    @population.setter
    def population(self, value):
        if not isinstance(value, self.Population):
            raise ValueError('population value type has to be {}'
                             .format(self.Population))
        self._set_bounded_property('population', value)

    def __init__(self, open_cluster=False, garden_host=False):
        self.garden_host = garden_host
        if open_cluster:
            self._stars_dist = [.162037037, .578703704, .259259259]
        else:
            self._stars_dist = [.5, .453703703, .046296297]
        if garden_host:
            self._population_dist = [0, .166666667, 0.555555556, .277777778, 0,
                                     0]
            self._population_bounds = model.bounds.ValueBounds(
                                        self.Population.YOUNG_POPULATION_1,
                                        self.Population.OLD_POPULATION_1
                                      )
        else:
            self._population_dist = [.00462963, .087962963, .407407407,
                                     .407407407, .087962963, .00462963]
        self.randomize()
