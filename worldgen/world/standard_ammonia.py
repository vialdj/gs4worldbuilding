from . import World

import numpy as np


class StandardAmmonia(World):
    _temperature_range = World.Range(140, 215)
    _size = World.Size.STANDARD
    _core = World.Core.ICY_CORE
    _pressure_factor = 1
    _greenhouse_factor = .2
    _hydrosphere_range = World.Range(.2, 1)
    _absorption = .84
    _atmosphere = ['N2', 'NH3', 'CH4']

    @classmethod
    def random_hydrosphere(cls):
        # roll of 2d maximum at 10 and divided by 10
        return min(np.random.triangular(0.2, .7, 1.2), 1)

    def __init__(self):
        super(StandardAmmonia, self).__init__()
