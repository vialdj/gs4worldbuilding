from . import World


class SmallHadean(World):
    """The small hadean world model"""

    _temperature_range = World.Range(50, 80)
    _size = World.Size.SMALL
    _core = World.Core.ICY_CORE
    _absorption = .67

    def __init__(self):
        super(SmallHadean, self).__init__()
