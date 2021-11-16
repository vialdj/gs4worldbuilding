# -*- coding: utf-8 -*-

from . import World
from .. import model

from astropy import units as u


class StandardChthonian(World):
    """the standard chthonian world model"""

    _temperature_bounds = model.bounds.QuantityBounds(500 * u.K, 950 * u.K)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _absorption = .97

    def __init__(self, **kw):
        super(StandardChthonian, self).__init__(**kw)
