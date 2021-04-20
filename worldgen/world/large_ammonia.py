from . import World

import numpy as np


class LargeAmmonia(World):
    _temperature_range = World.Range(140, 215)
    _size = World.Size.LARGE
    _core = World.Core.ICY_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrosphere_range = World.Range(.2, 1)
    _absorption = .84
    _atmosphere = ['He', 'NH3', 'CH4']
    _toxicity = World.Toxicity.LETHAL

    @classmethod
    def random_hydrosphere(cls):
        # roll of 2d capped at 10 and divided by 10
        return min(np.random.triangular(0.2, .7, 1.2), 1)

    def __init__(self):
        super(LargeAmmonia, self).__init__()
