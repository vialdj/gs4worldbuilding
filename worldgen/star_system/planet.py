# -*- coding: utf-8 -*-

from . import OrbitalObject
from .. import World

import numpy as np


class Planet(World, OrbitalObject):

    _precedence = [*[p for p in World._precedence if p != 'temperature'],
                   'eccentricity', 'average_orbital_radius']

    @property
    def blackbody_temperature(self):
        """blackbody temperature in K"""
        return (278 * np.power(self.parent_body.luminosity,
                               (1 / 4))
                / np.sqrt(self.average_orbital_radius))

    @property
    def temperature(self):
        """average temperature in K"""
        return self.blackbody_temperature * self.blackbody_correction

    @temperature.setter
    def temperature(self, _):
        raise AttributeError('can\'t set overriden attribute')

    def __init__(self, parent_body):
        OrbitalObject.__init__(self, parent_body)
