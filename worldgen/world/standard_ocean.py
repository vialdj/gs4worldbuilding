from .. import RandomizableModel
from . import Atmosphere
from . import World

from random import uniform
from scipy.stats import truncnorm


class StandardOcean(World):
    """the standard ocean world model"""

    class StandardOceanAtmosphere(Atmosphere, RandomizableModel):
        """the standard ocean atmosphere model"""
        _composition = ['CO2', 'N2']
        _suffocating = True
        _toxicity = None

        def randomize(self):
            """sum of a 3d roll to define toxicity if value > 12"""
            if uniform(0, 1) < .7407:
                self._toxicity = Atmosphere.Toxicity.MILD
            else:
                self._toxicity = None

    _temperature_range = World.Range(250, 340)
    _size = World.Size.STANDARD
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .16
    _hydrosphere_range = World.Range(.5, 1)
    _atmosphere = StandardOceanAtmosphere

    def random_hydrosphere(self):
        """roll of 1d+4 divided by 10"""
        self.hydrosphere = uniform(.5, 1)

    @property
    def absorption(self):
        """absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d"""
        return (-0.7500000000000038 * self.hydrosphere ** 3 +
                1.2000000000000057 * self.hydrosphere ** 2 -
                0.6475000000000023 * self.hydrosphere + 1.0375000000000003)

    def __init__(self):
        super(StandardOcean, self).__init__()
