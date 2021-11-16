# -*- coding: utf-8 -*-

from . import World
from .. import model

from astropy import units as u


class TinySulfur(World):
    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 140 * u.K)
    _size = World.Size.TINY
    _core = World.Core.ICY_CORE
    _absorption = .77

    def __init__(self, **kw):
        super(TinySulfur, self).__init__(**kw)
