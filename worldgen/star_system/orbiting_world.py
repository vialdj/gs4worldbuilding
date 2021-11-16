# -*- coding: utf-8 -*-

from . import OrbitalObject
from .. import (World,
                TinyIce, TinyRock,
                SmallHadean, SmallIce, SmallRock,
                StandardHadean, StandardIce, StandardOcean, StandardGreenhouse, StandardChthonian,
                LargeIce, LargeOcean, LargeGreenhouse, LargeChthonian)
from ..random import truncnorm_draw

import numpy as np
from astropy import units as u
from scipy.stats import truncnorm


def make_world(parent_body, average_orbital_radius: u.Quantity,
               size: World.Size):
    bb_temp = (278 * np.power(parent_body.luminosity.value, (1 / 4))
               / np.sqrt(average_orbital_radius.value)) * u.K
    types = {}
    if size == World.Size.SMALL:
        types = {0 * u.K: SmallHadean,
                 81 * u.K: SmallIce,
                 141 * u.K: SmallRock}
    elif size == World.Size.STANDARD:
        types = {0 * u.K: StandardHadean,
                 81 * u.K: StandardIce,
                 241 * u.K: StandardOcean,
                 321 * u.K: StandardGreenhouse,
                 501 * u.K: StandardChthonian}
    elif size == World.Size.LARGE:
        types = {0 * u.K: LargeIce,
                 241 * u.K: LargeOcean,
                 321 * u.K: LargeGreenhouse,
                 501 * u.K: LargeChthonian}

    world_type = None
    if size == World.Size.TINY:
        world_type = TinyIce if bb_temp <= 140 * u.K else TinyRock
    else:
        world_type = list(filter(lambda x: bb_temp >= x[0], types.items()))[-1][1]

    orbiting_world_type = orbiting_world(world_type)
    return orbiting_world_type(parent_body, average_orbital_radius)


def orbiting_world(world_type):

    class OrbitingWorld(world_type, OrbitalObject):

        _precedence = [*[p for p in World._precedence if p != 'temperature'],
                       'eccentricity']

        def random_eccentricity(self):
            """sum of a 3d6 roll over Planetary Orbital Eccentricity Table with
    modifiers if any"""
            self.eccentricity = truncnorm_draw(0, .8, .20445, .1492906477311958)

        @property
        def blackbody_temperature(self) -> u.Quantity:
            """blackbody temperature in K"""
            return (278 * np.power(self._parent_body.luminosity.value, (1 / 4))
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
            self.average_orbital_radius = average_orbital_radius
            self._parent_body = parent_body
            super(OrbitingWorld, self).__init__(parent_body=parent_body)

    return OrbitingWorld
