# -*- coding: utf-8 -*-

from . import TerrestrialWorld
from .. import model

from astropy import units as u


class StandardChthonian(TerrestrialWorld):
    """the standard chthonian world model"""

    _designation = "Standard (Chthonian)"
    _temperature_bounds = model.bounds.QuantityBounds(500 * u.K, 950 * u.K)
    _size = TerrestrialWorld.Size.STANDARD
    _core = TerrestrialWorld.Core.LARGE_IRON_CORE
    _absorption = .97

    def __init__(self, **kw):
        super(StandardChthonian, self).__init__(**kw)
