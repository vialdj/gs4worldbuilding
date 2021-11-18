# -*- coding: utf-8 -*-

from .. import model, random

import numpy as np
from astropy import units as u


class Orbit(model.RandomizableModel):
    """the orbit model"""
    
    _precedence = ['eccentricity']

    _eccentricity_bounds = model.bounds.ValueBounds(0, .8)

    @property
    def radius(self) -> u.Quantity:
        """The average orbital radius to the parent body in AU"""
        return self._radius

    @radius.setter
    def radius(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'length' not in value.unit.physical_type:
            raise ValueError('can\'t set radius to value of %s physical type' %
                             value.unit.physical_type)
        self._radius = value

    @property
    def eccentricity(self) -> float:
        """the orbital orbit eccentricity"""
        return self._get_bounded_property('eccentricity')

    @property
    def eccentricity_bounds(self) -> model.bounds.ValueBounds:
        """value range for eccentricity"""
        return self._eccentricity_bounds
    
    def random_eccentricity(self):
        """sum of a 3d6 roll over Planetary Orbital Eccentricity Table with
        modifiers if any"""
        self.eccentricity = random.truncnorm_draw(0, .8, .20295, .15273767544387992)

    @eccentricity.setter
    def eccentricity(self, value: float):
        self._set_bounded_property('eccentricity', value)

    @property
    def min_separation(self) -> u.Quantity:
        """the minimum separation in AU"""
        return ((1 - self.eccentricity) * self.radius.value) * u.au

    @property
    def max_separation(self) -> u.Quantity:
        """the maximum separation in AU"""
        return ((1 + self.eccentricity) * self.radius.value) * u.au

    @property
    def period(self):
        """the orbital period in earth years"""
        return np.sqrt(self.radius.value ** 3 / (self._parent_body.mass.value +
                       self._body.mass.to(u.M_sun).value)) * u.a


    def __init__(self, parent_body, radius, body=None):
        self._body = body
        self._parent_body = parent_body
        self.radius = radius

        self.randomize()
