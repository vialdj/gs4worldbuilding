from . import World

import random


class SmallIce(World):
    _temperature_range = World.Range(80, 140)
    _size = World.Size.SMALL
    _core = World.Core.ICY_CORE
    _pressure_factor = 10
    _greenhouse_factor = .1
    _hydrosphere_range = World.Range(.3, .8)
    _absorption = .93
    _atmosphere = World.Atmosphere(composition=['N2', 'CH4'])

    def random_hydrosphere(cls):
        # roll of 1d+2 divided by 10
        return random.uniform(.3, .8)

    def __init__(self):
        super(SmallIce, self).__init__()
