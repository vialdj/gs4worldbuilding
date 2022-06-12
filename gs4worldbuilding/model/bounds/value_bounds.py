from enum import Enum
from ordered_enum import OrderedEnum

import numpy as np

from .bounds import Bounds


class ValueBounds(Bounds):

    def normalize(self, value):
        if isinstance(value, Enum) or isinstance(value, bool):
            return value
        if np.isnan(value):
            raise ValueError('can\'t normalize nan in bounds')
        return (value - self.lower) / (self.upper - self.lower)

    def scale(self, value):
        if isinstance(value, OrderedEnum) or isinstance(value, bool):
            return min(max(value, self.lower), self.upper)
        return value * (self.upper - self.lower) + self.lower

    def __str__(self):
        if isinstance(self.lower, Enum):
            return f'[{self.lower.name}, {self.upper.name}]'
        else:
            return f'[{self.lower:.4g}, {self.upper:.4g}]'
