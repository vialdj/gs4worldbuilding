from astropy import units as u

from . import Terrestrial
from .. import model


class SmallRock(Terrestrial):
    """the small rock world model"""
    _designation = 'Small (Rock)'

    _temperature_bounds = model.bounds.QuantityBounds(140 * u.K, 500 * u.K)
    _size = Terrestrial.Size.SMALL
    _core = Terrestrial.Core.SMALL_IRON_CORE
    _absorption = .96

    def __init__(self, **kw):
        super().__init__(**kw)
