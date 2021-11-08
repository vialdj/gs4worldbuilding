# -*- coding: utf-8 -*-

from . import World
from .. import model

from astropy import units as u


class TinyRock(World):
    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 500 * u.K)
    _size = World.Size.TINY
    _core = World.Core.SMALL_IRON_CORE
    _absorption = .97

    def __init__(self):
        super(TinyRock, self).__init__()
