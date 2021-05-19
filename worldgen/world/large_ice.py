from . import Atmosphere
from . import World

import numpy as np


class LargeIce(World):
    """the large ice world model"""

    class LargeIceAtmosphere(Atmosphere):
        """the large ice atmosphere model"""
        _composition = ['He', 'N2']
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True

    _temperature_range = World.Range(80, 230)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .2
    _hydrosphere_range = World.Range(0, .2)
    _absorption = .86
    _atmosphere = LargeIceAtmosphere

    @classmethod
    def random_hydrosphere(cls):
        # roll of 2d-10 minimum at 0 and divided by 10
        return max(np.random.triangular(-.8, -.3, .2), 0)

    def __init__(self):
        super(LargeIce, self).__init__()
