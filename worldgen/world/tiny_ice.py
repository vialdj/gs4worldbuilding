from . import Range
from . import World


class TinyIce(World):
    _temperature_range = Range(80, 140)
    _size = World.Size.TINY
    _core = World.Core.ICY_CORE
    _absorption = .86

    def __init__(self):
        super(TinyIce, self).__init__()
