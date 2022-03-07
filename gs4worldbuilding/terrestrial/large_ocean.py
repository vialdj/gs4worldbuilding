# -*- coding: utf-8 -*-

from . import Atmosphere, Terrestrial
from .. import model
from ..random import RandomGenerator

from astropy import units as u


class LargeOcean(Terrestrial):
    """the large ocean world model"""
    _designation = 'Large (Ocean)'

    class LargeOceanAtmosphere(Atmosphere):
        """the large ocean atmosphere model"""
        _composition = ['He', 'N2']
        _toxicity = Atmosphere.Toxicity.HIGH
        _suffocating = True

    _temperature_bounds = model.bounds.QuantityBounds(250 * u.K, 340 * u.K)
    _size = Terrestrial.Size.LARGE
    _core = Terrestrial.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .16
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(.7, 1)
    _atmosphere = LargeOceanAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 1d+6 maxed at 10 divided by 10"""
        self.hydrographic_coverage = min(RandomGenerator().roll1d6(6, continuous=True), 10) / 10

    @property
    def absorption(self):
        """absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d"""
        return (-0.7500000000000038 * self.hydrographic_coverage ** 3 +
                1.2000000000000057 * self.hydrographic_coverage ** 2 -
                0.6475000000000023 * self.hydrographic_coverage +
                1.0375000000000003)

    def __init__(self, **kw):
        super(LargeOcean, self).__init__(**kw)
