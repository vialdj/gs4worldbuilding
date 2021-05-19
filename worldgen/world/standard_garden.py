from . import Atmosphere
from . import World

import random


class StandardGarden(World):
    """the standard garden world model"""

    class StandardGardenAtmosphere(Atmosphere):
        """the standard garden atmosphere model"""
        _composition = ['N2', 'O2']

    _temperature_range = World.Range(250, 340)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .16
    _hydrosphere_range = World.Range(.5, 1)
    _atmosphere = StandardGardenAtmosphere

    @classmethod
    def random_hydrosphere(cls):
        # roll of 1d+4 divided by 10
        return random.uniform(.5, 1)

    @classmethod
    def random_atm_seed(cls):
        """sum of a 3d roll"""
        return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                         loc=10.5, scale=2.958040).rvs()

    @property
    def absorption(self):
        # match hydrosphere to Temperature Factors Table
        assert(self.hydrosphere), "attribute is not applicable"
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        return d[list(filter(lambda x: x >= self.hydrosphere, sorted(d.keys())))[0]]

    def __init__(self):
        super(StandardGarden, self).__init__()
