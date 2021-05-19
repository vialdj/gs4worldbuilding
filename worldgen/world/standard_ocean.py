from . import Atmosphere
from . import World

import random

from scipy.stats import truncnorm


class StandardOcean(World):
    """the standard ocean world model"""

    class StandardOceanAtmosphere(Atmosphere):
        """the standard ocean atmosphere model"""
        _composition = ['CO2', 'N2']
        _suffocating = True

        def randomize(self):
            """sum of a 3d roll to define toxicity"""
            if truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                         loc=10.5, scale=2.958040).rvs() > 12:
                self._toxicity = Atmosphere.Toxicity.MILD

    _temperature_range = World.Range(250, 340)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .16
    _hydrosphere_range = World.Range(.5, 1)
    _atmosphere = StandardOceanAtmosphere

    @classmethod
    def random_hydrosphere(cls):
        # roll of 1d+4 divided by 10
        return random.uniform(.5, 1)

    @property
    def absorption(self):
        # match hydrosphere to Temperature Factors Table
        assert(self.hydrosphere), "attribute is not applicable"
        d = {.20: .95, .50: .92, .90: .88, 1: .84}
        return d[list(filter(lambda x: x >= self.hydrosphere, sorted(d.keys())))[0]]

    def __init__(self):
        super(StandardOcean, self).__init__()
