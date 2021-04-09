from . import World

import numpy as np


class LargeIce(World):
    _temperature_range = World.Range(80, 230)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrosphere_range = World.Range(0, .2)
    _absorption = .86
    _atmosphere = ['He', 'N2']

    @classmethod
    def random_hydrosphere(cls):
        # roll of 2d-10 minimum at 0 and divided by 10
        return max(np.random.triangular(-.8, -.3, .2), 0)

    def __init__(self):
        super(LargeIce, self).__init__()
