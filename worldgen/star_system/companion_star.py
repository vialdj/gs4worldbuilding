from worldgen.star_system import star
from worldgen.star_system.orbital_object import OrbitalObject
from . import Star

from enum import Enum
import random

import numpy as np
from scipy.stats import truncnorm, truncexpon


class CompanionStar(Star, OrbitalObject):

    _precedence = [*Star._precedence, 'separation', 'eccentricity', 'average_orbital_radius']

    class Separation(float, Enum):
        """class Separation Enum from Orbital Separation Table with radius multiplier in AU"""
        VERY_CLOSE = .05
        CLOSE = .5
        MODERATE = 2
        WIDE = 10
        DISTANT = 50

    def random_seed_mass(self):
        """campanion star random mass procedure"""
        mass = self._parent_body.mass
        # roll 1d6 - 1
        r = random.randint(0, 5)
        if r >= 1:
            # sum of nd6 roll
            s = sum([random.randint(1, 6) for _ in range(r)])
            for _ in range(s):
                # count down on the stellar mass table
                mass -= (.05 if mass <= 1.5 else .10)
        # add noise to value
        n = .025 if mass <= 1.5 else .05
        mass += random.uniform(-n, n)
        # mass in [.1, 2] range
        self.seed_mass = min(max(.1, mass), 2)

    def random_separation(self):
        """sum of a 3d6 roll over Orbital Separation Table"""
        self.separation = random.choices(list(self.Separation),
                                         weights=self._separation_distribution,
                                         k=1)[0]

    @staticmethod
    def __truncnorm_draw(lower, upper, mu, sigma):
        a, b = (lower - mu) / sigma, (upper - mu) / sigma
        return truncnorm(a, b, mu, sigma).rvs()

    @staticmethod
    def __truncexpon_draw(lower, upper, sigma):
        mu = lower
        b = (upper - lower) / sigma
        return truncexpon(b, mu, sigma).rvs()

    def random_eccentricity(self):
        """sum of a 3d6 roll over Stellar Orbital Eccentricity Table with modifiers if any"""
        if self.separation == self.Separation.MODERATE:
            eccentricity = self.__truncnorm_draw(0, .8, .4151, .16553546447815948)
        elif self.separation == self.Separation.CLOSE:
            eccentricity = self.__truncnorm_draw(0, .7, .3055, .1839014681833726)
        elif self.separation == self.Separation.VERY_CLOSE:
            eccentricity = self.__truncexpon_draw(0, .6, .1819450191678794)
        else:
            eccentricity = self.__truncnorm_draw(0, .95, .5204, .142456449485448)
        self.eccentricity = eccentricity

    def random_average_orbital_radius(self):
        """roll of 2d6 multiplied by the separation category radius"""
        self.average_orbital_radius = np.random.triangular(2, 7, 12) * self._separation.value

    @property
    def seed_mass_range(self):
        """value range for mass adjusted so mass cannot be greater than parent body mass"""
        return type(self).Range(.1, self._parent_body.mass)

    @property
    def separation(self):
        """separation category over Orbital Separation Table"""
        return self._separation

    @property
    def separation_range(self):
        """ressource range class variable"""
        return self._separation_range if hasattr(self, '_separation_range') else type(self).Range(self.Separation.VERY_CLOSE, self.Separation.DISTANT)

    @separation.setter
    def separation(self, value):
        if not isinstance(value, self.Separation):
            raise ValueError('{} value type has to be {}'.format('separation', self.Separation))
        self._set_ranged_property('separation', value)

    @property
    def eccentricity_range(self):
        """value range for eccentricity dependant on parent star separation"""
        rngs = {self.Separation.MODERATE: Star.Range(0, .8),
                self.Separation.CLOSE: Star.Range(0, .7),
                self.Separation.VERY_CLOSE: Star.Range(0, .6)}
        return rngs[self.separation] if self.separation in rngs.keys() else Star.Range(0, .95)

    @property
    def average_orbital_radius_range(self):
        """value range for average orbital radius"""
        return type(self).Range(2 * self._separation.value, 12 * self._separation.value)

    @property
    def minimum_separation(self):
        """the minimum separation in AU"""
        return (1 - self.eccentricity) * self.average_orbital_radius

    @property
    def maximum_separation(self):
        """the maximum separation in AU"""
        return (1 + self.eccentricity) * self.average_orbital_radius

    def __init__(self, star_system, parent_body, tertiary_star=False):
        if tertiary_star:
            self._separation_distribution = [0, .00462963, .041666667, .212962963, 0.740740741]
            self._separation_range = type(self).Range(self.Separation.CLOSE, self.Separation.DISTANT)
        else:
            self._separation_distribution = [.0926, .2824, .25, .2824, .0926]
        OrbitalObject.__init__(self, parent_body)
        Star.__init__(self, star_system)