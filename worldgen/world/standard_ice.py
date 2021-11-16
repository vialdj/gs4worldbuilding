# -*- coding: utf-8 -*-

from .. import model
from . import Atmosphere, World

from random import uniform

import numpy as np
from astropy import units as u


class StandardIce(World):
    """the standard ice world model"""

    class StandardIceAtmosphere(Atmosphere, model.RandomizableModel):
        """the standard ice atmosphere model"""
        _composition = ['CO2', 'N2']
        _suffocating = True

        def randomize(self):
            """sum of a 3d roll to define toxicity if value > 12"""
            if uniform(0, 1) < .7407:
                self._toxicity = Atmosphere.Toxicity.MILD

    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 230 * u.K)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .2
    _hydrosphere_bounds = model.bounds.ValueBounds(0, .2)
    _absorption = .86
    _atmosphere = StandardIceAtmosphere

    def random_hydrosphere(self):
        """roll of 2d-10 minimum at 0 and divided by 10"""
        self.hydrosphere = max(roll2d(-10) / 10, 0)

    def __init__(self):
        super(StandardIce, self).__init__()
