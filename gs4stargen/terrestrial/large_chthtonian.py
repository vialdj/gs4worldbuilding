# -*- coding: utf-8 -*-

from . import Terrestrial
from .. import model

from astropy import units as u


class LargeChthonian(Terrestrial):
    """The large chthonian world model"""
    _designation = 'Large (Chthonian)'

    _temperature_bounds = model.bounds.QuantityBounds(500 * u.K, 950 * u.K)
    _size = Terrestrial.Size.LARGE
    _core = Terrestrial.Core.LARGE_IRON_CORE
    _absorption = .97

    def __init__(self, **kw):
        super(LargeChthonian, self).__init__(**kw)
