from astropy import units as u

from gs4worldbuilding.terrestrial import Terrestrial, Size, Core
from gs4worldbuilding.model.bounds import QuantityBounds


class LargeChthonian(Terrestrial):
    '''The large chthonian world model'''
    _temperature_bounds = QuantityBounds(500 * u.K, 950 * u.K)
    _size = Size.LARGE
    _core = Core.LARGE_IRON_CORE
    _absorption = .97

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
