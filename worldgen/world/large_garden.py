from .utils import Range
from . import Atmosphere
from . import World

import random


class LargeGarden(World):
    """The large garden world model"""

    class LargeGardenAtmosphere(Atmosphere):
        """The large garden atmosphere model"""
        _composition = ['N2', 'O2', 'He', 'Ne', 'Ar', 'Kr', 'Xe']

    _temperature_range = Range(250, 340)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .16
    _hydrosphere_range = Range(.7, 1)
    _atmosphere = LargeGardenAtmosphere

    @classmethod
    def random_hydrosphere(cls):
        # roll of 1d+6 maxed at 10 divided by 10
        return min(random.uniform(.7, 1.2), 1)

    @property
    def absorption(self):
        # match hydrosphere to Temperature Factors Table
        assert(self.hydrosphere), "attribute is not applicable"
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        return d[list(filter(lambda x: x >= self.hydrosphere, sorted(d.keys())))[0]]

    def __init__(self):
        super(LargeGarden, self).__init__()
