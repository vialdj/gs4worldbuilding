# -*- coding: utf-8 -*-

from .bounds import Bounds

from enum import Enum

import numpy as np


class ValueBounds(Bounds):

    def normalize(self, value):
        if issubclass(type(value), Enum) or type(value) is bool:
            return value
        if np.isnan(value):
            raise ValueError('can\'t normalize nan in bounds')
        return (value - self.min) / (self.max - self.min)

    def scale(self, value):
        if issubclass(type(value), Enum) or type(value) is bool:
            return min(max(value, self.min), self.max)
        return value * (self.max - self.min) + self.min

    def __str__(self):
        if issubclass(type(self.min), Enum):
            return '[{}, {}]'.format(self.min.name, self.max.name)
        else:
            return '[{:.4g}, {:.4g}]'.format(self.min, self.max)
