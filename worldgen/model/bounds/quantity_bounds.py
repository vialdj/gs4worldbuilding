# -*- coding: utf-8 -*-

from .bounds import Bounds

from astropy import units as u


class QuantityBounds(Bounds):

    def normalize(self, value):
        return ((value.value - self.min.value) /
                (self.max.value - self.min.value))

    def scale(self, value):
        return value * (self.max.value - self.min.value) + self.min.value

    def __str__(self):
        return '[{:.4g}, {:.4g}] {}'.format(self.min.value, self.max.value,
                                            self.min.unit)

    def __init__(self, min: u.Quantity, max: u.Quantity):
        if type(min) is not u.Quantity or type(max) is not u.Quantity:
            raise ValueError('Expected quantity values')
        physical_type = min.unit.physical_type
        if physical_type not in max.unit.physical_type:
            raise ValueError('inconsistent physical type %s and %s' %
                             (physical_type, max.unit.physical_type))
        super(QuantityBounds, self).__init__(min, max)
