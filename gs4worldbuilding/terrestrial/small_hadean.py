# -*- coding: utf-8 -*-

from . import Terrestrial
from .. import model

from astropy import units as u


class SmallHadean(Terrestrial):
    """The small hadean world model"""
    _designation = 'Small (Hadean)'

    _temperature_bounds = model.bounds.QuantityBounds(50 * u.K, 80 * u.K)
    _size = Terrestrial.Size.SMALL
    _core = Terrestrial.Core.ICY_CORE
    _absorption = .67

    def __init__(self, **kw):
        super(SmallHadean, self).__init__(**kw)
