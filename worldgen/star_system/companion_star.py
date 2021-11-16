# -*- coding: utf-8 -*-

from . import OrbitalObject, Star
from .. import model
from ..random import truncnorm_draw, truncexpon_draw, roll2d

import random
import enum

import numpy as np
from ordered_enum.ordered_enum import ValueOrderedEnum
from astropy import units as u


class CompanionStar(Star, OrbitalObject):

    _precedence = [*Star._precedence, 'separation', 'eccentricity',
                   'average_orbital_radius']

    @enum.unique
    class Separation(u.Quantity, ValueOrderedEnum):
        """class Separation Enum from Orbital Separation Table with
radius multiplier in AU"""
        VERY_CLOSE = .05 * u.au
        CLOSE = .5 * u.au
        MODERATE = 2 * u.au
        WIDE = 10 * u.au
        DISTANT = 50 * u.au

    def random_seed_mass(self):
        """campanion star random mass procedure"""
        mass = self._parent_body.mass.value
        # roll 1d6 - 1
        r = random.randint(0, 5)
        if r >= 1:
            # sum of nd6 roll
            s = sum([random.randint(1, 6) for _ in range(r)])
            for _ in range(s):
                # count down on the stellar mass table
                mass -= (.05 if mass else .10)
        # add noise to value
        n = .025 if mass <= 1.5 else .05
        mass += random.uniform(-n, n)
        # mass in [.1, parent_body.mass] range
        self.seed_mass = min(max(.1, mass) * u.M_sun, self._parent_body.mass)

    def random_separation(self):
        """sum of a 3d6 roll over Orbital Separation Table"""
        self.separation = random.choices(list(self.Separation),
                                         weights=self._separation_dist,
                                         k=1)[0]


    def random_eccentricity(self):
        """sum of a 3d6 roll over Stellar Orbital Eccentricity Table with
modifiers if any"""
        match self.separation:
            case self.Separation.MODERATE:
                self.eccentricity = truncnorm_draw(0, .8, .4151, .16553546447815948)
            case self.Separation.CLOSE:
                self.eccentricity = truncnorm_draw(0, .7, .3055, .1839014681833726)
            case self.Separation.VERY_CLOSE:
                self.eccentricity = truncexpon_draw(0, .6, .1819450191678794)
            case _:
                self.ecccentricity = truncnorm_draw(0, .95, .5204, .142456449485448)

    def random_average_orbital_radius(self):
        """roll of 2d6 multiplied by the separation category radius"""
        self.average_orbital_radius = roll2d() * self.separation.value * u.au)

    @property
    def seed_mass_bounds(self) -> model.bounds.QuantityBounds:
        """value range for mass adjusted so mass cannot be greater than parent
body mass"""
        # TODO: enforce final mass range to be no more than parent mass (not seed mass)
        return model.bounds.QuantityBounds(.1 * u.M_sun, 2 * u.M_sun)

    @property
    def separation(self) -> Separation:
        """separation category over Orbital Separation Table"""
        return self._get_bounded_property('separation')

    @property
    def separation_bounds(self) -> model.bounds.ValueBounds:
        """resource range class variable"""
        return (self._separation_bounds if hasattr(self, '_separation_bounds')
                else model.bounds.ValueBounds(self.Separation.VERY_CLOSE,
                                              self.Separation.DISTANT))

    @separation.setter
    def separation(self, value):
        if not isinstance(value, self.Separation):
            raise ValueError('separation value type must be {}'
                             .format(self.Separation))
        self._set_bounded_property('separation', value)

    @property
    def eccentricity_bounds(self) -> model.bounds.ValueBounds:
        """value range for eccentricity dependant on parent star separation"""
        rngs = {self.Separation.MODERATE: model.bounds.ValueBounds(0, .8),
                self.Separation.CLOSE: model.bounds.ValueBounds(0, .7),
                self.Separation.VERY_CLOSE: model.bounds.ValueBounds(0, .6)}
        return (rngs[self.separation] if self.separation in rngs.keys() else
                model.bounds.ValueBounds(0, .95))

    @property
    def average_orbital_radius(self) -> u.Quantity:
        """The average orbital radius to the parent body in AU"""
        return self._get_bounded_property('average_orbital_radius') * u.au

    @property
    def average_orbital_radius_bounds(self) -> model.bounds.QuantityBounds:
        """value range for average orbital radius"""
        return model.bounds.QuantityBounds(2 * self.separation.value * u.au,
                                           12 * self.separation.value * u.au)

    @average_orbital_radius.setter
    def average_orbital_radius(self, value):
        if not isinstance(value, u.Quantity):
            raise ValueError('expected quantity type value')
        if 'length' not in value.unit.physical_type:
            raise ValueError('can\'t set average orbital radius to value of %s physical type' %
                             value.unit.physical_type)
        self._set_bounded_property('average_orbital_radius', value)


    @property
    def forbidden_zone(self) -> model.bounds.QuantityBounds:
        """the forbidden zone limits in AU if any"""
        if isinstance(self._companions[0], Star):
            return model.bounds.QuantityBounds(self.minimum_separation / 3,
                                               self.maximum_separation * 3)
        return super.forbidden_zone

    def __init__(self, star_system, parent_body, tertiary_star=False,
                 sub_companion=False):
        if not sub_companion:
            if star_system.garden_host and tertiary_star:
                self._separation_dist = [0, 0, 0, .01851851851853,
                                         .98148148148193]
                self._separation_bounds = model.bounds.ValueBounds(
                                            self.Separation.WIDE,
                                            self.Separation.DISTANT
                                          )
            elif star_system.garden_host:
                self._separation_dist = [0, .0463, .11574, .33796, .5]
                self._separation_bounds = model.bounds.ValueBounds(
                                            self.Separation.CLOSE,
                                            self.Separation.DISTANT
                                          )
            elif tertiary_star:
                self._separation_dist = [0, .00462963, .041666667, .212962963,
                                         .740740741]
                self._separation_bounds = model.bounds.ValueBounds(
                                            self.Separation.CLOSE,
                                            self.Separation.DISTANT
                                          )
            else:
                self._separation_dist = [.0926, .2824, .25, .2824, .0926]
        else:
            self._separation_dist = [.740740741, .212962963, .041666667,
                                     .00462963, 0]
            self._separation_bounds = model.bounds.ValueBounds(
                                        self.Separation.VERY_CLOSE,
                                        self.Separation.WIDE
                                      )
        OrbitalObject.__init__(self, parent_body)
        Star.__init__(self, star_system)
