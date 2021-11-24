# -*- coding: utf-8 -*-

from . import TerrestrialWorld
from .. import model

from astropy import units as u


class StandardHadean(TerrestrialWorld):
    _designation = "Standard (Hadean)"
    _temperature_bounds = model.bounds.QuantityBounds(50 * u.K, 80 * u.K)
    _size = TerrestrialWorld.Size.STANDARD
    _core = TerrestrialWorld.Core.ICY_CORE
    _absorption = .67

    def __init__(self, **kw):
        super(StandardHadean, self).__init__(**kw)
