from . import Star

from enum import Enum
from random import choices

import numpy as np
from scipy.stats import truncnorm


class CompanionStar(Star):

    _precedence = [*Star._precedence, 'separation', 'eccentricity', 'average_orbital_radius']

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
                                  weights=[.0926, .2824, .25, .2824, .0926],
                                  k=1)[0]

    def random_eccentricity(self):
        """consecutive sum of a 3d roll times over Stellar Mass Table"""
        xa, xb = .0, .95
        mu, sigma = .4954545454545455, .10522727272727272
        a, b = (xa - mu) / sigma, (xb - mu) / sigma
        self._eccentricity = truncnorm(a, b, mu, sigma).rvs()

    def random_average_orbital_radius(self):
        """roll of 2d multiplied by the separation category radius"""
        self.average_orbital_radius = np.random.triangular(2, 7, 12) * self._separation.value

    @property
    def separation(self):
        """separation category over Orbital Separation Table"""
        return self._separation

    @separation.setter
    def separation(self, value):
        if not isinstance(value, self.Separation):
            raise ValueError('{} value type has to be {}'.format('separation', self.Separation))
        self._separation = value

    @property
    def average_orbital_radius(self):
        """The average orbital radius to the primary star in AU"""
        return self._average_orbital_radius

    @property
    def average_orbital_radius_range(self):
        """value range for average orbital radius"""
        return type(self).Range(2 * self._separation.value, 12 * self._separation.value)

    @average_orbital_radius.setter
    def average_orbital_radius(self, value):
        self._set_ranged_property('average_orbital_radius', value)

    @property
    def eccentricity(self):
        """the companion orbit eccentricity"""
        return self._eccentricity

    @property
    def eccentricity_range(self):
        """value range for eccentricity"""
        return type(self).Range(.0, .95)

    @eccentricity.setter
    def eccentricity(self, value):
        self._set_ranged_property('eccentricity', value)

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

    def __init__(self, star_system, primary_star):
        super(CompanionStar, self).__init__(star_system)
        self._primary_star = primary_star
