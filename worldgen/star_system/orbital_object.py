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
        return self._average_orbital_radius

    @average_orbital_radius.setter
    def average_orbital_radius(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'length' not in value.unit.physical_type:
            raise ValueError('can\'t set average orbital radius to value of %s physical type' %
                             value.unit.physical_type)
        self._average_orbital_radius = value

    @property
    def eccentricity(self) -> float:
        """the orbital orbit eccentricity"""
        return self._get_bounded_property('eccentricity')

    @property
    def eccentricity_bounds(self) -> model.bounds.ValueBounds:
        """value range for eccentricity"""
        return self._eccentricity_bounds

    @eccentricity.setter
    def eccentricity(self, value: float):
        self._set_bounded_property('eccentricity', value)

    @property
    def minimum_separation(self) -> u.Quantity:
        """the minimum separation in AU"""
        return ((1 - self.eccentricity) * self.average_orbital_radius.value) * u.au

    @property
    def maximum_separation(self) -> u.Quantity:
        """the maximum separation in AU"""
        return ((1 + self.eccentricity) * self.average_orbital_radius.value) * u.au

    @property
    def orbital_period(self):
        """the orbital period in earth years"""
        # watch out for unit of mass i.e. planets
        return np.sqrt(
                self.average_orbital_radius.value ** 3 /
                (self._parent_body.mass.value +
                 self.mass.to(u.M_sun).value)
               ) * u.a


    def __init__(self, parent_body, **kw):
        self._parent_body = parent_body
