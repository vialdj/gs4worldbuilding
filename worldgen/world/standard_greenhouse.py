# -*- coding: utf-8 -*-

from . import Atmosphere, World
from .. import model
from ..random import roll2d

import numpy as np

from astropy import units as u


class StandardGreenhouse(World):
    """the standard greenhouse world model"""

    class StandardGreenhouseAtmosphere(Atmosphere):
        """the standard greenhouse atmosphere model"""
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True
        _corrosive = True

        @property
        def composition(self):
            return ['CO2'] if self._world.hydrosphere < .1 else ['N2', 'H2O',
                                                                 'O2']

    _temperature_bounds = model.bounds.QuantityBounds(500 * u.K, 950 * u.K)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 100
    _greenhouse_factor = 2.0
    _hydrosphere_bounds = model.bounds.ValueBounds(0, .5)
    _absorption = .77
    _atmosphere = StandardGreenhouseAtmosphere

    def random_hydrosphere(self):
        """roll of 2d-7 minimum at 0 and divided by 10"""
        self.hydrosphere = max(roll2d(-7) / 10, 0)

    def __init__(self, **kw):
        super(StandardGreenhouse, self).__init__(**kw)
