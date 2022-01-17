# -*- coding: utf-8 -*-

from ..random import roll1d6, roll3d6
from .. import model
from .marginal_atmosphere import MarginalCandidate
from . import Atmosphere, Terrestrial

from astropy import units as u


class LargeGarden(Terrestrial):
    """The large garden world model"""
    _designation = 'Large (Garden)'

    class LargeGardenAtmosphere(Atmosphere, MarginalCandidate,
                                model.RandomizableModel):
        """The large garden atmosphere model"""
        _composition = ['N2', 'O2', 'He', 'Ne', 'Ar', 'Kr', 'Xe']

        def randomize(self):
            """sum of a 3d roll to apply marginal modifier if > 11"""
            if roll3d6() > 11:
                self.make_marginal()

    _temperature_bounds = model.bounds.QuantityBounds(250 * u.K, 340 * u.K)
    _size = Terrestrial.Size.LARGE
    _core = Terrestrial.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .16
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(.7, 1)
    _atmosphere = LargeGardenAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 1d+6 maxed at 10 divided by 10"""
        self.hydrographic_coverage = min(roll1d6(6, continuous=True), 10) / 10

    @property
    def absorption(self):
        """absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d"""
        return (-0.7500000000000038 * self.hydrographic_coverage ** 3 +
                1.2000000000000057 * self.hydrographic_coverage ** 2 -
                0.6475000000000023 * self.hydrographic_coverage
                + 1.0375000000000003)

    def __init__(self, **kw):
        super(LargeGarden, self).__init__(**kw)
