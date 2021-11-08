# -*- coding: utf-8 -*-

from . import World
from .. import model

from astropy import units as u


class StandardHadean(World):
    _temperature_bounds = model.bounds.QuantityBounds(50 * u.K, 80 * u.K)
    _size = World.Size.STANDARD
    _core = World.Core.ICY_CORE
    _absorption = .67

    def __init__(self):
        super(StandardHadean, self).__init__()
