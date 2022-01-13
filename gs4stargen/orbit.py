# -*- coding: utf-8 -*-

from . import model, random
from .planet import Planet
from .units import D_earth

import numpy as np
from astropy import units as u


class Orbit(model.RandomizableModel):
    """the orbit model"""

    _precedence = ['eccentricity', 'inclination', 'ascending_lon', 'periapsis_arg', 'epoch_mean_anomaly']

    _eccentricity_bounds = model.bounds.ValueBounds(0, .8)
    
    def random_ascending_lon(self):
        """draw from a uniform distribution between -180 and 180"""
        self.ascending_lon = np.random.uniform(-180, 180) * u.deg

    def random_eccentricity(self):
        """sum of a 3d6 roll over Planetary Orbital Eccentricity Table with
        modifiers if any"""
        self.eccentricity = random.truncnorm_draw(0, .8, .20295,
                                                  .15273767544387992)
    def random_inclination(self):
        """draw from a Rayleigh distribution with a mode of 2"""
        self.inclination = np.random.rayleigh(2) * u.deg

    def random_epoch_mean_anomaly(self):
        """draw from a uniform distribution between 0 and 360"""
        self.epoch_mean_anomaly = np.random.uniform(0, 360) * u.deg
    
    def random_periapsis_arg(self):
        """draw from a uniform distribution between 0 and 360"""
        self.periapsis_arg = np.random.uniform(0, 360) * u.deg

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
        self._radius = value.to(u.au)

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
    def epoch_mean_anomaly(self) -> u.Quantity:
        """the mean anomaly at epoch M0 in degrees"""
        return self._epoch_mean_anomaly * u.deg

    @epoch_mean_anomaly.setter
    def epoch_mean_anomaly(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError('can\'t set mean anomaly at epoch to value of'
                             + ' %s physical type' %
                             value.unit.physical_type)
        self._epoch_mean_anomaly = value.to(u.deg)

    @property
    def inclination(self) -> u.Quantity:
        """the orbital inclination in degrees"""
        return self._inclination * u.deg

    @inclination.setter
    def inclination(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError('can\'t set inclination to value of'
                             + ' %s physical type' %
                             value.unit.physical_type)
        self._inclination = value.to(u.deg)

    @property
    def ascending_lon(self) -> u.Quantity:
        """the longitude of the ascending node Ω in degrees"""
        return self._ascending_lon * u.deg

    @ascending_lon.setter
    def ascending_lon(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError('can\'t set longitude of ascending node to value of'
                             + ' %s physical type' %
                             value.unit.physical_type)
        self._ascending_lon = value.to(u.deg)

    @property
    def min_separation(self) -> u.Quantity:
        """the minimum separation in AU"""
        return ((1 - self.eccentricity) * self.radius.value) * u.au

    @property
    def max_separation(self) -> u.Quantity:
        """the maximum separation in AU"""
        return ((1 + self.eccentricity) * self.radius.value) * u.au

    @property
    def periapsis_arg(self) -> u.Quantity:
        """the argument of periapsis ω in degrees"""
        return self._periapsis_arg * u.deg

    @periapsis_arg.setter
    def periapsis_arg(self, value: u.Quantity):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'angle' not in value.unit.physical_type:
            raise ValueError('can\'t set argument of periapsis to value of'
                             + ' %s physical type' %
                             value.unit.physical_type)
        self._periapsis_arg = value.to(u.deg)

    @property
    def period(self) -> u.Quantity:
        """the orbital period in earth years"""
        if issubclass(type(self._parent_body), Planet):
            # handling satellite orbital period
            return np.sqrt(self.radius.to(D_earth).value ** 3 /
                           (self._parent_body.mass.value +
                            self._body.mass.value)) * .166 * u.a
        else:
            return np.sqrt(self.radius.value ** 3 /
                           ((self._parent_body.mass.value +
                           self._body.mass.to(u.M_sun).value)
                           if issubclass(type(self._body), Planet)
                           else self._parent_body.mass.value)) * u.a

    def __init__(self, parent_body, radius, body=None):
        self._body = body
        self._parent_body = parent_body
        self.radius = radius

        self.randomize()
