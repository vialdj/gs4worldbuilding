from .. import Range
from . import World


class StandardChthonian(World):
    """the standard chthonian world model"""

    _temperature_range = Range(500, 950)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _absorption = .97

    def __init__(self):
        super(StandardChthonian, self).__init__()
