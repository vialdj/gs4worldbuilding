# -*- coding: utf-8 -*-

from .. import model
from .marginal_atmosphere import MarginalCandidate
from . import Atmosphere, World

from random import uniform

from astropy import units as u


class StandardGarden(World):
    """the standard garden world model"""

    class StandardGardenAtmosphere(Atmosphere, MarginalCandidate,
                                   model.RandomizableModel):
        """the standard garden atmosphere model"""
        _composition = ['N2', 'O2']

        def randomize(self):
            """sum of a 3d roll to apply marginal modifier if > 11"""
            if uniform(0, 1) < .375:
                self.make_marginal()
            else:
                self.remove_marginal()

    _temperature_bounds = model.bounds.QuantityBounds(250 * u.K, 340 * u.K)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .16
    _hydrosphere_bounds = model.bounds.ValueBounds(.5, 1)
    _atmosphere = StandardGardenAtmosphere

    def random_hydrosphere(self):
        """roll of 1d+4 divided by 10"""
        self.hydrosphere = uniform(.5, 1)

    @property
    def absorption(self):
        """absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d"""
        return (-0.7500000000000038 * self.hydrosphere ** 3 +
                1.2000000000000057 * self.hydrosphere ** 2 -
                0.6475000000000023 * self.hydrosphere + 1.0375000000000003)

    def __init__(self, **kw):
        super(StandardGarden, self).__init__(**kw)
