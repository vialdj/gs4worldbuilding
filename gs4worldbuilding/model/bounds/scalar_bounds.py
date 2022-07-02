from typing import TypeVar

import numpy as np

from gs4worldbuilding.model.bounds import Bounds


ST = TypeVar('ST', int, float)


class ScalarBounds(Bounds[ST]):
    '''Bounds for scalar values'''

    def normalize(self, value: ST):
        '''Normalize value'''
        if np.isnan(value):
            raise ValueError("can't normalize nan in bounds")
        return (value - self.lower) / (self.upper - self.lower)

    def scale(self, value):
        '''Scale value in range'''
        return value * (self.upper - self.lower) + self.lower

    def __str__(self):
        return f'[{self.lower:.4g}, {self.upper:.4g}]'

    def __init__(self, lower: ST, upper: ST):
        super().__init__(lower, upper)
