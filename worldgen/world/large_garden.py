from .. import Range
from .. import RandomizableModel
from .marginal_atmosphere import MarginalCandidate
from . import Atmosphere
from . import World

from scipy.stats import truncnorm
from random import uniform


class LargeGarden(World):
    """The large garden world model"""

    class LargeGardenAtmosphere(Atmosphere, MarginalCandidate,
                                RandomizableModel):
        """The large garden atmosphere model"""
        _composition = ['N2', 'O2', 'He', 'Ne', 'Ar', 'Kr', 'Xe']

        def randomize(self):
            """sum of a 3d roll to apply marginal modifier"""
            if truncnorm((3 - 10.5) / 2.958040, (18 - 10.5) / 2.958040,
                         loc=10.5, scale=2.958040).rvs() > 11:
                self.make_marginal()

    _temperature_range = Range(250, 340)
    _size = World.Size.LARGE
    _core = World.Core.LARGE_IRON_CORE
    _pressure_factor = 5
    _greenhouse_factor = .16
    _hydrosphere_range = Range(.7, 1)
    _atmosphere = LargeGardenAtmosphere

    def random_hydrosphere(self):
        """roll of 1d+6 maxed at 10 divided by 10"""
        self.hydrosphere = min(uniform(.7, 1.2), 1)

    @property
    def absorption(self):
        """absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d"""
        return (-0.7500000000000038 * self.hydrosphere ** 3 +
                1.2000000000000057 * self.hydrosphere ** 2 -
                0.6475000000000023 * self.hydrosphere + 1.0375000000000003)

    def __init__(self):
        super(LargeGarden, self).__init__()
