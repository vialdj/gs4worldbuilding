# -*- coding: utf-8 -*-

from . import Atmosphere, World
from .. import model
from ..random import roll2d

import numpy as np
from astropy import units as u


class StandardAmmonia(World):
    """the standard ammonia world model"""

    class StandardAmmoniaAtmosphere(Atmosphere):
        """the standard ammonia atmosphere model"""
        _composition = ['N2', 'NH3', 'CH4']
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True
        _corrosive = True

    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 215 * u.K)
    _size = World.Size.STANDARD
    _core = World.Core.ICY_CORE
    _pressure_factor = 1
    _greenhouse_factor = .2
    _hydrosphere_bounds = model.bounds.ValueBounds(.2, 1)
    _absorption = .84
    _atmosphere = StandardAmmoniaAtmosphere

    def random_hydrosphere(self):
        """roll of 2d maximum at 10 and divided by 10"""
        self.hydrosphere = min(roll2d() / 10, 1)

    def __init__(self, **kw):
        super(StandardAmmonia, self).__init__(**kw)
