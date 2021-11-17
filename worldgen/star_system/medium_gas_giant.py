# -*- coding: utf-8 -*-

from .gas_giant import GasGiant
from .. import model, random, units

from astropy import units as u


class MediumGasGiant(GasGiant):
    """The medium gas giant model"""

    _mass_bounds = model.bounds.QuantityBounds(100 * u.M_earth, 500 * u.M_earth)
    _size = GasGiant.Size.MEDIUM

    def random_mass(self):
        """medium mass pdf fit as a truncated normal"""
        self.mass = random.truncexpon_draw(100, 500, 102.41483046902924) * u.M_earth

    @property
    def density(self) -> u.Quantity:
        """medium density in d⊕ from Gas Giant Size Table fitted as ax+b"""
        return (.0002766666669434452 * self.mass.value + .15033333325029977) * units.d_earth

