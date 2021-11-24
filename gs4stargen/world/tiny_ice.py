# -*- coding: utf-8 -*-

from . import TerrestrialWorld
from .. import model

from astropy import units as u


class TinyIce(TerrestrialWorld):
    _designation = "Tiny (Ice)"
    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 140 * u.K)
    _size = TerrestrialWorld.Size.TINY
    _core = TerrestrialWorld.Core.ICY_CORE
    _absorption = .86

    def __init__(self, **kw):
        super(TinyIce, self).__init__(**kw)
