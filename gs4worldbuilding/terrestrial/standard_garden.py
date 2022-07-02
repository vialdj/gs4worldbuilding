from astropy import units as u

from gs4worldbuilding.random import RandomGenerator
from gs4worldbuilding.model.bounds import QuantityBounds, ScalarBounds
from gs4worldbuilding.terrestrial.marginal_atmosphere import MarginalCandidate
from gs4worldbuilding.terrestrial import Terrestrial, Size, Core


class StandardGardenAtmosphere(MarginalCandidate):
    '''the standard garden atmosphere model'''
    _composition = ['N2', 'O2']

    def random_marginalize(self) -> None:
        '''sum of a 3d roll to apply marginal modifier if > 11'''
        if RandomGenerator().roll3d6() > 11:
            self.make_marginal()
        else:
            self.remove_marginal()

    def randomize(self):
        self.random_marginalize()

    def __init__(self, *args, **kwargs):
        self.random_marginalize()
        super().__init__(*args, **kwargs)


class StandardGarden(Terrestrial):
    '''the standard garden world model'''
    _temperature_bounds = QuantityBounds(250 * u.K, 340 * u.K)
    _size = Size.STANDARD
    _core = Core.LARGE_IRON_CORE
    _pressure_factor = 1
    _greenhouse_factor = .16
    _hydrographic_coverage_bounds = ScalarBounds(.5, 1)
    _atmosphere_type = StandardGardenAtmosphere

    def random_hydrographic_coverage(self) -> float:
        '''roll of 1d+4 divided by 10'''
        return RandomGenerator().roll1d6(4, continuous=True) / 10

    @property
    def absorption(self):
        '''absorbtion from Temperature Factors Table fitted
through a * x ** 3 + b * x ** 2 + c * x + d'''
        assert self.hydrographic_coverage is not None
        return min(.95, (-0.7500000000000038 *
                         self.hydrographic_coverage ** 3 +
                   1.2000000000000057 * self.hydrographic_coverage ** 2 -
                   0.6475000000000023 * self.hydrographic_coverage +
                   1.0375000000000003))

    def randomize(self) -> None:
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().randomize()

    def __init__(self, *args, **kwargs):
        self.hydrographic_coverage = self.random_hydrographic_coverage()
        super().__init__(*args, **kwargs)
