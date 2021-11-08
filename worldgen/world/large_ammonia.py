# -*- coding: utf-8 -*-

from . import Atmosphere, World
from .. import model

import numpy as np

from astropy import units as u


class LargeAmmonia(World):
    """The large ammonia world model"""

    class LargeAmmoniaAtmosphere(Atmosphere):
        """The large ammonia atmosphere model"""
        _composition = ['He', 'NH3', 'CH4']
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True
        _corrosive = True

    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 215 * u.K)
    _size = World.Size.LARGE
    _core = World.Core.ICY_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrosphere_bounds = model.bounds.ValueBounds(.2, 1)
    _absorption = .84
    _atmosphere = LargeAmmoniaAtmosphere

    def random_hydrosphere(self):
        """roll of 2d capped at 10 and divided by 10"""
        self.hydrosphere = min(np.random.triangular(0.2, .7, 1.2), 1)

    def __init__(self):
        super(LargeAmmonia, self).__init__()
