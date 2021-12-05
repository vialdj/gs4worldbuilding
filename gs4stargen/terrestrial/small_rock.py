# -*- coding: utf-8 -*-

from . import Terrestrial
from .. import model

from astropy import units as u


class SmallRock(Terrestrial):
    """the small rock world model"""

    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 500 * u.K)
    _size = Terrestrial.Size.SMALL
    _core = Terrestrial.Core.SMALL_IRON_CORE
    _absorption = .96

    def __init__(self, **kw):
        super(SmallRock, self).__init__(**kw)
