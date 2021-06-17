from .. import Range
from . import Atmosphere
from . import World

import numpy as np


class LargeGreenhouse(World):
    """The large greenhouse world model"""

    class LargeGreenhouseAtmosphere(Atmosphere):
        """The large greenhouse atmosphere model"""
        _toxicity = Atmosphere.Toxicity.LETHAL
        _suffocating = True

        @property
        def composition(self):
            return ['CO2'] if self._world.hydrosphere < .1 else ['N2', 'H2O'
                                                                 'O2']

    _temperature_range = Range(500, 950)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 500
    _greenhouse_factor = 2.0
    _hydrosphere_range = Range(0, .5)
    _absorption = .77
    _atmosphere = LargeGreenhouseAtmosphere

    @classmethod
    def random_hydrosphere(cls):
        """roll of 2d-7 minimum at 0 and divided by 10"""
        return max(np.random.triangular(-.5, 0, .5), 0)

    def __init__(self):
        super(LargeGreenhouse, self).__init__()
