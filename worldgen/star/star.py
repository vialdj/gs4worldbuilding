# -*- coding: utf-8 -*-

from .. import Range, RandomizableModel

import random

import numpy as np


class Star(RandomizableModel):
    """the star model"""

    def _set_ranged_property(self, prop, value):
        """centralised setter for ranged value properties"""
        rng = getattr(self, '{}_range'.format(prop))
        if not rng:
            raise AttributeError('can\'t set attribute, no {}_range found'
                                 .format(prop))
        if np.isnan(value):
            raise ValueError('can\'t manually set {} value to nan'.format(prop))
        if value < rng.min or value > rng.max:
            raise ValueError('{} value out of range {}'
                             .format(prop, rng))
        setattr(self, '_{}'.format(prop), value)

    @staticmethod
    def random_mass():
        """consecutive sum of a 3d roll times over Stellar Mass Table"""
        mass_distribution = {2: 0.002315, 1.9: 0.002315, 1.8: 0.003601121,
                             1.7: 0.005080129, 1.6: 0.00520875,
                             1.5: 0.004501471, 1.45: 0.009388529,
                             1.4: 0.006687757, 1.35: 0.007202243,
                             1.3: 0.007502452, 1.25: 0.009860048,
                             1.2: 0.0057875, 1.15: 0.011146262,
                             1.10: 0.012003738, 1.05: 0.011252058,
                             1: 0.014787942, 0.95: 0.00868,
                             0.9: 0.016716986, 0.85: 0.018003014,
                             0.8: 0.015753529, 0.75: 0.020703971,
                             0.7: 0.0121525, 0.65: 0.023404743,
                             0.6: 0.025205257, 0.55: 0.030006752,
                             0.5: 0.042330748, 0.45: 0.0434025,
                             0.4: 0.0324075, 0.35: 0.0457175,
                             0.3: 0.046875, 0.25: 0.125,
                             0.2: 0.11574, 0.15: 0.09722,
                             0.1: 0.16204}
        return random.choices(mass_distribution.keys(),
                              weights=mass_distribution.values, k=1)[0]

    @property
    def mass(self):
        return self._mass

    @property
    def mass_range(self):
        return Range(.1, 2)

    @mass.setter
    def mass(self, value):
        self._set_ranged_property('mass', value)

    def __init__(self):
        self.randomize(['mass'])

    def __iter__(self):
        """yield property names and values"""
        for prop in list(filter(lambda x: hasattr(type(self), x)
                         and isinstance(getattr(type(self), x), property),
                         dir(self))):
            yield prop, getattr(self, prop)

    def __str__(self):
        return ('{{class: {}, {}}}'.format(self.__class__.__name__,
                                           ', '.join(['{}: {!s}'.format(prop, value)
                                                     for prop, value in self])))
