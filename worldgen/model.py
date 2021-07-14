# -*- coding: utf-8 -*-

from collections import namedtuple

import numpy as np


class Model(object):
    """the Model class"""

    class Range(namedtuple('Range', ['min', 'max'])):
        """value range named tuple"""
        def __str__(self):
            return ('[{}, {}]'.format(self.min, self.max))

    def _set_ranged_property(self, prop, value):
        """setter for ranged value properties"""
        rng = getattr(self, '{}_range'.format(prop), None)
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

    _precedence = []
    locked = False

    def randomize(self):
        """randomizes applicable properties values with precedence constraints"""
        # randomizable properties
        if not self.locked:
            props = list(filter(lambda x: hasattr(self, 'random_{}'.format(x)),
                                self._precedence))
            for prop in props:
                getattr(type(self), 'random_{}'.format(prop))(self)
