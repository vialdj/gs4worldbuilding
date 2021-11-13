# -*- coding: utf-8 -*-

from . import GasGiant
from .. import model

from astropy import units as u
from scipy.stats import truncnorm


class SmallGasGiant(GasGiant):
    """The small hadean world model"""

    _mass_bounds = model.bounds.QuantityBounds(10 * u.M_earth, 80 * u.M_earth)
    _size = GasGiant.Size.SMALL

    @staticmethod
    def __truncnorm_draw(lower, upper, mu, sigma):
        a, b = (lower - mu) / sigma, (upper - mu) / sigma
        return truncnorm(a, b, mu, sigma).rvs()

    def random_mass(self):
        """small mass pdf fit as a truncated normal"""
        self.mass = (self.__truncnorm_draw(10, 80, 10, 17.69518578597015)
                     * u.M_earth)

    @property
    def density(self) -> u.Quantity:
        """small density in d⊕ from Gas Giant Size Table fitted as ax**b+c"""
        return (74.43464003356911 * self.mass.value ** -2.473690314600168
                + .17) * u.d_earth

    def __init__(self, **kw):
        super(GasGiant, self).__init__(**kw)
