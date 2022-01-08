# -*- coding: utf-8 -*-

from . import Terrestrial
from .. import model

from astropy import units as u


class TinySulfur(Terrestrial):
    """the tiny sulfur world model"""
    _designation = 'Tiny (Sulfur)'

    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 140 * u.K)
    _size = Terrestrial.Size.TINY
    _core = Terrestrial.Core.ICY_CORE
    _absorption = .77

    def __init__(self, **kw):
        super(TinySulfur, self).__init__(**kw)
