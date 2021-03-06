from astropy import units as u

from . import Terrestrial
from .. import model


class TinyIce(Terrestrial):
    """the tiny ice world model"""
    _designation = 'Tiny (Ice)'

    _temperature_bounds = model.bounds.QuantityBounds(80 * u.K, 140 * u.K)
    _size = Terrestrial.Size.TINY
    _core = Terrestrial.Core.ICY_CORE
    _absorption = .86

    def __init__(self, **kw):
        super().__init__(**kw)
