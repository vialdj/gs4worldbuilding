from . import Range
from . import World


class TinySulfur(World):
    _temperature_range = Range(80, 140)
    _size = World.Size.TINY
    _core = World.Core.ICY_CORE
    _absorption = .77

    def __init__(self):
        super(TinySulfur, self).__init__()
