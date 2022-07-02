from astropy import units as u

from gs4worldbuilding.terrestrial import Terrestrial, Size, Core
from gs4worldbuilding.model.bounds import QuantityBounds


class TinyIce(Terrestrial):
    '''the tiny ice world model'''
    _temperature_bounds = QuantityBounds(80 * u.K, 140 * u.K)
    _size = Size.TINY
    _core = Core.ICY_CORE
    _absorption = .86

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
