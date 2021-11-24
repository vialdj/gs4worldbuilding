# -*- coding: utf-8 -*-

from . import TerrestrialWorld
from .. import model

from astropy import units as u


class SmallRock(TerrestrialWorld):
    """the small rock world model"""

    _designation = "Small (Rock)"
    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 500 * u.K)
    _size = TerrestrialWorld.Size.SMALL
    _core = TerrestrialWorld.Core.SMALL_IRON_CORE
    _absorption = .96

    def __init__(self, **kw):
        super(SmallRock, self).__init__(**kw)
