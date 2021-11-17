# -*- coding: utf-8 -*-

from .gas_giant import GasGiant
from .. import model, random, units

from astropy import units as u


class SmallGasGiant(GasGiant):
    """The small gas giant model"""

    _mass_bounds = model.bounds.QuantityBounds(10 * u.M_earth, 80 * u.M_earth)
    _size = GasGiant.Size.SMALL

    def random_mass(self):
        """small mass pdf fit as a truncated exponential"""
        self.mass = random.truncexpon_draw(10, 80, 17.69518578597015) * u.M_earth

    @property
    def density(self) -> u.Quantity:
        """small density in d⊕ from Gas Giant Size Table fitted as ax**b+c"""
        return (74.43464003356911 * self.mass.value ** -2.473690314600168
                + .17) * units.d_earth

