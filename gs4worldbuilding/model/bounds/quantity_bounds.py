from astropy import units as u

from .bounds import Bounds


class QuantityBounds(Bounds):

    def normalize(self, value):
        return ((value.value - self.lower.value) /
                (self.upper.value - self.lower.value))

    def scale(self, value):
        return value * (self.upper - self.lower) + self.lower

    def __str__(self):
        return (f'[{self.lower.value:.4g}, {self.upper.value:.4g}] ' +
                f'{self.lower.unit}')

    def __init__(self, lower: u.Quantity, upper: u.Quantity):
        if not (isinstance(lower, u.Quantity) and
                isinstance(upper, u.Quantity)):
            raise ValueError('Expected quantity values')
        physical_type = lower.unit.physical_type
        if physical_type not in upper.unit.physical_type:
            raise ValueError(f'inconsistent physical type {physical_type} ' +
                             f'and {upper.unit.physical_type}')
        super().__init__(lower, upper)
