# -*- coding: utf-8 -*-

from . import Range

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