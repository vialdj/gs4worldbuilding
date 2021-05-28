from . import Range
from . import World


class TinyRock(World):
    _temperature_range = Range(140, 500)
    _size = World.Size.TINY
    _core = World.Core.SMALL_IRON_CORE
    _absorption = .97

    def __init__(self):
        super(TinyRock, self).__init__()
