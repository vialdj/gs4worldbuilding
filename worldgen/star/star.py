# -*- coding: utf-8 -*-

from .. import Range, Model

from inspect import ismethod

import numpy as np


class Star(Model):
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

    @classmethod
    def random_ressource(cls):
        return .1

    @property
    def mass(self):
        return self._mass

    @property
    def mass_range(self):
        return Range(.1, 2)

    @mass.setter
    def mass(self, value):
        self._set_ranged_property('mass', value)

    def randomize(self):
        """randomizes applicable properties values"""
        # ranged properties
        rng_props = list(filter(lambda x: hasattr(self, 'random_{}'.format(x)),
                                ['mass']))
        for prop in rng_props:
            f = getattr(type(self), 'random_{}'.format(prop))
            if getattr(self, '{}_range'.format(prop)):
                val = f() if ismethod(f) else f(self)
                setattr(self, prop, val)

    def __init__(self):
        self.randomize()

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
