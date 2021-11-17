# -*- coding: utf-8 -*-

from .gas_giant import GasGiant
from .. import model, random, units

from astropy import units as u


class LargeGasGiant(GasGiant):
    """The large gas giant model"""

    _mass_bounds = model.bounds.QuantityBounds(600 * u.M_earth, 4000 * u.M_earth)
    _size = GasGiant.Size.LARGE

    def random_mass(self):
        """large mass pdf fit as a truncated exponential"""
        self.mass = random.truncexpon_draw(600, 4000, 872.1918137657565) * u.M_earth

    @property
    def density(self) -> u.Quantity:
        """large density in d⊕ from Gas Giant Size Table fitted as ax+b"""
        return (.0003880597018732323 * self.mass.value + .036185736947409355) * units.d_earth

