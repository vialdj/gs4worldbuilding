# -*- coding: utf-8 -*-

from ..random import roll1d6, roll3d6
from .. import model
from . import Atmosphere, Terrestrial

from astropy import units as u


class StandardOcean(Terrestrial):
    """the standard ocean world model"""

    class StandardOceanAtmosphere(Atmosphere, model.RandomizableModel):
        """the standard ocean atmosphere model"""
        _composition = ['CO2', 'N2']
        _suffocating = True
        _toxicity = None

        def randomize(self):
            """sum of a 3d roll to define toxicity if value > 12"""
            if roll3d6() > 12:
                self._toxicity = Atmosphere.Toxicity.MILD
            else:
                self._toxicity = None

    _temperature_bounds = model.bounds.QuantityBounds(250 * u.K, 340 * u.K)
    _size = Terrestrial.Size.STANDARD
    _core = Terrestrial.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .16
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(.5, 1)
    _atmosphere = StandardOceanAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 1d+4 divided by 10"""
        self.hydrographic_coverage = roll1d6(4, continuous=True) / 10

    @property
    def absorption(self):
        """absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d"""
        return (-0.7500000000000038 * self.hydrographic_coverage ** 3 +
                1.2000000000000057 * self.hydrographic_coverage ** 2 -
                0.6475000000000023 * self.hydrographic_coverage +
                1.0375000000000003)

    def __init__(self, **kw):
        super(StandardOcean, self).__init__(**kw)
