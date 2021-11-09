# -*- coding: utf-8 -*-

from . import OrbitalObject, Star
from .. import World

import numpy as np
from astropy import units as u
from scipy.stats import truncnorm


class Planet(World, OrbitalObject):

    _precedence = [*[p for p in World._precedence if p != 'temperature'],
                   'eccentricity']

    @staticmethod
    def __truncnorm_draw(lower, upper, mu, sigma):
        a, b = (lower - mu) / sigma, (upper - mu) / sigma
        return truncnorm(a, b, mu, sigma).rvs()

    def random_eccentricity(self):
        """sum of a 3d6 roll over Planetary Orbital Eccentricity Table with
modifiers if any"""
        if (self._parent_body.gas_giant_arrangement ==
            Star.GasGiantArrangement.CONVENTIONAL):
            eccentricity = self.__truncnorm_draw(0, .2, .047700000000000006,
                                                 .0432401433855162)
        else:
            eccentricity = self.__truncnorm_draw(0, .8, .20445,
                                                 .1492906477311958)
        self.eccentricity = eccentricity

    @property
    def blackbody_temperature(self) -> u.Quantity:
        """blackbody temperature in K"""
        return (278 * np.power(self.parent_body.luminosity.value,
                               (1 / 4))
                / np.sqrt(self.average_orbital_radius.value)) * u.K

    @property
    def temperature(self):
        """average temperature in K"""
        return (self.blackbody_temperature.value *
                self.blackbody_correction) * u.K

    @temperature.setter
    def temperature(self, _):
        raise AttributeError('can\'t set overriden attribute')

    def __init__(self, parent_body, average_orbital_radius):
        OrbitalObject.__init__(self, parent_body)
        self.average_orbital_radius = average_orbital_radius
