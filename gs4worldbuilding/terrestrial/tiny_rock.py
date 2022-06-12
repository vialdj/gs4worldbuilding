from astropy import units as u

from . import Terrestrial
from .. import model


class TinyRock(Terrestrial):
    """the tiny rock world model"""
    _designation = 'Tiny (Rock)'

    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 500 * u.K)
    _size = Terrestrial.Size.TINY
    _core = Terrestrial.Core.SMALL_IRON_CORE
    _absorption = .97

    def __init__(self, **kw):
        super().__init__(**kw)
