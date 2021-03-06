from astropy import units as u

from . import Terrestrial
from .. import model


class SmallHadean(Terrestrial):
    """The small hadean world model"""
    _designation = 'Small (Hadean)'

    _temperature_bounds = model.bounds.QuantityBounds(50 * u.K, 80 * u.K)
    _size = Terrestrial.Size.SMALL
    _core = Terrestrial.Core.ICY_CORE
    _absorption = .67

    def __init__(self, **kw):
        super().__init__(**kw)
