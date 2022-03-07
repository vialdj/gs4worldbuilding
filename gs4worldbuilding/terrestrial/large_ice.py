# -*- coding: utf-8 -*-

from . import Atmosphere, Terrestrial
from .. import model
from ..random import RandomGenerator

from astropy import units as u


class LargeIce(Terrestrial):
    """the large ice world model"""
    _designation = 'Large (Ice)'
 
    class LargeIceAtmosphere(Atmosphere):
        """the large ice atmosphere model"""
        _composition = ['He', 'N2']
        _toxicity = Atmosphere.Toxicity.HIGH
        _suffocating = True

    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 230 * u.K)
    _size = Terrestrial.Size.LARGE
    _core = Terrestrial.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrographic_coverage_bounds = model.bounds.ValueBounds(0, .2)
    _absorption = .86
    _atmosphere = LargeIceAtmosphere

    def random_hydrographic_coverage(self):
        """roll of 2d-10 minimum at 0 and divided by 10"""
        self.hydrographic_coverage = max(RandomGenerator().roll2d6(-10, continuous=True) / 10, 0)

    def __init__(self, **kw):
        super(LargeIce, self).__init__(**kw)
