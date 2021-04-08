from . import World

import numpy as np


class LargeGreenhouse(World):
    _temperature_range = World.Range(500, 950)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 500
    _greenhouse_factor = 2.0
    _hydrosphere_range = World.Range(0, .5)
    _absorption = .77
    _atmosphere = ['CO2']

    @classmethod
    def random_hydrosphere(cls):
        # roll of 2d-7 minimum at 0 and divided by 10
        return max(np.random.triangular(-.5, 0, .5), 0)

    @property
    def atmosphere(self):
        return ['CO2'] if self.hydrosphere < .1 else ['N2', 'H2O', 'O2']

    def __init__(self):
        super(LargeGreenhouse, self).__init__()
