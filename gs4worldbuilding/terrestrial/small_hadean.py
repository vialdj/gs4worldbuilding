from astropy import units as u

from gs4worldbuilding.terrestrial import Terrestrial, Size, Core
from gs4worldbuilding.model.bounds import QuantityBounds


class SmallHadean(Terrestrial):
    '''The small hadean world model'''
    _temperature_bounds = QuantityBounds(50 * u.K, 80 * u.K)
    _size = Size.SMALL
    _core = Core.ICY_CORE
    _absorption = .67

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
