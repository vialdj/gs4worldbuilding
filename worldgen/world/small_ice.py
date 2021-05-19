from . import Atmosphere
from . import World

import random

from scipy.stats import truncnorm


class SmallIce(World):
    """the small ice world model"""

    class SmallIceAtmosphere(Atmosphere):
        """the small ice atmosphere model"""
        _composition = ['N2', 'CH4']
        _suffocating = True

        def randomize(self):
            """sum of a 3d roll to define toxicity"""
            if truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                         loc=10.5, scale=2.958040).rvs() <= 15:
                self._toxicity = Atmosphere.Toxicity.MILD
            else:
                self._toxicity = Atmosphere.Toxicity.HIGH

    _temperature_range = World.Range(80, 140)
    _size = World.Size.SMALL
    _core = World.Core.ICY_CORE
    _pressure_factor = 10
    _greenhouse_factor = .1
    _hydrosphere_range = World.Range(.3, .8)
    _absorption = .93
    _atmosphere = SmallIceAtmosphere

    @classmethod
    def random_hydrosphere(cls):
        # roll of 1d+2 divided by 10
        return random.uniform(.3, .8)

    def __init__(self):
        super(SmallIce, self).__init__()
