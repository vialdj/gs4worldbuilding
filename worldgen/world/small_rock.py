# -*- coding: utf-8 -*-

from . import World
from .. import model

from astropy import units as u


class SmallRock(World):
    """the small rock world model"""

    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 500 * u.K)
    _size = World.Size.SMALL
    _core = World.Core.SMALL_IRON_CORE
    _absorption = .96

    def __init__(self):
        super(SmallRock, self).__init__()
