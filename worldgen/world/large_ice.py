# -*- coding: utf-8 -*-

from . import Atmosphere, World
from .. import model

from astropy import units as u


class LargeIce(World):
    """the large ice world model"""

    class LargeIceAtmosphere(Atmosphere):
        """the large ice atmosphere model"""
        _composition = ['He', 'N2']
        _toxicity = Atmosphere.Toxicity.HIGH
        _suffocating = True

    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 230 * u.K)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrosphere_bounds = model.bounds.ValueBounds(0, .2)
    _absorption = .86
    _atmosphere = LargeIceAtmosphere

    def random_hydrosphere(self):
        """roll of 2d-10 minimum at 0 and divided by 10"""
        self.hydrosphere = max(roll2d(-10) / 10, 0)

    def __init__(self):
        super(LargeIce, self).__init__()
