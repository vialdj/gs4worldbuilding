from .utils import Range
from . import World


class StandardHadean(World):
    _temperature_range = Range(50, 80)
    _size = World.Size.STANDARD
    _core = World.Core.ICY_CORE
    _absorption = .67

    def __init__(self):
        super(StandardHadean, self).__init__()
