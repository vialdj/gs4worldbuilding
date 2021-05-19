from . import Atmosphere
from . import World

import numpy as np


class StandardIce(World):
    """the standard ice world model"""

    class StandardIceAtmosphere(Atmosphere):
        """the standard ice atmosphere model"""
        _composition = ['CO2', 'N2']

    _temperature_range = World.Range(80, 230)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .2
    _hydrosphere_range = World.Range(0, .2)
    _absorption = .86
    _atmosphere = StandardIceAtmosphere

    @classmethod
    def random_hydrosphere(cls):
        # roll of 2d-10 minimum at 0 and divided by 10
        return max(np.random.triangular(-.8, -.3, .2), 0)

    @classmethod
    def random_atm_seed(cls):
        """sum of a 3d roll"""
        return truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                         loc=10.5, scale=2.958040).rvs()

    def __init__(self):
        super(StandardIce, self).__init__()
