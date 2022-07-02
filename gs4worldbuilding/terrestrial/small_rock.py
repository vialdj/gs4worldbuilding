from astropy import units as u

from gs4worldbuilding.terrestrial import Terrestrial, Size, Core
from gs4worldbuilding.model.bounds import QuantityBounds


class SmallRock(Terrestrial):
    '''the small rock world model'''
    _temperature_bounds = QuantityBounds(140 * u.K, 500 * u.K)
    _size = Size.SMALL
    _core = Core.SMALL_IRON_CORE
    _absorption = .96

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
