from . import World


class LargeChthonian(World):
    _temperature_range = World.Range(500, 950)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _absorption = .97

    def __init__(self):
        super(LargeChthonian, self).__init__()
