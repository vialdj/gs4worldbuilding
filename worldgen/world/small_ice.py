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

    @classmethod
    def random_hydrosphere(cls):
        # roll of 1d+2 divided by 10
        return random.uniform(.3, .8)

    @classmethod
    def random_atm_seed(cls):
        """sum of a 3d roll"""
        return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                         loc=10.5, scale=2.958040).rvs()

    def __init__(self):
        super(SmallIce, self).__init__()
