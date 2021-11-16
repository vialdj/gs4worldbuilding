# -*- coding: utf-8 -*-

from . import World
from .. import model

from astropy import units as u


class SmallHadean(World):
    """The small hadean world model"""

    _temperature_bounds = model.bounds.QuantityBounds(50 * u.K, 80 * u.K)
    _size = World.Size.SMALL
    _core = World.Core.ICY_CORE
    _absorption = .67

    def __init__(self, **kw):
        super(SmallHadean, self).__init__(**kw)
