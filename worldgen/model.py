# -*- coding: utf-8 -*-

from inspect import ismethod

import numpy as np


class Model(object):
    """the Model class"""

    def _set_ranged_property(self, prop, value):
        """setter for ranged value properties"""
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


class RandomizableModel(Model):
    """the Randomizable model specialization"""

    def randomize(self, precedence):
        """randomizes applicable properties values with precedence constraints"""
        # ranged properties
        rng_props = list(filter(lambda x: hasattr(self, 'random_{}'.format(x)),
                                precedence))
        for prop in rng_props:
            f = getattr(type(self), 'random_{}'.format(prop))
            if getattr(self, '{}_range'.format(prop)):
                val = f() if ismethod(f) else f(self)
                setattr(self, prop, val)
