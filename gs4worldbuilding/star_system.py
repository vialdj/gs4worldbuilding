from collections import namedtuple
from typing import List, Literal, Optional

from ordered_enum import OrderedEnum
from astropy import units as u

from gs4worldbuilding.model import RandomizableModel
from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.star import Star
from gs4worldbuilding.companion_star import CompanionStar, Separation
from gs4worldbuilding.model.bounds import QuantityBounds, EnumBounds

PopulationTuple = namedtuple('Population', ['base', 'step_a', 'step_b'])


class Population(PopulationTuple, OrderedEnum):
    '''population Enum from Stellar Age Table with base and
steps in Ga'''
    EXTREME_POPULATION_1 = (0 * u.Ga, 0 * u.Ga, 0 * u.Ga)
    YOUNG_POPULATION_1 = (.1 * u.Ga, .3 * u.Ga, .05 * u.Ga)
    INTERMEDIATE_POPULATION_1 = (2 * u.Ga, .6 * u.Ga, .1 * u.Ga)
    OLD_POPULATION_1 = (5.6 * u.Ga, .6 * u.Ga, .1 * u.Ga)
    INTERMEDIATE_POPULATION_2 = (8 * u.Ga, .6 * u.Ga, .1 * u.Ga)
    EXTREME_POPULATION_2 = (10 * u.Ga, .6 * u.Ga, .1 * u.Ga)


class StarSystem(RandomizableModel):
    '''the StarSystem model'''

    def random_population(self) -> PopulationTuple:
        '''sum of a 3d roll over Stellar Age Table populations categories'''
        return RandomGenerator().choice(list(Population),
                                        self._population_dist)

    def random_age(self) -> u.Quantity:
        '''2 distinct rolls of 1d-1 times step-a and step-b added to base age
from Stellar Age Table'''
        return (self.population.base +
                RandomGenerator().roll1d6(-1, continuous=True)
                * self.population.step_a +
                RandomGenerator().roll1d6(-1, continuous=True)
                * self.population.step_b)

    @property
    def age(self) -> u.Quantity:
        '''age in Ga'''
        return self._get_bounded_property('age')

    @property
    def age_bounds(self) -> QuantityBounds:
        '''computed value range for age'''
        return QuantityBounds(
            self.population.base,
            self.population.base + 5 * self.population.step_a +
            5 * self.population.step_b
        )

    @property
    def multiplicity(self) -> int:
        '''The star system multiplicity'''
        return len(self._stars)

    @age.setter
    def age(self, value):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'time' not in value.unit.physical_type:
            raise ValueError("can't set age to value of " +
                             f'{value.unit.physical_type} physical type')
        self._set_bounded_property('age', value.to(u.Ga))

    @property
    def stars(self) -> List[Star]:
        '''The system stars'''
        return self._stars

    def make_stars(self, n_stars: Literal[1, 2, 3],
                   allow_subcompanions: bool = False) -> List[Star]:
        '''the system stars generation and arrangement procedure'''
        primary_star = Star(self)

        companion_stars: List[CompanionStar] = []
        if n_stars > 1:
            secondary_star = CompanionStar(self, primary_star)
            primary_star._companions = [secondary_star]
            secondary_star._companions = [primary_star]
            companion_stars.append(secondary_star)
        if n_stars > 2:
            teriary_star = CompanionStar(self, primary_star, True)
            primary_star._companions.append(teriary_star)
            # for the third component in a trinary star system
            # the closest companion is the primary star of the system
            teriary_star._companions = [primary_star, secondary_star]
            secondary_star._companions.append(teriary_star)
            companion_stars.append(teriary_star)

        # sub-companion star rolls if allowed
        for star in filter(lambda s: s.separation >=
                           Separation.DISTANT, companion_stars[1:]):
            if RandomGenerator().roll3d6() >= 11 and allow_subcompanions:
                companion = CompanionStar(self, star, sub_companion=True)
                # the two stars are closest companions
                star._companions.insert(0, companion)
                companion._companions = [star]
                companion_stars.append(companion)

        return [primary_star, *companion_stars]

        # populate stars orbits
        """self._worlds = []
        for star in self._stars:
            star.populate()
            self._worlds.extend(star._worlds)"""

    def random_stars(self) -> List[Star]:
        '''the system randomization of stars'''
        # multiple star roll
        return self.make_stars(RandomGenerator()
                               .choice([1, 2, 3], self._stars_dist),
                               allow_subcompanions=True)

    @property
    def population(self) -> Population:
        '''population category over Stellar Age Table'''
        return self._population

    @property
    def population_bounds(self):
        '''population range class variable'''
        return (self._population_bounds
                if hasattr(type(self), '_population_bounds')
                else EnumBounds(Population.EXTREME_POPULATION_1,
                                Population.EXTREME_POPULATION_2))

    @population.setter
    def population(self, value):
        if not isinstance(value, Population):
            raise ValueError("population value type has to be " +
                             f'{Population}')
        self._set_bounded_property('population', value)

    def randomize(self) -> None:
        self.population = self.random_population()
        self.age = self.random_age()
        self._stars = self.random_stars()

    def __init__(self, open_cluster=False, garden_host=False,
                 n_stars: Optional[Literal[1, 2, 3]] = None):
        self.garden_host = garden_host
        if open_cluster:
            self._stars_dist = [.162037037, .578703704, .259259259]
        else:
            self._stars_dist = [.5, .453703703, .046296297]
        if garden_host:
            self._population_dist = [0, .166666667, 0.555555556, .277777778, 0,
                                     0]
            self._population_bounds = EnumBounds(
                                        Population.YOUNG_POPULATION_1,
                                        Population.OLD_POPULATION_1
                                      )
        else:
            self._population_dist = [.00462963, .087962963, .407407407,
                                     .407407407, .087962963, .00462963]

        self.population = self.random_population()
        self.age = self.random_age()
        if not n_stars:
            self._stars = self.random_stars()
        else:
            self._stars = self.make_stars(n_stars)

    def __eq__(self, other: 'StarSystem') -> bool:
        return (isinstance(other, type(self)) and
                self.age == other.age and
                self.multiplicity == other.multiplicity and
                self.population == other.population and
                self.stars == other.stars)

    def __getitem__(self, idx) -> Star:
        '''return the star system's star at idx'''
        return self._stars[idx]

    def __len__(self) -> int:
        return len(self._stars)
