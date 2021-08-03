from worldgen.star_system.orbital_object import OrbitalObject
from . import Star

from enum import Enum
from random import choices

import numpy as np
from scipy.stats import truncnorm


class CompanionStar(Star, OrbitalObject):

    _precedence = [*Star._precedence, 'separation', 'eccentricity', 'average_orbital_radius']
    _eccentricity_range = Star.Range(0, .95)

    class Separation(float, Enum):
        """class Separation Enum from Orbital Separation Table with radius multiplier in AU"""
        VERY_CLOSE = .05
        CLOSE = .5
        MODERATE = 2
        WIDE = 10
        DISTANT = 50

    def random_separation(self):
        """sum of a 3d roll over Orbital Separation Table"""
        self.separation = choices(list(self.Separation),
                                  weights=self._separation_distribution,
                                  k=1)[0]

    def random_eccentricity(self):
        """consecutive sum of a 3d roll times over Stellar Mass Table"""
        xa, xb = .0, .95
        mu, sigma = .516, .14421858410066296
        a, b = (xa - mu) / sigma, (xb - mu) / sigma
        self._eccentricity = truncnorm(a, b, mu, sigma).rvs()

    def random_average_orbital_radius(self):
        """roll of 2d multiplied by the separation category radius"""
        self.average_orbital_radius = np.random.triangular(2, 7, 12) * self._separation.value

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
        super(CompanionStar, self).__init__(star_system=star_system, parent_body=parent_body)
