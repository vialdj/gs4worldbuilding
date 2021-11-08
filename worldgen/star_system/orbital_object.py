# -*- coding: utf-8 -*-

from .. import model

import numpy as np
from astropy import units as u


class OrbitalObject(model.Model):
    """the orbital object model"""
    _eccentricity_bounds = model.bounds.ValueBounds(0, 1)

    @property
    def average_orbital_radius(self) -> u.Quantity:
        """The average orbital radius to the parent body in AU"""
        return self._get_bounded_property('average_orbital_radius') * u.au

    @average_orbital_radius.setter
    def average_orbital_radius(self, value):
        self._set_bounded_property('average_orbital_radius', value)

    @property
    def eccentricity(self) -> u.Quantity:
        """the orbital orbit eccentricity"""
        return self._get_bounded_property('eccentricity')

    @property
    def minimum_separation(self) -> u.Quantity:
        """the minimum separation in AU"""
        return (1 - self.eccentricity) * self.average_orbital_radius

    @property
    def maximum_separation(self) -> u.Quantity:
        """the maximum separation in AU"""
        return (1 + self.eccentricity) * self.average_orbital_radius

    @property
    def orbital_period(self):
        """the orbital period in earth years"""
        # watch out for unit of mass i.e. planets
        np.sqrt(self.average_orbital_radius ** 3 /
                (self.parent_body.mass + self.mass.to(u.M_sun)))

    @property
    def eccentricity_bounds(self) -> model.bounds.ValueBounds:
        """value range for eccentricity"""
        return self._eccentricity_bounds

    @eccentricity.setter
    def eccentricity(self, value):
        self._set_bounded_property('eccentricity', value)

    def __init__(self, parent_body):
        self._parent_body = parent_body
