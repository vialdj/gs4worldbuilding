from .. import Range
from . import World


class SmallRock(World):
    """the small rock world model"""

    _temperature_range = Range(140, 500)
    _size = World.Size.SMALL
    _core = World.Core.SMALL_IRON_CORE
    _absorption = .96

    def __init__(self):
        super(SmallRock, self).__init__()
