# -*- coding: utf-8 -*-

from collections import namedtuple
from enum import Enum

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
        if isinstance(value, Enum):
            value_idx = list(type(value)).index(value)
            if (value_idx < list(type(value)).index(rng.min) or
                value_idx > list(type(value)).index(rng.max)):
                raise ValueError('{} value out of range {}'
                                 .format(prop, rng))
            setattr(self, '_{}'.format(prop), value)
        else:
            if np.isnan(value):
                raise ValueError('can\'t manually set {} value to nan'
                                 .format(prop))
            if value < rng.min or value > rng.max:
                raise ValueError('{} value out of range {}'
                                 .format(prop, rng))
            setattr(self, '_{}'.format(prop), (value - rng.min) /
                                      (rng.max - rng.min))

    def _get_ranged_property(self, prop):
        """getter for ranged value properties"""
        rng = getattr(self, '{}_range'.format(prop), None)
        if not rng:
            raise AttributeError('can\'t get attribute, no {}_range found'
                                 .format(prop))
        value = getattr(self, '_{}'.format(prop))
        if isinstance(value, Enum):
            value_idx = list(type(value)).index(value)
            idx = min(max(value_idx, list(type(value)).index(rng.min)),
                      list(type(value)).index(rng.max))
            return list(type(value))[idx]
        else:
            return value * (rng.max - rng.min) + rng.min

    def __iter__(self):
        """yield property names and values"""
        for prop in list(filter(lambda x: hasattr(type(self), x)
                         and isinstance(getattr(type(self), x), property),
                         dir(self))):
            yield prop, getattr(self, prop)

    def __str__(self):
        return ('{{class: {}, {}}}'
                .format(self.__class__.__name__,
                        ', '.join(['{}: {!s}'.format(prop, value)
                                  for prop, value in self])))


class RandomizableModel(Model):
    """the Randomizable model specialization"""

    _precedence = []
    locked = False

    def randomize(self):
        """randomizes applicable properties values with precedence
constraints"""
        # randomizable properties
        if not self.locked:
            props = list(filter(lambda x: hasattr(self, 'random_{}'.format(x)),
                                self._precedence))
            for prop in props:
                getattr(type(self), 'random_{}'.format(prop))(self)
